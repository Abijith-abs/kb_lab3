# kb_lab3 — Signals and Systems, Lab 3: Sampling, Windowing and Spectral Analysis

> **Read this first (written for AI assistants and humans).** This repository is a student's working folder for one university lab. It contains **no application code, no build, no tests**. It is: assignment documents, lecture slides, two MATLAB files, and photos/screenshots of the data collected in the lab. The final deliverable (a lab report / completed result sheet) is **not yet in the repo**.

## 1. Quick facts

| Item | Value |
|---|---|
| Course | ENS3553 / ENS6160 Signals and Systems (LMS page shows "ENS6160.4") |
| Assignment | Laboratory 3: Sampling, Windowing and Spectral Analysis of Signals |
| Weight / type | 7 %, group work, no word limit (from `docs/assignment/lms_assignment_page.jpeg`) |
| Due | Lab sheets within 2 weeks of lab completion; pre-lab questions may be done after the lab (same screenshot) |
| Topics | Sampling, Nyquist rate, aliasing, windowing (Hanning vs Rectangle), spectral resolution, DFT/FFT |
| Tools | MATLAB; function generator (33220A); Keysight InfiniiVision **DSOX4024G** oscilloscope in the photos (the instruction sheet says "DSO-X 3024A") |
| Language | MATLAB only (`.m`) |
| Lab session date | MATLAB screenshots show a Windows clock of **22/10/2026**; photo files were shared via WhatsApp on 28 Oct 2026 |
| Git history | One commit ("Add files via upload"); files were later reorganised (see section 8 for old → new names) |

## 2. Repository layout

```
kb_lab3/
├── README.md                                   ← this file
├── matlab/
│   ├── cosgen2.m                               cosine generator used in Part A
│   └── prelab3.m                               FFT / zero-padding demo used in the post-lab
├── docs/
│   ├── assignment/
│   │   ├── lab3_instruction_sheet.pdf          the task: post-lab Qs + Part A + Part B (4 pp)
│   │   ├── lab3_result_sheet_template.docx     blank answer sheet to fill in
│   │   ├── lab_marking_scheme.pdf              report structure + marking rubric (3 pp)
│   │   └── lms_assignment_page.jpeg            screenshot of the LMS assignment page
│   └── lecture_slides/
│       ├── module_08_sampling_theory.pdf       sampling, Nyquist, aliasing, reconstruction (22 pp)
│       └── module_10_discrete_fourier_transform.pdf   DFT, windowing/leakage, FFT (32 pp)
└── data/
    ├── part_a_matlab_sampling_plots/           MATLAB figures of cosgen2 output at different fs
    ├── part_b_oscilloscope_fft/                oscilloscope photos: waveform + FFT, windows, cycle counts
    └── chat_screenshots/                       WhatsApp screenshots whose captions label the photos
```

## 3. How the files connect

```
lab3_instruction_sheet.pdf  (defines every task)
 ├─ Post-lab Q1-2, Q5      ─ theory ◄── module_08 (Nyquist, aliasing), MATLAB help
 ├─ Post-lab Q3-4          ─ theory ◄── Module 7 (NOT in repo), module_10 (windowing)
 ├─ Post-lab Q6-7          ─ run ─► matlab/prelab3.m ─► figures (NOT in repo)
 ├─ Part A  Sampling       ─ run ─► matlab/cosgen2.m ─► data/part_a_matlab_sampling_plots/
 └─ Part B  FFT/windowing  ─ lab bench (function generator + scope) ─► data/part_b_oscilloscope_fft/
                                         ▲ captions in data/chat_screenshots/ label these photos
All results + explanations go into ─► lab3_result_sheet_template.docx
The written report is graded by    ─► lab_marking_scheme.pdf
```

