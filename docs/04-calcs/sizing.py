"""PotholeLog sizing calculations, PHL-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Each line carries a tag such as
[B3] that the note cites. Geometry comes from cad/src/model.py (PARAMS, derived and part
volumes), the parts cost from bom/bom.csv and the budget from project.yaml.

Method: a linear quarter-car model of a city bus rear corner (sprung body, unsprung axle and
twin tyres) driven by (a) random road profiles with the ISO 8608 spectral shape, solved in the
frequency domain, and (b) a single pothole, enveloped by a rigid tyre circle and solved in the
time domain. The IRI of each profile comes from the standard golden-car model at 80 km/h.
First-principles estimates for a paper proof of concept; not a substitute for field data.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, build_parts  # noqa: E402

G = 9.81
RNG = np.random.default_rng(20260925)


def tag(t, text):
    print(f"[{t}] {text}")


def kmh(v):
    return v / 3.6


# ------------------------------------------------------------------ assumptions
# Bus rear corner (one side of the drive axle), mid load. Air suspension keeps the body
# frequency near 1.2 Hz across loads; twin tyres per side.
BUS = {"ms": 4500.0, "mu": 500.0, "fs": 1.2, "zeta": 0.20, "kt": 1.8e6}
LOAD_RANGE = (3500.0, 5250.0)       # kg sprung per side, empty to laden
GOLDEN = {"c": 6.0, "k1": 653.0, "k2": 63.3, "mu": 0.15}   # IRI reference quarter car, per unit sprung mass
IRI_V = kmh(80.0)
BASELEN = 0.25                       # m, 250 mm moving average used for IRI and as a tyre patch filter
N_BAND = (0.01, 10.0)                # cycles/m, spatial band of the random profiles
ISO_CLASSES = {"A": 16e-6, "B": 64e-6, "C": 256e-6, "D": 1024e-6}   # Gd(n0), m^3, n0 = 0.1 cycles/m
LOGGER_ONE_SIDE = 0.5                # share of a one-sided wheel input seen at the floor centerline (bounce only)
LOGGER_TWO_SIDE = math.sqrt((1 + 0.5) / 2)   # random roughness, left-right correlation 0.5
BAND_HZ = (0.5, 20.0)                # roughness metric band
IMU_NOISE = 100e-6                   # g per root Hz, LSM6DSO class at +/-16 g (to confirm from the datasheet)
FS = 400.0                           # Hz IMU output rate
FS_RANGE_G = 16.0
POTHOLE = {"depth": 0.050, "length": 0.300, "width": 0.300}   # R1 reference defect
TYRE_R = 0.52                        # m, 295/80 R22.5 class
TWIN_W = 0.60                        # m, width of a twin-tyre pair
WANDER = 0.25                        # m, standard deviation of lateral wander about the wheel path
WHEELBASE = 6.0                      # m, 12 m city bus class
FALSE_PER_KM = 1.0                   # allowed background threshold crossings per km, before clustering
SPEEDS = [10, 20, 30, 50, 80]        # km/h

print("PotholeLog sizing, PHL-CAL-001 v0.1")
D = derived(P)
print(f"Geometry from cad/src/model.py: plate {P['plate']} mm, holes {P['hole_pitch']} mm, box {P['box']} mm, "
      f"overall height {D['overall_h']:.0f} mm")


# ------------------------------------------------------------------ models
def bus_ss(ms=BUS["ms"], mu=BUS["mu"], fs=BUS["fs"], zeta=BUS["zeta"], kt=BUS["kt"], ks=None):
    ks = ms * (2 * math.pi * fs) ** 2 if ks is None else ks
    cs = 2 * zeta * math.sqrt(ks * ms)
    A = np.array([[0, 1, 0, 0],
                  [-ks / ms, -cs / ms, ks / ms, cs / ms],
                  [0, 0, 0, 1],
                  [ks / mu, cs / mu, -(ks + kt) / mu, -cs / mu]])
    B = np.array([[0], [0], [0], [kt / mu]])
    C = np.vstack([A[1], A[3], [1, 0, -1, 0]])      # sprung accel, unsprung accel, suspension travel
    return A, B, C, ks, cs


def golden_ss():
    c, k1, k2, mu = GOLDEN["c"], GOLDEN["k1"], GOLDEN["k2"], GOLDEN["mu"]
    A = np.array([[0, 1, 0, 0], [-k2, -c, k2, c], [0, 0, 0, 1], [k2 / mu, c / mu, -(k1 + k2) / mu, -c / mu]])
    B = np.array([[0], [0], [0], [k1 / mu]])
    C = np.array([[0, 1, 0, -1]])                    # relative velocity
    return A, B, C


def freq_resp(A, B, C, f):
    s = 2j * math.pi * f
    I = np.eye(A.shape[0])
    return np.array([(C @ np.linalg.solve(s * I - A, B)).ravel() for s in s])   # (nf, nout)


def patch(n):
    """250 mm moving-average filter in the spatial frequency domain."""
    x = math.pi * n * BASELEN
    return np.where(x == 0, 1.0, np.sin(x) / np.where(x == 0, 1, x))


def spectrum(gd0, w=2.0, n=None):
    n = np.geomspace(*N_BAND, 4000) if n is None else n
    return n, gd0 * (n / 0.1) ** (-w) * patch(n) ** 2


def iri(gd0, w=2.0):
    """Expected IRI (m/km) of a Gaussian profile: mean |relative velocity| / V."""
    n, gd = spectrum(gd0, w)
    f = n * IRI_V
    A, B, C = golden_ss()
    H = freq_resp(A, B, C, f)[:, 0]
    var = np.trapezoid(np.abs(H) ** 2 * gd / IRI_V, f)
    return math.sqrt(2 / math.pi) * math.sqrt(var) / IRI_V * 1000


def band(f):
    return ((f >= BAND_HZ[0]) & (f <= BAND_HZ[1])).astype(float)


def accel_stats(gd0, v, w=2.0, ss=None, filt=True):
    """Sprung acceleration RMS (m/s^2) in the metric band, its derivative RMS, and effective bandwidth."""
    n, gd = spectrum(gd0, w)
    f = n * v
    A, B, C = ss if ss is not None else bus_ss()[:3]
    Ha = freq_resp(A, B, C[:1], f)[:, 0]
    s = np.abs(Ha) ** 2 * gd / v * (band(f) if filt else 1.0)
    var = np.trapezoid(s, f)
    var_d = np.trapezoid((2 * math.pi * f) ** 2 * s, f)
    beff = var ** 2 / np.trapezoid(s ** 2, f)
    return math.sqrt(var), math.sqrt(var_d), beff


# ------------------------------------------------------------------ A. Road and vehicle model
print("\nA. Road and vehicle model")
A_, B_, C_, KS, CS = bus_ss()
fu = math.sqrt((KS + BUS["kt"]) / BUS["mu"]) / (2 * math.pi)
tag("A1", f"bus rear corner: sprung {BUS['ms']:.0f} kg, unsprung {BUS['mu']:.0f} kg, body {BUS['fs']} Hz "
          f"(ks {KS / 1e3:.0f} kN/m, cs {CS / 1e3:.1f} kN s/m), wheel hop {fu:.1f} Hz (kt {BUS['kt'] / 1e6:.1f} MN/m)")
IRI_CLASS = {k: iri(g) for k, g in ISO_CLASSES.items()}
tag("A2", "IRI of ISO 8608 profiles (w = 2, golden car at 80 km/h): " +
    ", ".join(f"class {k} {v:.2f} m/km" for k, v in IRI_CLASS.items()))
K_IRI = IRI_CLASS["A"] / math.sqrt(ISO_CLASSES["A"])


def gd_for_iri(i, w=2.0):
    """Gd(n0) that gives a target IRI (IRI scales with the square root of Gd)."""
    return (i / iri(1e-6, w)) ** 2 * 1e-6


tag("A3", f"IRI scales as sqrt(Gd0): IRI 2 m/km at Gd0 {gd_for_iri(2) * 1e6:.1f}e-6 m^3; IRI 4 at {gd_for_iri(4) * 1e6:.1f}e-6; "
          f"IRI 6 at {gd_for_iri(6) * 1e6:.1f}e-6")

# ------------------------------------------------------------------ B. Roughness signal and calibration (R3, R5)
print("\nB. Roughness signal and calibration (R3, R5)")
noise = IMU_NOISE * G * math.sqrt(BAND_HZ[1] - BAND_HZ[0])
lsb = 2 * FS_RANGE_G * G / 65536
tag("B1", f"IMU noise in the {BAND_HZ[0]} to {BAND_HZ[1]:.0f} Hz band: {noise * 1000:.1f} mm/s^2 RMS "
          f"({IMU_NOISE * 1e6:.0f} ug/rtHz); 1 LSB at +/-{FS_RANGE_G:.0f} g is {lsb * 1000:.1f} mm/s^2")
rows = []
for i_ in (1.0, 2.0, 4.0, 6.0):
    g0 = gd_for_iri(i_)
    rms = [accel_stats(g0, kmh(v))[0] * LOGGER_TWO_SIDE for v in SPEEDS]
    rows.append((i_, rms))
    tag("B2", f"IRI {i_:.0f} m/km: floor RMS accel (band) " +
        ", ".join(f"{v} km/h {r:.3f}" for v, r in zip(SPEEDS, rms)) + " m/s^2")
snr20 = rows[0][1][1] / noise
snr10 = rows[0][1][0] / noise
tag("B3", f"signal-to-noise on a smooth road (IRI 1): {snr10:.0f} at 10 km/h, {snr20:.0f} at 20 km/h")
r20, r80 = rows[1][1][1], rows[1][1][4]
r50 = rows[1][1][3]
tag("B4", f"speed effect at IRI 2: RMS at 80 km/h is {r80 / r20:.2f} x the 20 km/h value and {r80 / r50:.2f} x the 50 km/h value; "
          f"a metric normalized by v^0.5 varies {max(r / math.sqrt(v) for r, v in zip(rows[1][1], SPEEDS)) / min(r / math.sqrt(v) for r, v in zip(rows[1][1], SPEEDS)):.2f}:1 "
          f"over 10 to 80 km/h, so calibration is per speed band")
# segment estimate scatter and synthetic calibration
v50 = kmh(50)
sig, _, beff = accel_stats(gd_for_iri(3), v50)
T = 100 / v50
cv1 = 1 / math.sqrt(2 * beff * T)
tag("B5", f"100 m segment at 50 km/h: {T:.1f} s of data; effective bandwidth {beff:.2f} Hz; "
          f"random scatter of one RMS estimate {cv1 * 100:.0f} %, {cv1 / math.sqrt(5) * 100:.0f} % averaged over 5 passes")
n_sec = 40
iris, accs = [], []
for _ in range(n_sec):
    w = RNG.uniform(1.8, 2.2)
    i_true = RNG.uniform(1.0, 8.0)
    g0 = gd_for_iri(i_true, w)
    iris.append(iri(g0, w))
    accs.append(accel_stats(g0, v50, w)[0] * LOGGER_TWO_SIDE)
iris, accs = np.array(iris), np.array(accs)


def r2(x, y):
    a, b = np.polyfit(x, y, 1)
    return 1 - np.sum((y - (a * x + b)) ** 2) / np.sum((y - y.mean()) ** 2), a, b


r2_ideal, slope, icpt = r2(accs, iris)
noisy1 = accs * (1 + cv1 * RNG.standard_normal(n_sec))
noisy5 = accs * (1 + cv1 / math.sqrt(5) * RNG.standard_normal(n_sec))
tag("B6", f"synthetic calibration, {n_sec} sections, IRI 1 to 8 m/km, spectral slope 1.8 to 2.2: r^2 {r2_ideal:.3f} with expected RMS; "
          f"{r2(noisy1, iris)[0]:.3f} from one pass; {r2(noisy5, iris)[0]:.3f} from 5 passes; slope {slope:.1f} m/km per m/s^2")
g2 = gd_for_iri(2)
air = [accel_stats(g2, v50, ss=bus_ss(ms=m)[:3])[0] for m in LOAD_RANGE]
steel = [accel_stats(g2, v50, ss=bus_ss(ms=m, ks=KS)[:3])[0] for m in LOAD_RANGE]
nom = accel_stats(g2, v50)[0]
tag("B7", f"load sensitivity at 50 km/h, empty {LOAD_RANGE[0]:.0f} kg to laden {LOAD_RANGE[1]:.0f} kg per side: "
          f"air suspension {air[0] / nom:.2f} to {air[1] / nom:.2f} of mid-load RMS; steel springs {steel[0] / nom:.2f} to {steel[1] / nom:.2f}")

# ------------------------------------------------------------------ C. Pothole detection (R1, R2, R6)
print("\nC. Pothole detection (R1, R2, R6)")
dx = 0.002
x = np.arange(-3.0, 12.0, dx)
k = int(TYRE_R / dx)
off = np.arange(-k, k + 1) * dx
circ = np.sqrt(np.maximum(TYRE_R ** 2 - off ** 2, 0)) - TYRE_R


def envelope(depth, length):
    """Rigid-circle envelope: wheel center height = max over the road of (road + circle), minus R."""
    road = np.where((x >= 0) & (x <= length), -depth, 0.0)
    pad = np.pad(road, k, constant_values=0.0)
    return np.max(np.lib.stride_tricks.sliding_window_view(pad, 2 * k + 1) + circ, axis=1)


env = envelope(POTHOLE["depth"], POTHOLE["length"])
drop = -env.min()
geo = TYRE_R - math.sqrt(TYRE_R ** 2 - (POTHOLE["length"] / 2) ** 2)
defl = (BUS["ms"] + BUS["mu"]) * G / BUS["kt"]
patch_l = 2 * math.sqrt(2 * TYRE_R * defl)
tag("C1", f"reference pothole {POTHOLE['depth'] * 1000:.0f} mm deep, {POTHOLE['length'] * 1000:.0f} mm long: a {TYRE_R * 2000:.0f} mm tyre "
          f"drops only {drop * 1000:.1f} mm (geometry {geo * 1000:.1f} mm) and climbs out over {POTHOLE['length'] / 2 * 1000:.0f} mm; "
          f"static tyre deflection {defl * 1000:.0f} mm gives a contact patch about {patch_l * 1000:.0f} mm long, so the tyre bridges much of the hole")
sys_c = signal.StateSpace(A_, B_, C_, np.zeros((3, 1)))


def threshold(i_, V, per_km):
    """Floor acceleration exceeded (either sign) per_km times per km on a road of IRI i_ (Rice formula, Gaussian)."""
    s_a, s_d, _ = accel_stats(gd_for_iri(i_), V, filt=False)
    s_a *= LOGGER_TWO_SIDE
    s_d *= LOGGER_TWO_SIDE
    nu0 = s_d / (2 * math.pi * s_a)
    return s_a * math.sqrt(2 * math.log(2 * nu0 * 1000 / (V * per_km)))


def pothole_peaks(e, v):
    V = kmh(v)
    t = (x - x[0]) / V
    _, y, _ = signal.lsim(sys_c, e, t)
    a_s = y[:, 0] * LOGGER_ONE_SIDE
    idx = np.arange(0, len(t), max(1, int(round(1 / (FS * (t[1] - t[0]))))))
    return np.abs(a_s).max(), np.abs(a_s[idx]).max(), np.abs(y[:, 1]).max()


peaks = {}
for v in SPEEDS:
    pk, pk400, pku = pothole_peaks(env, v)
    th = {i_: threshold(i_, kmh(v), FALSE_PER_KM) for i_ in (2.0, 4.0)}
    peaks[v] = (pk, pk400, pku, th)
for v, (pk, pk400, pku, th) in peaks.items():
    tag("C2", f"{v} km/h: floor peak {pk:.2f} m/s^2 ({pk / G:.3f} g), {pk400:.2f} at 400 Hz; axle peak {pku / G:.1f} g; "
              f"threshold for {FALSE_PER_KM:.0f} false crossing/km {th[2.0]:.2f} (IRI 2) and {th[4.0]:.2f} m/s^2 (IRI 4); "
              f"margin {pk400 / th[2.0]:.2f} and {pk400 / th[4.0]:.2f}")
det = {v: (peaks[v][1] / peaks[v][3][2.0], peaks[v][1] / peaks[v][3][4.0]) for v in SPEEDS}
det10 = {v: peaks[v][1] / threshold(4.0, kmh(v), 10.0) for v in SPEEDS}
tag("C2b", "allowing 10 background crossings per km (clusters need repeat passes), margin at IRI 4: " +
    ", ".join(f"{v} km/h {det10[v]:.2f}" for v in SPEEDS))
env_long = envelope(POTHOLE["depth"], 0.600)
det_long = {v: pothole_peaks(env_long, v)[1] / threshold(4.0, kmh(v), FALSE_PER_KM) for v in SPEEDS}
tag("C2c", f"a {POTHOLE['depth'] * 1000:.0f} mm deep, 600 mm long pothole (tyre drops {-env_long.min() * 1000:.0f} mm), margin at IRI 4: " +
    ", ".join(f"{v} km/h {det_long[v]:.2f}" for v in SPEEDS))
hit = math.erf(((TWIN_W + POTHOLE["width"]) / 2) / (WANDER * math.sqrt(2)))
tag("C3", f"chance the twin tyres hit a {POTHOLE['width'] * 1000:.0f} mm pothole centered in the wheel path: {hit:.2f} per pass "
          f"(lateral wander sigma {WANDER * 1000:.0f} mm); {1 - (1 - hit) ** 3:.4f} within 3 passes if every hit is detected")
worst_axle = max(p[2] for p in peaks.values()) / G
tag("C4", f"range: floor peak at most {max(p[0] for p in peaks.values()) / G:.2f} g against +/-{FS_RANGE_G:.0f} g; "
          f"the axle would see up to {worst_axle:.0f} g in this linear model, {worst_axle / (max(p[0] for p in peaks.values()) / G):.0f} times the floor peak, "
          f"with water and stones; the floor mount keeps the IMU far inside its range")
tag("C5", f"sampling: 400 Hz keeps {min(peaks[v][1] / peaks[v][0] for v in SPEEDS) * 100:.0f} % or more of the floor peak; "
          f"sample spacing {kmh(50) / FS * 1000:.0f} mm at 50 km/h, {kmh(80) / FS * 1000:.0f} mm at 80 km/h; "
          f"{POTHOLE['length'] / (kmh(50) / FS):.0f} samples across the pothole at 50 km/h, {POTHOLE['length'] / (kmh(80) / FS):.0f} at 80 km/h")
tag("C6", f"front and rear axle impacts are {WHEELBASE:.0f} m apart: {WHEELBASE / kmh(30):.2f} s at 30 km/h, {WHEELBASE / kmh(50):.2f} s at 50 km/h; "
          f"pairing them checks each event and attributes it to the rear axle")

# ------------------------------------------------------------------ D. Location (R4)
print("\nD. Location (R4)")
CEP_OPEN = 1.5                     # m, u-blox M10 class open-sky CEP (to confirm)
SIG = {"open sky": CEP_OPEN / 1.1774, "suburban": 3.0, "dense urban": 10.0}   # m per axis
SYNC = {"PPS": 0.010, "NMEA only": 0.100}   # s timing error between IMU and GNSS
for name, s in SIG.items():
    r95 = 2.4477 * s
    r10 = 2.4477 * s * math.sqrt(0.5 + 0.5 / 10) if name == "dense urban" else 2.4477 * s / math.sqrt(10)
    tag("D1", f"{name}: sigma {s:.1f} m per axis; 95 % radius {r95:.1f} m on one pass; {r10:.1f} m for a 10-pass cluster "
              f"({'errors 0.5 correlated between passes' if name == 'dense urban' else 'independent errors'})")
tag("D2", f"timing: at 80 km/h a {SYNC['PPS'] * 1000:.0f} ms IMU-to-GNSS error is {SYNC['PPS'] * kmh(80):.2f} m (with PPS); "
          f"{SYNC['NMEA only'] * 1000:.0f} ms is {SYNC['NMEA only'] * kmh(80):.1f} m (message time only); fix spacing {kmh(80) / 10:.1f} m at 10 Hz")
tag("D3", f"axle attribution: an event assigned to the wrong axle is misplaced by the {WHEELBASE:.0f} m wheelbase")

# ------------------------------------------------------------------ E. Storage and upload (R7, R8)
print("\nE. Storage and upload (R7, R8)")
IMU_B = 6 * 2 * FS                 # 6 axes, 16 bit
GNSS_B = 40 * 10                   # 40 B record at 10 Hz
HDR_B = 8 * FS / 100               # 8 B time stamp per 100-sample block
HOURS = (10.0, 12.0)
CARD = 32e9 * 0.94                 # bytes usable after formatting
rate = IMU_B + GNSS_B + HDR_B
day = [rate * h * 3600 for h in HOURS]
tag("E1", f"raw data rate {rate / 1000:.2f} kB/s (IMU {IMU_B / 1000:.1f}, GNSS {GNSS_B / 1000:.1f}, time stamps {HDR_B:.0f} B/s); "
          f"{day[0] / 1e6:.0f} MB per {HOURS[0]:.0f} h day, {day[1] / 1e6:.0f} MB per {HOURS[1]:.0f} h day")
tag("E2", f"32 GB card: {CARD / day[0]:.0f} days at {HOURS[0]:.0f} h, {CARD / day[1]:.0f} days at {HOURS[1]:.0f} h of driving")
tag("E3", f"card wear over 5 years: {day[1] * 365 * 5 / 1e9:.0f} GB written, {day[1] * 365 * 5 / CARD:.0f} full-card writes")
SEG_B = {"start lat, lon": 8, "end lat, lon": 8, "pass time (s, operator copy only)": 4, "duration (0.1 s)": 2,
         "mean speed and speed band": 3, "roughness metric (float)": 4, "IRI estimate (0.01 m/km)": 2,
         "peak and crest factor": 4, "samples, GNSS quality, flags": 5, "vehicle and pass IDs": 8}
EV_B = {"lat, lon": 8, "time": 4, "speed": 2, "peak accel": 2, "peak gyro roll": 2, "duration": 2, "axle pairing": 2,
        "heading": 2, "GNSS quality": 2, "vehicle and pass IDs": 6}
KM_DAY, EV_DAY = 200, 500
summ = KM_DAY * 10 * sum(SEG_B.values()) + EV_DAY * sum(EV_B.values())
tag("E4", f"segment record {sum(SEG_B.values())} B, event record {sum(EV_B.values())} B; {KM_DAY} km and {EV_DAY} events a day give "
          f"{summ / 1e3:.0f} kB of summaries")
WIFI = 2e6                          # bit/s effective at the edge of depot coverage
CONNECT = 8.0                       # s join, DHCP, TLS
t_up = CONNECT + summ * 8 / WIFI
tag("E5", f"upload at {WIFI / 1e6:.0f} Mbit/s effective: {t_up:.1f} s including {CONNECT:.0f} s to connect; "
          f"raw data for a day would take {day[0] * 8 / WIFI / 60:.0f} min, so raw data stays on the card")

# ------------------------------------------------------------------ F. Power and transients (R9)
print("\nF. Power and transients (R9)")
LOADS_3V3 = {"ESP32-S3, 240 MHz, radio off": 0.060, "board overhead": 0.010, "GNSS tracking": 0.010,
             "microSD average": 0.010, "IMU at 416 Hz": 0.001}
I3 = sum(LOADS_3V3.values())
P5 = I3 * 5.0                       # linear regulator on the board: 5 V in, same current
ETA = 0.85
P_IN = P5 / ETA
tag("F1", f"3.3 V loads {I3 * 1000:.0f} mA; {P5:.2f} W at 5 V through the board's linear regulator; "
          f"{P_IN:.2f} W from the vehicle at {ETA * 100:.0f} % converter efficiency")
tag("F2", f"supply current {P_IN / 12 * 1000:.0f} mA at 12 V, {P_IN / 24 * 1000:.0f} mA at 24 V, {P_IN / 9 * 1000:.0f} mA at 9 V; inline fuse 2 A")
I_WIFI = 0.150                      # A average extra while uploading
P_UP = (I3 + I_WIFI) * 5.0 / ETA
tag("F3", f"while uploading: {P_UP:.2f} W for about {t_up:.0f} s a day; daily energy {P_IN * HOURS[0]:.1f} Wh over {HOURS[0]:.0f} h "
          f"(about {P_IN * HOURS[0] / 12 * 1000:.0f} mAh at 12 V)")
LEVELS = {"12 V system, normal": (9, 16), "24 V system, normal": (18, 32),
          "12 V, suppressed load dump (ISO 16750-2 test B, to confirm)": (35, 35),
          "24 V, suppressed load dump (ISO 16750-2 test B, to confirm)": (58, 58)}
CONV_MAX, TVS_VC = 36.0, 58.1
for k_, (lo, hi) in LEVELS.items():
    tag("F4", f"{k_}: {lo if lo == hi else f'{lo} to {hi}'} V against the 36 V converter input: {'within' if hi <= CONV_MAX else 'EXCEEDS'}")
tag("F5", f"SMBJ36A-class TVS clamps at up to {TVS_VC} V at its rated pulse current, above the {CONV_MAX:.0f} V converter rating; "
          f"a 60 V-rated converter would clear the clamp by {60 - TVS_VC:.1f} V")

# ------------------------------------------------------------------ G. Hold-up (R10)
print("\nG. Hold-up (R10)")
C_F, V_RAIL, V_DIODE, V_MIN = 1.0, 5.0, 0.3, 3.6
AGE = 0.7                            # capacitance at end of life and -20 degC (tolerance, ageing, cold)
e_hold = 0.5 * C_F * ((V_RAIL - V_DIODE) ** 2 - V_MIN ** 2)
t_new = e_hold / P5
t_old = e_hold * AGE / P5
T_CLOSE = 1.0                        # s to flush buffers and close files, with worst-case card latency
tag("G1", f"1 F from {V_RAIL - V_DIODE:.1f} V to {V_MIN} V stores {e_hold:.2f} J; at {P5:.2f} W it lasts {t_new:.1f} s new, "
          f"{t_old:.1f} s at {AGE:.0%} capacitance; closing files needs about {T_CLOSE:.0f} s, a factor of {t_old / T_CLOSE:.0f}")
R_CH = 10.0
tag("G2", f"charging through {R_CH:.0f} ohm: time constant {R_CH * C_F:.0f} s, 95 % after {3 * R_CH * C_F:.0f} s; "
          f"peak charge current {V_RAIL / R_CH:.1f} A within the 1 A converter")
tag("G3", f"Wi-Fi on the hold-up alone: {e_hold * AGE / P_UP:.1f} s at {P_UP:.2f} W, too short to join a network, so uploads run with the ignition on")

# ------------------------------------------------------------------ H. Environment and fixings (R11)
print("\nH. Environment and fixings (R11)")
parts = build_parts()
bl, bw = P["box"]
bh = D["box_h"]
area = bl * bw + 2 * (bl + bw) * bh     # top and sides, mm^2; the base sits on the plate
H_CONV = 8.0                           # W/m^2K, still cabin air, convection plus radiation
dT = P_IN / (H_CONV * area / 1e6)
tag("H1", f"self-heating: {P_IN:.2f} W over {area / 100:.0f} cm^2 of box at {H_CONV:.0f} W/m^2K raises the inside by {dT:.1f} K; "
          f"at +70 degC ambient the parts see about {70 + dT:.0f} degC")
RHO = {"plate": 2.68, "base": 1.20, "lid": 1.20}
M_BUY = {"converter": 15, "supercap": 6, "controller": 10, "imu": 2, "gnss": 12, "sd": 0.5,
         "gland": 12, "lead": 2 * 45, "fixings": 4 * 12}
m_plate = parts["plate"].volume / 1000 * RHO["plate"]
m_box = (parts["base"].volume + parts["lid"].volume) / 1000 * RHO["base"]
m_inside = sum(M_BUY[k] for k in ("converter", "supercap", "controller", "imu", "gnss", "sd"))
m_logger = m_plate + m_box + m_inside + M_BUY["gland"]
m_total = m_logger + M_BUY["lead"] + M_BUY["fixings"]
tag("H2", f"mass: plate {m_plate:.0f} g, enclosure {m_box:.0f} g (polycarbonate), modules {m_inside:.0f} g, gland {M_BUY['gland']} g: "
          f"logger {m_logger / 1000:.2f} kg; with 2 m lead and fixings {m_total / 1000:.2f} kg")
CRASH_G, BUMP_G = 20.0, 10.0
F_crash = m_logger / 1000 * CRASH_G * G
M6_SHEAR = 0.6 * 800 * 20.1         # N, property class 8.8, stress area 20.1 mm^2
m_above = (m_box + m_inside) / 1000
F_box = m_above * CRASH_G * G
tag("H3", f"{CRASH_G:.0f} g crash pulse: {F_crash:.0f} N on the plate, {F_crash / 4:.0f} N per M6 bolt against about {M6_SHEAR / 1000:.1f} kN "
          f"shear capacity (factor {M6_SHEAR / (F_crash / 4):.0f}); {F_box:.0f} N on the 4 M4 box screws")

# ------------------------------------------------------------------ I. Plate stiffness and installation (R12)
print("\nI. Plate stiffness and installation (R12)")
E_AL = 70e9
pl, pw, pt = [v / 1000 for v in P["plate"]]
span = P["hole_pitch"][0] / 1000
b_eff = 0.5 * pw                     # point supports at the corners: half the width carries the load
I_ = b_eff * pt ** 3 / 12
k_pl = 48 * E_AL * I_ / span ** 3
m_eff = m_above + 17 / 35 * m_plate / 1000
f1 = math.sqrt(k_pl / m_eff) / (2 * math.pi)
I_full = pw * pt ** 3 / 12
f_full = math.sqrt(48 * E_AL * I_full / span ** 3 / m_eff) / (2 * math.pi)
tag("I1", f"plate spanning {span * 1000:.0f} mm between bolt lines with nothing beneath: k {k_pl / 1e3:.0f} kN/m, "
          f"moving mass {m_eff * 1000:.0f} g, first mode {f1:.0f} Hz (half-width, corner bolts); {f_full:.0f} Hz on full-width supports")
t_needed = pt * 1000 * (150 / f1) ** (2 / 3)
tag("I2", f"thickness for 150 Hz on the half-width model: {t_needed:.1f} mm; a plate laid flat on a rigid floor is stiffer still")
TASKS = {"secure vehicle, isolate battery": 3, "open access to the fixings": 5, "place plate, fit and torque 4 M6 bolts": 5,
         "route 2 m lead along the loom, tie": 8, "connect to fused ignition feed (fuse tap)": 4,
         "reconnect, power up, check GNSS fix and Wi-Fi from a phone": 5}
tag("I3", "installation tasks: " + "; ".join(f"{k_} {v} min" for k_, v in TASKS.items()) + f"; total {sum(TASKS.values())} min")
sock = P["hole_pitch"][0] / 2 - bl / 2
tag("I4", f"bolt tool clearance: hole centers are {sock:.0f} mm beyond the box end walls; a 10 mm socket (about 16 mm OD) leaves {sock - 8:.0f} mm")

# ------------------------------------------------------------------ J. Cost (R15)
print("\nJ. Cost (R15)")
with open(ROOT / "bom" / "bom.csv") as fh:
    bom = list(csv.DictReader(fh))
total = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in bom)
import yaml  # noqa: E402
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
tag("J1", f"BOM {len(bom)} lines, ${total:.2f} against budget_usd ${budget:.0f}: margin ${budget - total:.2f}")
tag("J2", f"a 60 V-rated converter (about $2 more) would give ${total + 2:.2f}; LTE-M option (about $20 to $30) would give "
          f"${total + 20:.0f} to ${total + 30:.0f}")

# ------------------------------------------------------------------ K. Summary for the results table
print("\nK. Summary")
tag("K1", f"detection margin at IRI 2: " + ", ".join(f"{v} km/h {det[v][0]:.2f}" for v in SPEEDS) +
    f"; at IRI 4: " + ", ".join(f"{v} km/h {det[v][1]:.2f}" for v in SPEEDS))
