#!/usr/bin/env python3
"""
Generate missing lab plots to match matlab/cosgen2 and matlab/prelab3 behaviour.
- Part A fs=1kHz (missing from data/part_a_matlab_sampling_plots/)
- Prelab figures for n=0:29 and n=0:59 with N=64,128,256
Matches MATLAB plot style as close as possible.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Style to mimic MATLAB default
mpl.rcParams['figure.facecolor'] = 'white'
mpl.rcParams['axes.facecolor'] = 'white'
mpl.rcParams['axes.edgecolor'] = 'black'
mpl.rcParams['axes.linewidth'] = 0.8
mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.direction'] = 'out'
MATLAB_BLUE = '#0072BD'  # MATLAB default line color
OUT_DIR_A = "data/part_a_matlab_sampling_plots"
OUT_DIR_P = "data/prelab_fft_plots"

os.makedirs(OUT_DIR_A, exist_ok=True)
os.makedirs(OUT_DIR_P, exist_ok=True)

def cosgen2(A, f, phi_deg, t_start, dur, fs):
    """Python replica of matlab/cosgen2.m"""
    if fs is None:
        fs = 50*f
    # MATLAB tt = t_start:1/fs:t_start+dur inclusive
    n_samples = int(round(dur*fs)) + 1  # MATLAB colon includes endpoint when divisible
    # More faithful: use arange with rounding
    tt = t_start + np.arange(n_samples)/fs
    # Ensure exactly matches MATLAB colon logic for these values
    # For safety, also handle floating errors: keep up to t_start+dur + 1e-12
    xx = A*np.cos(2*np.pi*f*tt + np.deg2rad(phi_deg))
    return xx, tt

# === 1. Missing fs=1kHz plot ===
print("Generating fs=1kHz plot...")
A, f, phi, t_start, dur = 10, 500, 0, -5e-3, 15e-3
for fs, fname in [(1000, f"{OUT_DIR_A}/fs_1khz.jpeg")]:
    xx, tt = cosgen2(A, f, phi, t_start, dur, fs)
    print(f" fs={fs}  samples={len(xx)}  tt[0]={tt[0]} tt[-1]={tt[-1]}")
    print(f"  xx[:5]={xx[:5]}")
    # Create figure similar to MATLAB Figure 1 screenshot (1600x900 ~ 16:9)
    # Use high DPI to match pixel dimensions
    fig_w, fig_h = 16, 9  # inches
    dpi = 100
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    # Plot line matching MATLAB
    ax.plot(tt, xx, color=MATLAB_BLUE, linewidth=0.9, antialiased=True)
    # Also plot markers? Original plots have continuous line only, no markers
    # Axis limits: replicate MATLAB auto behaviour
    # For fs=1kHz alternating -10,10 expect ylim -10..10
    # Use same xlim as MATLAB: t_start to t_start+dur
    ax.set_xlim(t_start, t_start+dur)
    # MATLAB auto y expansion: for this signal symmetric, keep -10..10 with margin
    ax.set_ylim(-10.5, 10.5)
    ax.set_yticks([-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10])
    # X ticks: MATLAB shows -5,0,5,10 with x1e-3 exponent
    ax.set_xticks([-5e-3, 0, 5e-3, 10e-3])
    ax.set_xticklabels(['-5', '0', '5', '10'])
    # Axis labels style: add exponent annotation like original screenshots show "x10^-3"
    # Use figure text at bottom right near axis
    # Add offset text manually
    # Tight layout
    ax.tick_params(labelsize=9, length=4, width=0.8)
    ax.grid(False)
    # Add x10^-3 notation at bottom right (like MATLAB's offset)
    fig.text(0.885, 0.08, r'$\times 10^{-3}$', fontsize=9, ha='center', va='bottom')
    # Add title? Original MATLAB figures had no title, just axes
    # Save as JPEG to match existing (quality 95)
    # Use tight_bbox but keep space for exponent
    plt.subplots_adjust(left=0.08, right=0.97, top=0.92, bottom=0.15)
    fig.savefig(fname, dpi=dpi, format='jpeg', pil_kwargs={'quality': 95})
    plt.close(fig)
    print(f"  Saved {fname} ({os.path.getsize(fname)} bytes)")

# Also verify and print expected values for report
print("\nPart A fs comparison:")
for fs in [10000, 1000, 800, 500]:
    xx, tt = cosgen2(A, f, phi, t_start, dur, fs)
    alias = abs(f - round(f/fs)*fs) if fs!=0 else f
    # alias freq minimal <= fs/2
    # More accurate alias calc: map to Nyquist zone
    # For reporting: f_alias = |f - k*fs| where k=round(f/fs) then if >fs/2 fold?
    # Simpler: Nyquist = fs/2
    nyq = fs/2
    k = int(np.floor(f/fs+0.5))
    f_alias_simple = abs(f - k*fs)
    if f_alias_simple > nyq:
        f_alias_simple = fs - f_alias_simple
    print(f" fs={fs:5d}  N={len(xx):3d}  samp/period={fs/f:4.1f}  Nyq={nyq:5.0f}  alias≈{f_alias_simple:6.1f} Hz  status={'OK (>Nyq)' if fs>2*f else 'CRITICAL (=Nyq)' if fs==2*f else 'ALIASED'}  y_unique={np.unique(np.round(xx,6))[:6]}")

# === 2. Prelab plots ===
print("\nGenerating prelab3.m plots...")

def generate_prelab(n, out_path, title_suffix=""):
    N1, N2, N3 = 64, 128, 256
    x = np.cos(2*np.pi*n/10)
    # Compute FFT magnitudes
    X1 = np.abs(np.fft.fft(x, N1))
    X2 = np.abs(np.fft.fft(x, N2))
    X3 = np.abs(np.fft.fft(x, N3))
    F1 = np.arange(N1)/N1
    F2 = np.arange(N2)/N2
    F3 = np.arange(N3)/N3
    fig, axs = plt.subplots(3, 1, figsize=(10, 7), dpi=150, sharex=False)
    # MATLAB subplot style: white background, blue line with x markers
    for ax, F, X, N in [(axs[0], F1, X1, N1), (axs[1], F2, X2, N2), (axs[2], F3, X3, N3)]:
        ax.plot(F, X, color=MATLAB_BLUE, linewidth=1.0, marker='x', markersize=4, markeredgewidth=0.8, markevery=1)
        ax.set_title(f'N = {N}', fontsize=11, pad=8)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 30)
        ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticks([0, 10, 20, 30])
        ax.tick_params(labelsize=9, length=3)
        ax.grid(False)
    # MATLAB axis labels: frequency axis normalized 0..1 (0 to 1/N scale), magnitude
    # Add common xlabel/ylabel to mimic? Original had no labels, just axis
    fig.text(0.5, 0.02, 'Normalized frequency', ha='center', fontsize=10)
    fig.text(0.02, 0.5, 'Magnitude |X[k]|', va='center', rotation='vertical', fontsize=10)
    plt.subplots_adjust(left=0.08, right=0.97, top=0.93, bottom=0.09, hspace=0.5)
    if title_suffix:
        fig.suptitle(title_suffix, fontsize=10, y=0.98)
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f" Saved {out_path}  ({os.path.getsize(out_path)} bytes)")
    # Print peaks for caption
    for N, X in [(64,X1),(128,X2),(256,X3)]:
        peak=np.max(X)
        idx=np.argmax(X)
        # Also symmetric peak on other side (~1 - f)
        print(f"   N={N:3d} peak={peak:.2f} at bin {idx} (F={idx/N:.4f})")

# Original: n=0:29 (30 samples)
n30 = np.arange(0, 30)
generate_prelab(n30, f"{OUT_DIR_P}/prelab3_n30_N64_128_256.jpeg", title_suffix="prelab3.m — n = [0:29] (30 samples, 10 per period)")
# Extended: n=0:59 (60 samples)
n60 = np.arange(0, 60)
generate_prelab(n60, f"{OUT_DIR_P}/prelab3_n60_N64_128_256.jpeg", title_suffix="prelab3.m — n = [0:59] (60 samples, 10 per period)")

# Also generate combined comparison PNGs with transparent bg for report use
print("\nAlso saving PNG versions for LaTeX/report...")
for name in ["prelab3_n30_N64_128_256", "prelab3_n60_N64_128_256"]:
    src = f"{OUT_DIR_P}/{name}.jpeg"
    # JPEG already saved, also export PNG copy
    import shutil
    # We'll regenerate as PNG for lossless report embedding
    # Already have JPEG; create PNG duplicate by converting via PIL
    from PIL import Image
    im = Image.open(src)
    dst = f"{OUT_DIR_P}/{name}.png"
    im.save(dst)
    print(f"  PNG {dst}")

print("\nDone. Files generated:")
for root,_,files in os.walk(OUT_DIR_A):
    for f in files: print(os.path.join(root,f))
for root,_,files in os.walk(OUT_DIR_P):
    for f in files: print(os.path.join(root,f))