| Result-sheet section | Code / data that feeds it | Theory behind it |
|---|---|---|
| Post-lab Q1-2 (Nyquist frequency; 500 Hz, 2.5 kHz, 5 kHz, 5.5 kHz sampled at 5 kHz) | none | `module_08` (Nyquist rate, aliasing formula) |
| Post-lab Q3-4 (rect pulse spectrum, Hanning window) | none | Module 7 (missing), `module_10` |
| Post-lab Q5 (`fft`) | none | MATLAB `help fft`, `module_10` |
| Post-lab Q6-7 (prelab output, N = 64/128/256, then `n = [0:59]`) | `matlab/prelab3.m` | `module_10` (spectral sampling, resolution, leakage) |
| Part A: fs = 10 kHz, 1 kHz, 800 Hz, 500 Hz | `matlab/cosgen2.m`, `data/part_a_matlab_sampling_plots/` | `module_08` |
| Part B: Hanning vs Rectangle, 2 cycles | `sine_hanning_2cycles`, `sine_rectangle_2cycles` | `module_10` |
| Part B: Rectangle, 10 and 50 cycles (resolution) | `sine_rectangle_10cycles`, `sine_rectangle_50cycles` | `module_10` |
| Part B: 50 % duty square wave | `square_rectangle_50cycles` | `module_10`, Fourier series (slide 3 of `module_10`) |
| Discussion of experimental results | all of the above | all |

## 4. What the lab asks (summary of `lab3_instruction_sheet.pdf`)

- **Post-lab (theory, answered on the result sheet):** Nyquist frequency; aliased frequencies for four inputs sampled at 5 kHz; sketches of a rectangular pulse and a Hanning window with spectra; explain MATLAB `fft`; run `prelab3.m` and explain the spectrum shape and the effect of N; change to `n = [0:59]` and explain the change in shape and height.
- **Part A, Sampling of a signal (MATLAB):** with `cosgen2`, generate `y = 10 cos(1000πt)`, start time −5×10⁻³ s, duration 15×10⁻³ s, at fs = 10 kHz, then 1 kHz, 800 Hz, 500 Hz, and explain what each plot looks like and why. The sheet's hint call is `[xx tt] = cosgen2(10, 500, 0, -5e-3, 15e-3, 1e4); plot(tt, xx)`.
- **Part B, FFT and windowing (oscilloscope):** 50 kHz sine, 2.0 V amplitude from the function generator into Channel 1. FFT: span 500 kHz, centre 250 kHz, 5 dB/div, offset 0 dBV. Record the "FFT Resolution" and sketch the spectrum for: Hanning @ 2 cycles; Rectangle @ 2, 10 and 50 cycles; then a 50 % duty-cycle square wave (Rectangle, 50 cycles). Explain the differences.
- **Final:** a discussion of how sampling and windowing affect spectral analysis.

## 5. File-by-file reference

### 5.1 `matlab/`

| File | What it is |
|---|---|
| `cosgen2.m` | `function [xx, tt] = cosgen2(A, f, phi, t_start, dur, fs)`. Returns a cosine `xx = A*cos(2*pi*f*tt + phi*pi/180)` on time base `tt = t_start : 1/fs : t_start+dur`. `phi` is in **degrees**. If `fs` is omitted it defaults to `50*f` (50 samples per period). Function name must equal the file name. Quirks: the comment on line 14 says "20 samples per period" but the default is 50; the instruction sheet calls the 5th argument `duration`, the file calls it `dur`. |
| `prelab3.m` | Script. Builds `x = cos(2*pi*n/10)` for `n = 0:29` (30 samples, 10 per period), takes `abs(fft(x, N))` for N = 64, 128, 256, builds normalised frequency axes `[0:N-1]/N`, and plots the three spectra in a 3×1 `subplot` with `axis([0 1 0 30])`. The post-lab asks to run it, then change line 2 to `n = [0:59]` and run again. Independent of `cosgen2.m`. |

