# Original chill reggaeton (dembow) background bed, synthesized from scratch.
# Usage: python beat.py out.wav duration_seconds
import sys, wave
import numpy as np

SR = 48000
OUT, DUR = sys.argv[1], float(sys.argv[2])
BPM = 92.0
beat = 60.0 / BPM
s16 = beat / 4
N = int(DUR * SR) + SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)

# arrangement switches (seconds, aligned with the edit)
BREAK = (54.9, 56.2)     # drums drop before "וגולת הכותרת", back when the title lands
END_DRUMS = 62.37        # end card: drums stop, pads ring out

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i]
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l
    R[i:i + len(sig)] += sig * gain * r

def env(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
    return e

def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 48 + 90 * np.exp(-t * 35)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(1.6 * np.sin(ph) * np.exp(-t * 9))

def snare():
    n = int(0.18 * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    noise = np.convolve(noise, np.ones(3) / 3, 'same') - np.convolve(noise, np.ones(40) / 40, 'same')
    body = np.sin(2 * np.pi * 210 * t) * np.exp(-t * 30)
    return (0.6 * noise * np.exp(-t * 26) + 0.5 * body)

def hat(open_=False):
    n = int((0.12 if open_ else 0.04) * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n); x = x - np.convolve(x, np.ones(8) / 8, 'same')
    return x * np.exp(-t * (18 if open_ else 90))

def bass(freq, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(4 * np.pi * freq * t)
    e = np.minimum(1, t / 0.005) * np.exp(-t / (dur * 0.9))
    return np.tanh(3.2 * x) * e

def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.0, 0.12):
            x += np.sin(2 * np.pi * f * (1 + det / 100) * t + rng.uniform(0, 6.28))
    a = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)
    # soft low-pass via moving average
    k = 3; x = np.convolve(x, np.ones(k) / k, 'same')
    return x * a / (3 * len(freqs))

def pluck(freq, dur=0.9):
    # Karplus-Strong nylon-ish pluck
    n = int(dur * SR); p = int(SR / freq)
    buf = rng.uniform(-1, 1, p); out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * np.exp(-np.arange(n) / SR * 2.5)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

# Am - F - C - G (one bar each), warm minor loop
prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]
bar = 4 * beat
nbars = int(DUR / bar) + 1
plk_cache = {}
for b in range(nbars):
    t0 = b * bar
    root, chord = prog[b % 4]
    # pads through the whole piece
    add(pad([hz(m + 12) for m in chord], bar + 0.3), t0, 0.7, 0.0)
    in_break = lambda t: BREAK[0] <= t < BREAK[1]
    for k in range(16):
        t = t0 + k * s16
        if t >= DUR: break
        drums = t < END_DRUMS and not in_break(t)
        if drums:
            if k % 4 == 0: add(kick(), t, 0.6)
            if k in (3, 6, 11, 14): add(snare(), t, 0.42, 0.1)
            if k % 2 == 0: add(hat(k in (6, 14)), t, 0.16, -0.25)
            add(hat(), t + 0.004, 0.05, 0.3)  # shaker 16ths
        # bass on the dembow pulse
        if drums and k in (0, 3, 8, 11):
            add(bass(hz(root - 12), s16 * (3 if k in (0, 8) else 2)), t, 0.4)
    # guitar arpeggio, half-time, soft
    if t0 < END_DRUMS + bar:
        notes = [chord[0] + 12, chord[1] + 12, chord[2] + 12, chord[1] + 12]
        for j, m in enumerate(notes):
            t = t0 + j * beat + (beat / 2 if j % 2 else 0)
            if t < DUR and not (BREAK[0] <= t < BREAK[1] - 0.5):
                if m not in plk_cache: plk_cache[m] = pluck(hz(m))
                add(plk_cache[m], t, 0.6, 0.35 if j % 2 else -0.35)

# marimba lead: a short catchy 2-bar motif, mid range (phone-audible)
def marimba(freq, dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2*np.pi*freq*t) + 0.35*np.sin(2*np.pi*freq*4*t)*np.exp(-t*30)
    return x * np.minimum(1, t/0.002) * np.exp(-t*7)
motif = [(0,76),(1.5,74),(2,72),(3,69),(4,72),(5.5,71),(6,67),(7,69)]  # beats, midi (A minor)
for b in range(0, nbars, 2):
    t0 = b * bar
    for bt, m in motif:
        t = t0 + bt * beat
        if t < END_DRUMS and not (BREAK[0] - 0.3 <= t < BREAK[1]):
            add(marimba(hz(m)), t, 0.5, 0.15)

# riser into the hero moment
n = int((BREAK[1] - BREAK[0]) * SR); t = np.arange(n) / SR
riser = rng.standard_normal(n); riser = riser - np.convolve(riser, np.ones(30) / 30, 'same')
add(riser * (t / t[-1]) ** 2 * 0.12, BREAK[0])

# master: gentle fade-in, fade-out at the end, normalise
Lm, Rm = L[: int(DUR * SR)], R[: int(DUR * SR)]
tt = np.arange(len(Lm)) / SR
fade = np.minimum(1, tt / 0.8) * np.clip((DUR - tt) / 1.6, 0, 1)
Lm *= fade; Rm *= fade
peak = max(np.abs(Lm).max(), np.abs(Rm).max())
st = np.stack([Lm, Rm], 1) / peak * 0.85
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print(OUT, round(DUR, 2))
