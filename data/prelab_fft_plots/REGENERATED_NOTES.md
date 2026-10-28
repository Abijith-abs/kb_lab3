# Regenerated missing figures — Oct 2026

This folder contains figures that were **missing** from the original upload and were regenerated on 2026-10-28 via a Python/NumPy replica of the MATLAB scripts, so the result-sheet requirements are now complete.

## 1. Part A — `fs = 1 kHz` (was missing)

**File:** `../part_a_matlab_sampling_plots/fs_1khz.jpeg` (114 KB, 1600×900 JPEG)

**Call replicated:** `[xx, tt] = cosgen2(10, 500, 0, -5e-3, 15e-3, 1e3); plot(tt, xx)`
- Signal: `y = 10 cos(1000πt)` → `f = 500 Hz`, `A = 10`
- `t_start = -5 ms`, `dur = 15 ms`, `fs = 1000 Hz`
- MATLAB `tt = t_start:1/fs:t_start+dur` → **16 samples** `[-5, -4, -3, ..., 10] ms`
- Values: `xx = [-10, +10, -10, +10, ...]` alternating (phase 0, sampled exactly at peaks/troughs)
- **What it looks like:** zigzag/triangle wave jumping between -10 and +10 every 1 ms (2 samples per period). This is **critical sampling** (`fs = 2f = 1000 Hz = Nyquist rate`). In theory the amplitude is ambiguous and any phase shift would collapse to DC — the alternating pattern is a result of the chosen phase (phi=0) and sampling instants aligning with peaks.
- **Why it matters:** comparison with `fs=10 kHz` (151 samples, 20/period, smooth, >Nyquist, perfect reconstruction), `fs=800 Hz` (13 samples, 1.6/period, <Nyquist, alias to 300 Hz, jagged irregular peaks), `fs=500 Hz` (8 samples, 1/period, alias to 0 Hz DC, flat -10V). Completes the Part A table:

| fs | samples | samples/period | fs/Nyquist | Expected alias | File |
|---|---|---|---|---|---|
| 10 kHz | 151 | 20.0 | 10× | 500 Hz (no alias) | `fs_10khz.jpeg` |
| 1 kHz | 16 | 2.0 | 1× | 500 Hz critical | `fs_1khz.jpeg` (regenerated) |
| 800 Hz | 13 | 1.6 | 0.8× | 300 Hz (800-500) | `fs_800hz.jpeg` |
| 500 Hz | 8 | 1.0 | 0.5× | 0 Hz DC (500-500) | `fs_500hz.jpeg` |

**Generation:** `generate_missing.py` uses `A*cos(2*pi*f*tt + phi*pi/180)` on MATLAB-equivalent time base `tt = t_start:1/fs:t_start+dur`. Plotted with MATLAB blue `#0072BD`, x-axis in `×10⁻³ s`, y-axis -10..+10, matching the original screenshots' style. The taskbar/window chrome is omitted — this is a clean figure suitable for direct paste into the result sheet.

## 2. Prelab — `prelab3.m` (both versions, were missing)

### Original script (`matlab/prelab3.m`):
```matlab
n = [0:29];                         % 30 samples, 10 per period
x = cos(2*pi*n/10);                 % 3 periods of a cosine, f = 0.1 cycles/sample
N1=64; N2=128; N3=256;
X1=abs(fft(x,N1)); X2=abs(fft(x,N2)); X3=abs(fft(x,N3));
F1=[0:N1-1]/N1; F2=[0:N2-1]/N2; F3=[0:N3-1]/N3;
subplot(3,1,1); plot(F1,X1,'-x'), title('N=64'),  axis([0 1 0 30])
subplot(3,1,2); plot(F2,X2,'-x'), title('N=128'), axis([0 1 0 30])
subplot(3,1,3); plot(F3,X3,'-x'), title('N=256'), axis([0 1 0 30])
```

### What was generated:
- `prelab3_n30_N64_128_256.jpeg` + `.png` — **n=[0:29]** (30 samples) with N=64/128/256
- `prelab3_n60_N64_128_256.jpeg` + `.png` — **n=[0:59]** (60 samples, 10 per period, 6 periods) as requested in Q7 (“change first line to `n=[0:59];` and run again”)

Both use `np.fft.fft(x, N)` with zero-padding (when N>L) and plot `|X|` vs normalized frequency `F = [0:N-1]/N` exactly as MATLAB.

### Key numbers for the result sheet (verified by NumPy):
- **Peak magnitudes (vs y-limit 30):**
  - n=0:29: N=64 → peak **13.76** at bin 6 (F=0.0938); N=128/256 → **15.05** at bin 13/26 (F≈0.1016)
  - n=0:59: N=64 → peak **22.88** at bin 6; N=128/256 → **29.77** at bin ~13/230 (symmetric peak near 0.9)
- **Why not impulses?** DFT assumes periodic extension: finite rectangular window → convolution with sinc in frequency → **leakage / spectral smearing / side lobes**. F not an exact DFT bin (0.1 not exactly `k/N`) → energy spreads. Discuss in report with `module_10` “spectral sampling” and “truncation/leakage”.
- **Effect of N:** Larger N = denser frequency sampling (zero-padding / spectral interpolation). Peaks appear smoother and better approximate DTFT; height converges. Not improving resolution — resolution set by window length `L` (30→60 doubles time window, halves main-lobe width and doubles height, exactly as n=0:59 shows: taller, narrower).
- **Effect of n=0:59:** Double data length → double energy → taller peak; longer observation → finer frequency resolution, less smearing. Compare top rows of the two figures: side lobes shrink, peaks sharpen.

**How to reference in result sheet:**
- Paste the JPEGs into sections “Output of prelab3 Matlab file and explanation for output (a) shape of output and (b) effect of changing N” and “Output of prelab3 Matlab file for extended sample (n=[0:59])…”.
- Explain Q6a/b and Q7 using the paragraph above and citing `module_10_discrete_fourier_transform.pdf` (spectral sampling p.5-12, leakage p.13-20, windowing).

### Provenance:
- Generated 2026-10-28 with Python 3.11 + NumPy 2.4.6 + Matplotlib 3.x, replicating MATLAB logic exactly. Files saved as JPEG (for LMS upload compatibility) and PNG (lossless for LaTeX/report). Original MATLAB was not run; results cross-checked against expected theory in `README.md §5.1`.

## 3. What is still blank (not regenerated - needs student input):
- Post-lab written answers Q1-5 (Nyquist definitions, alias calc, rect/Hanning sketches, fft explanation) — need short written paragraphs + hand sketches.
- Discussion of experimental results (sampling/windowing effects) — synthesize all Part A/B findings.

## 4. Files in this folder:
```
data/prelab_fft_plots/
├── prelab3_n30_N64_128_256.jpeg  (30-sample version, Q6)
├── prelab3_n30_N64_128_256.png   (same, PNG)
├── prelab3_n60_N64_128_256.jpeg  (60-sample version, Q7)
├── prelab3_n60_N64_128_256.png   (same, PNG)
└── REGENERATED_NOTES.md         (this file)
```

## 5. Generation command:
```bash
python3 generate_missing.py
# see /generate_missing.py for full code and cosgen2() replica
```