For expected numbers (checked with an equivalent NumPy computation; MATLAB itself was not run): with N = 64 the spectral peak is about 13.8 for 30 samples and about 22.9 for 60 samples, against a fixed y-axis limit of 30.

### 5.2 `docs/assignment/`

| File | What it is |
|---|---|
| `lab3_instruction_sheet.pdf` | Official lab handout ("Lab 3 2020 v1.0"). Prerequisites, objectives, post-lab questions, equipment, Part A, Part B, discussion. |
| `lab3_result_sheet_template.docx` | **Blank** result sheet (name / student-number fields empty). Sections: Post-lab answers; Sampling of a signal (four plots); FFT and windowing (five spectra, each with an "FFT resolution =" field); discussion. |
| `lab_marking_scheme.pdf` | Required report structure: title page, abstract (200-400 words), table of contents, introduction, method, results, discussion, conclusion (~200 words), references (APA). Weights: Abstract 5 %, Introduction 10 %, Method 20 %, Results 20 %, Discussion 20 %, Conclusion 5 %, Written skills 15 %, Referencing 5 %. |
| `lms_assignment_page.jpeg` | Phone screenshot of the LMS page: weight, group, deadline wording, list of the five assignment files and two support-reading PDFs. |

### 5.3 `docs/lecture_slides/`

| File | What it covers | Used for |
|---|---|---|
| `module_08_sampling_theory.pdf` | Sampling of continuous signals, Shannon-Nyquist theorem and Nyquist rate, aliasing (incl. the alias-frequency formula), anti-alias filtering, reconstruction (zero-order hold, sinc interpolation). | Post-lab Q1-2, Part A |
| `module_10_discrete_fourier_transform.pdf` | Recap of Fourier series/transform, spectral sampling, DFT definition, sources of error (aliasing, truncation/leakage "spectral smearing", windowing), worked 8·rect(t) DFT example, DFT properties, FFT. | Post-lab Q4-7, Part B |

The instruction sheet also cites **Module 7** (rectangular pulse transform) and **Module 11**, and "Lecture 10 on Sampling Theory"; those numbers do not line up cleanly with the two decks included here, and Modules 7 and 11 are not in the repo.

### 5.4 `data/part_a_matlab_sampling_plots/` (MATLAB figure screenshots of `cosgen2` output)

All show `y = 10cos(1000πt)` plotted against time (x axis in ×10⁻³ s; the exponent is cut off in the first screenshot). Sample values below are from the plots and a NumPy recomputation.

| File | fs | What the figure shows |
|---|---|---|
| `fs_10khz.jpeg` | 10 kHz | Smooth cosine between −10 and +10, about 7 peaks, 151 samples. |
| `fs_10khz_duplicate.jpeg` | 10 kHz | Byte-identical copy of `fs_10khz.jpeg` (same MD5). Safe to delete. |
| `fs_800hz.jpeg` | 800 Hz | Jagged zigzag through −10, 7.07, 0, −7.07, 10, … (13 samples); peaks do not reach the true amplitude every time. |
| `fs_500hz.jpeg` | 500 Hz | A flat horizontal line at −10 (all 8 samples equal −10). |
| *(missing)* | 1 kHz | Part A step 3 asks for it; **no screenshot is in the repo**. |

### 5.5 `data/part_b_oscilloscope_fft/` (photos of the Keysight scope)

Every photo shows Channel 1 (yellow time-domain trace, 2.00 V/div) plus an FFT trace `M1 = FFT(Ch1)` with: Scale 5.00 dB/div, Offset 0.0 dBV, Vertical Units Logarithmic, FFT Gating None, Detection Type None, 640 points per span, frequency axis labelled 50.0k … 450kHz (500 kHz span, 250 kHz centre). The on-screen "Bin Size" readout (bottom right, above the softkeys) appears to be what the sheet calls "FFT Resolution".

| File | Signal | Window | Time/div | Cycles shown | Bin size | Meas Freq(1) | Pk-Pk(1) | Result-sheet slot |
|---|---|---|---|---|---|---|---|---|
| `sine_hanning_2cycles.jpeg` | sine | Hanning | 4.000 µs | ~2 | 9.54 kHz | 49.930 kHz | 6.03 V | Hanning, 2 cycles |
| `sine_rectangle_2cycles.jpeg` | sine | Rectangle | 4.000 µs | ~2 | 9.54 kHz | 50.000 kHz | 6.03 V | Rectangle, 2 cycles |
| `sine_rectangle_10cycles.jpeg` | sine | Rectangle | 20.00 µs | ~10 | 2.38 kHz | 50.04 kHz | 6.03 V | Rectangle, 10 cycles (portrait photo, also shows the bench wiring) |
| `sine_rectangle_50cycles.jpeg` | sine | Rectangle | 100.0 µs | ~50 | 477 Hz | 49.92 kHz | 6.03 V | Rectangle, 50 cycles |
| `square_rectangle_50cycles.jpeg` | square wave | Rectangle | 100.0 µs | ~50 | 477 Hz | 50.00 kHz | 4.95 V | Square wave; FFT shows decaying spikes near 50, 150, 250, 350, 450 kHz |
| `extra_sine_hanning_10cycles.jpeg` | sine | Hanning | 20.00 µs | ~10 | 2.38 kHz | 50.05 kHz | 6.03 V | Not requested by the sheet (extra comparison) |
| `extra_sine_hanning_50cycles.jpeg` | sine | Hanning | 100.0 µs | ~50 | 477 Hz | 49.96 kHz | 6.03 V | Not requested by the sheet (extra comparison) |

"Cycles shown" = 10 horizontal divisions × time/div × 50 kHz. Window, time/div, bin size, frequency and Pk-Pk were read off the scope displays in the photos.

### 5.6 `data/chat_screenshots/`

Screenshots of the WhatsApp conversation in which the photos were forwarded. They matter only because the message captions label the photos: "Hanning", "Rectangular", "Windowing action rectangle", "Hanning", "100 cycle", "Rectangular change", "Square rectangular fft". They also show thumbnails of the MATLAB plots sent just before the scope photos. The caption-to-photo pairing is not exact, so trust the settings read off each scope photo (section 5.5) over the captions. The "100 cycle" caption does not match any lab step (the sheet uses 50 cycles).

## 6. Known gaps and inconsistencies

1. `fs = 1 kHz` MATLAB plot (Part A step 3) is missing.
2. No output figures from `prelab3.m` (N = 64/128/256, nor the `n = [0:59]` version).
3. Post-lab written answers, sketches (rect pulse, Hanning window) and the completed result sheet / report are not in the repo; the `.docx` is a blank template.
4. Module 7 and Module 11 slides, cited by the instruction sheet, are not included.
5. `fs_10khz_duplicate.jpeg` is a byte-identical duplicate.
6. The instruction sheet specifies 2.0 V amplitude, but the scope reads Pk-Pk 6.03 V (sine) and 4.95 V (square); the actual generator settings are not recorded anywhere in the repo.
7. The instruction sheet lists a "DSO-X 3024A" scope; the photos show a DSOX4024G.
8. `cosgen2.m` has a stale comment on line 14 (says 20 samples per period; default is 50).

## 7. Guidance for AI assistants working in this repo

- Treat this as coursework with a clear output: **the lab report / result sheet**, structured per `lab_marking_scheme.pdf`. Help with explanation, checking, structuring, formatting and figures.
- **Do not invent measurements.** Use values readable in `data/` or ask. When asked to describe a photo, read the scope settings on screen (section 5.5) rather than relying on the file name or WhatsApp caption.
- To run Part A: put `matlab/` on the MATLAB path (so `cosgen2` resolves), then e.g. `[xx, tt] = cosgen2(10, 500, 0, -5e-3, 15e-3, 1e4); plot(tt, xx)`, repeating with `1e3`, `800`, `500` as the last argument.
- To run the pre-lab: `run('matlab/prelab3.m')`. For the extended-sample step, edit the first computation line to `n = [0:59];`.
- The `.m` files were uploaded as `.txt` and have been renamed to `.m`; the originals' content is unchanged.
- The `.docx` template is the authoritative layout for answers; the PDF marking scheme is the authoritative layout for the written report.

## 8. Original → current file names

| Original name | Current path |
|---|---|
| `cosgen2.m.txt` | `matlab/cosgen2.m` |
| `prelab3-1 (1).m.txt` | `matlab/prelab3.m` |
| `Microsoft Word - Lab 3 2020 v1.0.docx.pdf` | `docs/assignment/lab3_instruction_sheet.pdf` |
| `Lab 3 result sheet _11807348.docx` | `docs/assignment/lab3_result_sheet_template.docx` |
| `Labs Marking Scheme-2_12182152.pdf` | `docs/assignment/lab_marking_scheme.pdf` |
| `WhatsApp Image 2026-10-28 at 7.37.05 PM.jpeg` | `docs/assignment/lms_assignment_page.jpeg` |
| `Microsoft PowerPoint - Signals and Systems Module 8 slides.pptx.pdf` | `docs/lecture_slides/module_08_sampling_theory.pdf` |
| `Slide 1.pdf` | `docs/lecture_slides/module_10_discrete_fourier_transform.pdf` |
| `WhatsApp Image 2026-10-28 at 7.36.59 PM (1).jpeg` | `data/part_a_matlab_sampling_plots/fs_10khz.jpeg` |
| `WhatsApp Image 2026-10-28 at 7.37.00 PM (1).jpeg` | `data/part_a_matlab_sampling_plots/fs_10khz_duplicate.jpeg` |
| `WhatsApp Image 2026-10-28 at 7.37.00 PM.jpeg` | `data/part_a_matlab_sampling_plots/fs_800hz.jpeg` |
| `WhatsApp Image 2026-10-28 at 7.36.59 PM.jpeg` | `data/part_a_matlab_sampling_plots/fs_500hz.jpeg` |
| `WhatsApp Image 2026-10-28 at 7.37.05 PM (1).jpeg` | `data/part_b_oscilloscope_fft/sine_hanning_2cycles.jpeg` |
| `WhatsApp Image 2026-10-28 at 7.37.01 PM.jpeg` | `data/part_b_oscilloscope_fft/sine_rectangle_2cycles.jpeg` |
| `WhatsApp Image 2026-10-28 at 7.37.03 PM.jpeg` | `data/part_b_oscilloscope_fft/sine_rectangle_10cycles.jpeg` |
| `WhatsApp Image 2026-10-28 at 7.37.04 PM.jpeg` | `data/part_b_oscilloscope_fft/sine_rectangle_50cycles.jpeg` |
| `WhatsApp Image 2026-10-28 at 7.37.04 PM (1).jpeg` | `data/part_b_oscilloscope_fft/square_rectangle_50cycles.jpeg` |
| `WhatsApp Image 2026-10-28 at 7.37.03 PM (1).jpeg` | `data/part_b_oscilloscope_fft/extra_sine_hanning_10cycles.jpeg` |
| `WhatsApp Image 2026-10-28 at 7.37.03 PM (2).jpeg` | `data/part_b_oscilloscope_fft/extra_sine_hanning_50cycles.jpeg` |
| `Screenshot 2026-10-28 194137.png` | `data/chat_screenshots/chat_1_matlab_thumbnails_then_hanning_rectangular.png` |
| `Screenshot 2026-10-28 194200.png` | `data/chat_screenshots/chat_2_windowing_action_hanning_100cycle.png` |
| `Screenshot 2026-10-28 194219.png` | `data/chat_screenshots/chat_3_square_rectangular_fft.png` |
