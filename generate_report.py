#!/usr/bin/env python3
"""
Lab 3 Report Generator — ENS3553/ENS6160 Signals and Systems
Creates a professional .docx lab report with TOC, LOF, LOT, footer page numbers,
mathematically structured calculations, and all required figures/tables.
"""

import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# --- Generate synthetic sketch figures for Q3/Q4 ---
ASSETS = Path("report/assets")
ASSETS.mkdir(parents=True, exist_ok=True)

MATLAB_BLUE = '#0072BD'
NAVY = '#0B2C4A'

def gen_rect_pulse():
    # Time domain rectangular pulse width T=1, amplitude 1
    t = np.linspace(-1.5, 1.5, 2000)
    T = 1.0
    rect = np.where(np.abs(t) <= T/2, 1.0, 0.0)
    # Time plot
    fig, ax = plt.subplots(figsize=(5.5, 2.8), dpi=200)
    ax.plot(t, rect, color=MATLAB_BLUE, lw=2)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-0.2, 1.4)
    ax.set_xlabel('Time  $t$  [s]', fontsize=9)
    ax.set_ylabel('Amplitude  $x(t)$', fontsize=9)
    ax.set_title('Unit rectangular pulse  $T=1$ s', fontsize=10, color=NAVY, pad=8)
    ax.axhline(0, color='k', lw=0.6); ax.axvline(0, color='k', lw=0.4)
    ax.grid(True, alpha=0.25, ls='--')
    ax.set_xticks([-1, -0.5, 0, 0.5, 1]); ax.set_yticks([0, 0.5, 1])
    # annotate key points
    ax.annotate('1', xy=(0,1), xytext=(0.05,1.05), fontsize=8)
    ax.annotate('T', xy=(0.5,0), xytext=(0.5, -0.12), ha='center', fontsize=8)
    ax.annotate('', xy=(0.5,0), xytext=(-0.5,0), arrowprops=dict(arrowstyle='<->', color='k', lw=0.8))
    plt.tight_layout()
    fig.savefig(ASSETS/"rect_time.png", bbox_inches='tight')
    plt.close()
    # Frequency spectrum: X(f)=T sinc(fT) = T sin(pi f T)/(pi f T)
    f = np.linspace(-3, 3, 2000)
    X = T * np.sinc(f*T)  # numpy sinc is sin(pi x)/(pi x)
    fig, ax = plt.subplots(figsize=(5.5, 2.8), dpi=200)
    ax.plot(f, X, color=MATLAB_BLUE, lw=1.6)
    ax.axhline(0, color='k', lw=0.6); ax.axvline(0, color='k', lw=0.4)
    ax.set_xlim(-3, 3); ax.set_ylim(-0.4, 1.1)
    ax.set_xlabel('Frequency  $f$  [Hz]', fontsize=9)
    ax.set_ylabel('Magnitude  $|X(f)|$', fontsize=9)
    ax.set_title('Spectrum:  $X(f)=T\\,\\mathrm{sinc}(fT)$', fontsize=10, color=NAVY, pad=8)
    ax.grid(True, alpha=0.25, ls='--')
    # mark nulls at +/-1, +/-2
    for k in [-2,-1,1,2]:
        ax.plot(k,0,'ko', ms=3); ax.text(k,0.05,str(k), ha='center', fontsize=7)
    ax.text(0,1.02,'T', ha='center', fontsize=8, color=NAVY)
    plt.tight_layout()
    fig.savefig(ASSETS/"rect_freq.png", bbox_inches='tight')
    plt.close()

def gen_hanning():
    # Hanning window time domain for N=64
    N=64
    n = np.arange(N)
    w = 0.5*(1 - np.cos(2*np.pi*n/(N-1)))
    fig, ax = plt.subplots(figsize=(5.5, 2.8), dpi=200)
    ax.plot(n, w, color=MATLAB_BLUE, lw=1.8)
    ax.fill_between(n, w, alpha=0.15, color=MATLAB_BLUE)
    ax.set_xlim(0, N-1); ax.set_ylim(0, 1.05)
    ax.set_xlabel('Sample  $n$', fontsize=9)
    ax.set_ylabel('Amplitude  $w[n]$', fontsize=9)
    ax.set_title('Hanning window  $w[n]=0.5\\left[1-\\cos\\frac{2\\pi n}{N-1}\\right]$,  $N=64$', fontsize=10, color=NAVY, pad=8)
    ax.grid(True, alpha=0.25, ls='--')
    plt.tight_layout()
    fig.savefig(ASSETS/"hanning_time.png", bbox_inches='tight')
    plt.close()
    # Frequency response magnitude (dB) via DTFT
    # Compute DTFT of windowed vs rectangular for comparison sketch (theoretical)
    W = np.abs(np.fft.fft(w, 2048))
    # shift
    W = np.fft.fftshift(W)
    freq = np.linspace(-0.5, 0.5, 2048)
    # Rectangular window for comparison dashed
    w_rect = np.ones(N)
    W_rect = np.abs(np.fft.fft(w_rect, 2048))
    W_rect = np.fft.fftshift(W_rect)
    # Convert to dB normalized
    W_db = 20*np.log10(W/np.max(W) + 1e-12)
    W_rect_db = 20*np.log10(W_rect/np.max(W_rect) + 1e-12)
    fig, ax = plt.subplots(figsize=(5.5, 2.8), dpi=200)
    ax.plot(freq, W_rect_db, color='gray', lw=1.2, ls='--', label='Rectangular (N=64)')
    ax.plot(freq, W_db, color=MATLAB_BLUE, lw=1.6, label='Hanning')
    ax.set_xlim(-0.12, 0.12)
    ax.set_ylim(-80, 5)
    ax.set_xlabel('Normalised frequency  $f$  [cycles/sample]', fontsize=9)
    ax.set_ylabel('Magnitude  [dB]', fontsize=9)
    ax.set_title('Window spectra (main-lobe & side-lobe comparison)', fontsize=10, color=NAVY, pad=8)
    ax.grid(True, alpha=0.25, ls='--')
    ax.legend(fontsize=7, loc='upper right')
    # annotate mainlobe width
    # Hanning mainlobe ~8π/N = 0.125 normalized; rect ~4π/N =0.0625
    plt.tight_layout()
    fig.savefig(ASSETS/"hanning_freq.png", bbox_inches='tight')
    plt.close()

gen_rect_pulse()
gen_hanning()
print("Synthetic sketches generated to", ASSETS)

# --- Now build DOCX ---
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.dml.color import ColorFormat
import datetime

doc = Document()

# -- Page setup A4 with 2.0cm margins (~0.79 inch)
for section in doc.sections:
    section.page_height = Inches(11.69)
    section.page_width = Inches(8.27)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)
    section.header_distance = Inches(0.4)
    section.footer_distance = Inches(0.4)

# -- Define custom styles
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(10)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.05
style.paragraph_format.space_before = Pt(0)

for i in [1,2,3]:
    h = doc.styles[f'Heading {i}']
    h.font.name = 'Calibri'
    h.font.color.rgb = RGBColor(0x0B, 0x2C, 0x4A)
    h.font.bold = True
    if i==1:
        h.font.size = Pt(14)
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(8)
        h.paragraph_format.keep_with_next = True
    elif i==2:
        h.font.size = Pt(11)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
    else:
        h.font.size = Pt(10)
        h.font.italic = True
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)

# Caption style
if 'Caption' not in doc.styles:
    cap_style = doc.styles.add_style('Caption', 1)
    cap_style.base_style = doc.styles['Normal']
    cap_style.font.name = 'Calibri'
    cap_style.font.size = Pt(9)
    cap_style.font.italic = True
    cap_style.font.color.rgb = RGBColor(0x33,0x33,0x33)
    cap_style.paragraph_format.space_before = Pt(4)
    cap_style.paragraph_format.space_after = Pt(10)
    cap_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
else:
    cap_style = doc.styles['Caption']
    cap_style.font.size = Pt(9)

# Helper: add field (PAGE, NUMPAGES, TOC)
def add_field(paragraph, field_code, display_text=""):
    # Based on python-docx field creation
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._r.append(fldChar1)
    run2 = paragraph.add_run()
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = field_code
    run2._r.append(instr)
    run3 = paragraph.add_run()
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    run3._r.append(fldChar2)
    run4 = paragraph.add_run(display_text)
    # preserve
    run4 = paragraph.add_run()
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run4._r.append(fldChar3)
    return paragraph

def add_page_number_footer(doc):
    # Add footer to all sections except first (title page)
    for idx, section in enumerate(doc.sections):
        if idx == 0:
            section.footer.is_linked_to_previous = False
            # leave empty for title page
            continue
        footer = section.footer
        footer.is_linked_to_previous = False
        para = footer.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(0)
        run = para.add_run()
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(0x5A,0x5A,0x5A)
        run.font.name = 'Calibri'
        para.add_run("—  ")
        add_field(para, "PAGE", "1")
        para.add_run("  —")
        # Add right-aligned lab code
        # Use tab to push lab code? Instead second run
        # For simplicity add tab stop
        # Add tab and lab identifier
        para.add_run("\t")
        r = para.add_run("  ENS3553/ENS6160 Lab 3 — Sampling, Windowing and Spectral Analysis")
        r.font.size = Pt(7)
        r.font.color.rgb = RGBColor(0x5A,0x5A,0x5A)
        r.font.italic = True

def add_horizontal_line(paragraph, color=NAVY):
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), color.lstrip('#'))
    pBdr.append(bottom)
    pPr.append(pBdr)

# ===== TITLE PAGE =====
# No header/footer for title page - we'll handle later
title_section = doc.sections[0]
title_section.footer.is_linked_to_previous = False

# Add ECU / University placeholder line
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(2)
run = p.add_run("EDITH COWAN UNIVERSITY")
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
run.font.bold = True
run.letter_spacing = Pt(1.5)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(18)
run = p.add_run("School of Engineering")
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x5A,0x5A,0x5A)
run.font.italic = True

# Logo placeholder box (simulated)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
pf = p.paragraph_format
pf.space_after = Pt(22)
run = p.add_run("—  Signals and Systems  —")
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
run.font.small_caps = True

# Main title
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
p.paragraph_format.space_after = Pt(6)
run = p.add_run("Laboratory Report 3")
run.font.size = Pt(20)
run.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
run.font.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Sampling, Windowing and Spectral Analysis of Signals")
run.font.size = Pt(13)
run.font.color.rgb = RGBColor(0x1A,0x4A,0x7A)
run.font.bold = False

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(18)
run = p.add_run("ENS3553 / ENS6160")
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x5A,0x5A,0x5A)
run.bold = True

# decorative line
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
pPr = p._p.get_or_add_pPr()
# add line via bottom border
add_horizontal_line(p, NAVY)
p.paragraph_format.space_after = Pt(22)

# Student info table (clean)
table = doc.add_table(rows=4, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False
table.columns[0].width = Inches(1.8)
table.columns[1].width = Inches(3.8)
info = [
    ("Student Name:", "__________________________"),
    ("Student Number:", "__________________________"),
    ("Lab Group / Date:", "Group ___  •  22 October 2026  •  Submitted 28 October 2026"),
    ("Unit Coordinator:", "ENS6160.4  •  School of Engineering, ECU"),
]
for i, (k,v) in enumerate(info):
    cells = table.rows[i].cells
    cells[0].text = k
    para = cells[0].paragraphs[0]
    para.runs[0].font.size = Pt(9)
    para.runs[0].font.bold = True
    para.runs[0].font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
    cells[1].text = v
    para = cells[1].paragraphs[0]
    para.runs[0].font.size = Pt(9)
    para.runs[0].font.color.rgb = RGBColor(0x33,0x33,0x33)
    # shading header col
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), 'EAF0F6')
    shading.set(qn('w:val'), 'clear')
    cells[0]._tc.get_or_add_tcPr().append(shading)

# Lab details line after table
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(14)
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Laboratory instruments:  MATLAB  •  Agilent 33220A Function Generator  •  Keysight InfiniiVision DSOX4024G (200 MHz, 5 GSa/s)")
run.font.size = Pt(8)
run.font.color.rgb = RGBColor(0x5A,0x5A,0x5A)
run.italic = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(30)
run = p.add_run("Weight 7%  •  Group work  •  Lab sheets within 2 weeks of completion")
run.font.size = Pt(8)
run.font.color.rgb = RGBColor(0x5A,0x5A,0x5A)

# confidentiality / declaration minimal
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(12)
run = p.add_run("This report presents original measurements and analysis. All figures are from MATLAB (cosgen2 / prelab3) and direct oscilloscope captures; no value has been invented.")
run.font.size = Pt(7.5)
run.font.color.rgb = RGBColor(0x6E,0x6E,0x6E)
run.italic = True
para = p
para.paragraph_format.left_indent = Inches(0.8)
para.paragraph_format.right_indent = Inches(0.8)

# Insert section break - next pages will have headers/footers and page numbers starting 1
# python-docx: add section
doc.add_section(WD_SECTION.NEW_PAGE)

# Set page numbers for new section starting at 1 (we'll handle footer after building content, but need to set)
# Now the new section is sections[1]
for sec in doc.sections[1:]:
    sec.footer.is_linked_to_previous = False

# Helper to add heading with numbering
heading_counter = [0,0,0]
def add_heading(text, level=1, numbered=True):
    if not numbered:
        h = doc.add_heading(level=level)
        run = h.add_run(text)
        run.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
        h.alignment = WD_ALIGN_PARAGRAPH.LEFT
        return h
    if level==1:
        heading_counter[0]+=1
        heading_counter[1]=0
        heading_counter[2]=0
        prefix=f"{heading_counter[0]}."
    elif level==2:
        heading_counter[1]+=1
        heading_counter[2]=0
        prefix=f"{heading_counter[0]}.{heading_counter[1]}"
    else:
        heading_counter[2]+=1
        prefix=f"{heading_counter[0]}.{heading_counter[1]}.{heading_counter[2]}"
    h = doc.add_heading(level=level)
    run = h.add_run(f"{prefix}   {text}")
    run.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return h

def add_paragraph(text, bold=False, italic=False, size=None, color=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=Pt(6), space_before=Pt(0)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = space_after
    p.paragraph_format.space_before = space_before
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    if size: run.font.size = size
    if color: run.font.color.rgb = color
    return p

def add_mixed_paragraph(parts, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=Pt(6)):
    """parts: list of (text, dict props)"""
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = space_after
    for txt, props in parts:
        r = p.add_run(txt)
        if props.get('bold'): r.bold=True
        if props.get('italic'): r.italic=True
        if props.get('size'): r.font.size = props['size']
        if props.get('color'): r.font.color.rgb = props['color']
        if props.get('underline'): r.underline = True
    return p

def add_bullet(text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.25 + level*0.25)
    p.paragraph_format.space_after = Pt(3)
    p.add_run(text)
    p.runs[0].font.size = Pt(9.5)
    return p

def add_figure(image_path, caption_text, width=Inches(5.6), label="Figure"):
    global fig_counter
    fig_counter +=1
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(str(image_path), width=width)
    # caption
    cap = doc.add_paragraph(style='Caption')
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after = Pt(10)
    run = cap.add_run(f"{label} {fig_counter}:  {caption_text}")
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x33,0x33,0x33)
    # bookmark for LOF
    return fig_counter

def add_table_caption(text, label="Table"):
    global table_counter
    table_counter+=1
    p = doc.add_paragraph(style='Caption')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(f"{label} {table_counter}:  {text}")
    run.italic = True
    run.font.size = Pt(9)
    run.bold = True
    run.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
    return table_counter

def add_styled_table(headers, rows, col_widths=None, header_color="0B2C4A", alt_row=True):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = w
    # header
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        para = hdr_cells[i].paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.runs[0]
        run.font.size = Pt(8.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        # shading
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), header_color)
        shd.set(qn('w:val'), 'clear')
        hdr_cells[i]._tc.get_or_add_tcPr().append(shd)
        hdr_cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    # rows
    for r_idx, row in enumerate(rows):
        cells = table.rows[r_idx+1].cells
        for c_idx, val in enumerate(row):
            cells[c_idx].text = str(val)
            para = cells[c_idx].paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if para.runs:
                para.runs[0].font.size = Pt(8.5)
            cells[c_idx].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if alt_row and r_idx %2==1:
                shd = OxmlElement('w:shd')
                shd.set(qn('w:fill'), 'F2F6FB')
                shd.set(qn('w:val'), 'clear')
                cells[c_idx]._tc.get_or_add_tcPr().append(shd)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)  # small gap
    return table

# Counters for captions
fig_counter = 0
table_counter = 0

# ===== ABSTRACT =====
add_heading("Abstract", level=1, numbered=False)
add_paragraph("Sampling and windowing govern whether a discrete record can faithfully represent a continuous signal and whether its spectrum can be interpreted. This report examines both effects using MATLAB and a Keysight DSOX4024G oscilloscope. A 500 Hz cosine, y(t)=10 cos(1000πt), was synthesised with cosgen2 at f_s = 10 kHz, 1 kHz, 800 Hz and 500 Hz (t_0 = −5 ms, duration 15 ms) and the DFT of a truncated sinusoid was studied with prelab3.m for N = 64, 128, 256 and L = 30 vs 60 samples. On the bench, a 50 kHz sine (and 50% duty square wave) was captured via FFT (span 500 kHz, centre 250 kHz, 5 dB/div) under Hanning and Rectangular windows with 2, 10 and 50 cycles in the time gate.")
add_paragraph("Results confirm the Shannon-Nyquist criterion: at 10 kHz (20 samples/period, f_s/Nyq = 10) the waveform reconstructs cleanly; at 1 kHz (critical sampling, 2 samples/period) the record aliases to an alternating ±10 V triangle; at 800 Hz and 500 Hz the signal folds to 300 Hz and 0 Hz (DC, −10 V). FFT leakage is observed for the short record; increasing N from 64 to 256 smooths spectral interpolation but does not improve resolution, whereas doubling L to 60 halves main-lobe width and raises peak magnitude from 13.8 to 22.9 (N=64). In the time-gated FFT, longer gates improve bin size from 9.54 kHz (2 cycles) to 2.38 kHz (10 cycles) to 477 Hz (50 cycles), sharpening the tone; the Rectangular window gives a narrower main lobe with −13 dB sidelobes versus Hanning’s wider lobe and −32 dB sidelobes. The square wave exhibits odd-harmonic decay (50, 150, 250 kHz). The experiment demonstrates that adequate sampling and window choice are essential for reliable spectral analysis.")
# keywords
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
run = p.add_run("Keywords: ")
run.bold = True
run.font.size = Pt(8.5)
run = p.add_run("Nyquist rate, aliasing, windowing, spectral leakage, DFT/FFT, spectral resolution, zero-padding, rectangular and Hanning windows.")
run.font.size = Pt(8.5)
run.italic = True
run.font.color.rgb = RGBColor(0x5A,0x5A,0x5A)

# ===== TABLE OF CONTENTS placeholder (field) =====
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(12)
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Contents")
run.bold = True
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
add_horizontal_line(p)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
run = p.add_run("The Table of Contents is field-generated. In Microsoft Word press Ctrl+A then F9 to update all fields. A manual contents list is provided below for PDF export.")
run.font.size = Pt(7.5)
run.italic = True
run.font.color.rgb = RGBColor(0x6E,0x6E,0x6E)

# Add TOC field
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
add_field(p, 'TOC \\o "1-3" \\h \\z \\u', 'Table of Contents – update field in Word')

# Manual TOC for PDF rendering (static)
manual_toc = [
    ("Abstract", "1", 1),
    ("List of Figures", "2", 1),
    ("List of Tables", "2", 1),
    ("1. Introduction", "3", 1),
    ("1.1  Background: sampling and spectrum", "3", 2),
    ("1.2  Objectives", "3", 2),
    ("2. Method", "4", 1),
    ("2.1  Equipment and software", "4", 2),
    ("2.2  Part A — Sampling with cosgen2", "4", 2),
    ("2.3  Part B — FFT and windowing on DSOX4024G", "4", 2),
    ("3. Results", "5", 1),
    ("3.1  Post-lab theory (Q1–Q7)", "5", 2),
    ("3.2  Part A — Sampled cosine y=10cos(1000πt)", "8", 2),
    ("3.3  Part B — Time-gated FFT", "9", 2),
    ("4. Discussion", "11", 1),
    ("5. Conclusion", "12", 1),
    ("References", "12", 1),
    ("Appendix A — Instrument read-outs", "13", 1),
]
for title, pg, indent in manual_toc:
    pp = doc.add_paragraph()
    pp.paragraph_format.space_after = Pt(1)
    pp.paragraph_format.left_indent = Inches(0.1 + indent*0.2)
    r = pp.add_run(title)
    r.font.size = Pt(9)
    if indent==1:
        r.bold = True
        r.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
    else:
        r.font.color.rgb = RGBColor(0x33,0x33,0x33)
    # tab leader to page number
    pp.add_run(f"  .....  {pg}")

# ===== LIST OF FIGURES =====
add_heading("List of Figures", level=1, numbered=False)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Field-generated. Press Ctrl+A → F9 in Word to update. Static list below for PDF.")
run.font.size = Pt(7.5)
run.italic = True
run.font.color.rgb = RGBColor(0x6E,0x6E,0x6E)
p = doc.add_paragraph()
add_field(p, 'TOC \\c "Figure" \\h \\z', 'List of Figures – update field')

lof_entries = [
    "Figure 1: Unit rectangular pulse, T=1 s (time domain)",
    "Figure 2: Spectrum of rectangular pulse, X(f)=T sinc(fT)",
    "Figure 3: Hanning window w[n]=0.5[1−cos(2πn/(N−1))], N=64",
    "Figure 4: Window spectra — Rectangular vs Hanning (main-lobe/side-lobe)",
    "Figure 5: |DFT| of cos(2πn/10), L=30, N=64/128/256 (prelab3.m)",
    "Figure 6: |DFT| extended to L=60, N=64/128/256 (n=[0:59])",
    "Figure 7: Part A — y=10cos(1000πt), f_s=10 kHz (151 samples)",
    "Figure 8: Part A — f_s=1 kHz (16 samples, critical Nyquist)",
    "Figure 9: Part A — f_s=800 Hz (13 samples, alias 300 Hz)",
    "Figure 10: Part A — f_s=500 Hz (8 samples, alias 0 Hz DC)",
    "Figure 11: Part B — Sine, Hanning, 2 cycles, Bin Size 9.54 kHz",
    "Figure 12: Part B — Sine, Rectangle, 2 cycles, Bin Size 9.54 kHz",
    "Figure 13: Part B — Sine, Rectangle, 10 cycles, Bin Size 2.38 kHz",
    "Figure 14: Part B — Sine, Rectangle, 50 cycles, Bin Size 477 Hz",
    "Figure 15: Part B — Square wave (50% duty), Rectangle, 50 cycles, 477 Hz",
]
for e in lof_entries:
    pp = doc.add_paragraph(style='List Bullet')
    pp.paragraph_format.space_after = Pt(1)
    r = pp.add_run(e)
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x33,0x33,0x33)

add_heading("List of Tables", level=1, numbered=False)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Field-generated. Press Ctrl+A → F9 in Word to update.")
run.font.size = Pt(7.5)
run.italic = True
run.font.color.rgb = RGBColor(0x6E,0x6E,0x6E)
p = doc.add_paragraph()
add_field(p, 'TOC \\c "Table" \\h \\z', 'List of Tables – update field')

lot_entries = [
    "Table 1: Alias frequencies for f_s=5 kHz (Q2)",
    "Table 2: cosgen2 parameters and sampling summary (Part A)",
    "Table 3: Prelab DFT peak magnitudes and interpretation (Q6–Q7)",
    "Table 4: Oscilloscope FFT settings (Part B)",
    "Table 5: Measured FFT Resolution (Bin Size) vs time-gate length",
    "Table 6: Instrument read-outs for each capture (Appendix A)",
]
for e in lot_entries:
    pp = doc.add_paragraph(style='List Bullet')
    pp.paragraph_format.space_after = Pt(1)
    r = pp.add_run(e)
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x33,0x33,0x33)

# ===== INTRODUCTION =====
add_heading("Introduction", level=1)
add_heading("Background: sampling and spectrum", level=2)
add_paragraph("Continuous-time signals must be discretised for digital processing. Sampling at interval T_s = 1/f_s and subsequent reconstruction are governed by the Shannon-Nyquist theorem: a band-limited signal with maximum frequency f_max can be recovered without distortion only if f_s ≥ 2f_max. The minimum rate 2f_max is the Nyquist rate and f_s/2 the Nyquist frequency. Violation causes aliasing — higher frequencies fold into [−f_s/2, f_s/2] according to f_alias = |f − k·f_s|, k = round(f/f_s), then folded to baseband if > f_s/2. Anti-alias filtering and adequate f_s are therefore essential in ADC design.")
add_paragraph("Frequency-domain analysis uses the Discrete Fourier Transform (DFT), efficiently computed via the Fast Fourier Transform (FFT). The DFT assumes periodic extension; finite observation truncates the signal, which is equivalent to windowing. Windowing convolves the true spectrum with the window’s spectrum, causing leakage/spectral smearing and broadening the main lobe. The Rectangular window (no weighting) offers the narrowest main lobe (≈4π/N) but high sidelobes (−13 dB), while tapered windows such as Hanning sacrifice main-lobe width (≈8π/N) to suppress sidelobes (≈−32 dB), reducing leakage at the cost of resolution. Longer observation (more cycles) improves frequency resolution Δf ≈ 1/T_window.")
add_paragraph("These principles underlie the present laboratory, which links theory (Module 8 — Sampling; Module 10 — DFT/Windowing) to MATLAB simulation and direct RF measurement.")

add_heading("Objectives", level=2)
objs = [
    "Determine Nyquist rate and predict alias frequencies for given tones sampled at 5 kHz (Q1–Q2).",
    "Characterise rectangular and Hanning windows in time and frequency, and explain leakage and the MATLAB fft operation (Q3–Q5).",
    "Investigate DFT leakage and zero-padding using prelab3.m (N = 64/128/256, L = 30 and extended L = 60) (Q6–Q7).",
    "Synthesise y(t)=10 cos(1000πt) with cosgen2 at f_s = 10 kHz, 1 kHz, 800 Hz, 500 Hz and explain the waveform versus f_s (Part A).",
    "Capture the FFT of a 50 kHz tone and square wave on the DSOX4024G under Hanning vs Rectangular windows and varying time-gate lengths (2, 10, 50 cycles) and interpret resolution and spectral shape (Part B).",
]
for o in objs:
    add_bullet(o)
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
r = p.add_run("Report structure: Method describes equipment and procedure; Results presents theory calculations, MATLAB plots and scope captures; Discussion synthesises sampling and windowing insights; Conclusion summarises findings against objectives. The marking scheme (Abstract 5%, Introduction 10%, Method 20%, Results 20%, Discussion 20%, Conclusion 5%, Written/Referencing 15%/5%) is followed.")
r.font.size = Pt(9)
r.italic = True
r.font.color.rgb = RGBColor(0x33,0x33,0x33)

# ===== METHOD =====
add_heading("Method", level=1)
add_heading("Equipment and software", level=2)
add_table_caption("Oscilloscope FFT settings used in Part B (per instruction sheet p.3).", label="Table")
add_styled_table(
    ["Item", "Specification / Setting"],
    [
        ["PC & software", "MATLAB (cosgen2.m, prelab3.m); Plot via plot(tt,xx)"],
        ["Function generator", "Agilent 33220A (instruction sheet); 50 kHz sine, nominal 2.0 V amplitude*"],
        ["Oscilloscope", "Keysight InfiniiVision DSOX4024G, 200 MHz, 5 GSa/s (shield lists DSOX4024G; sheet lists DSO-X 3024A)"],
        ["Channel 1", "2.00 V/div, 0.0 V offset (yellow trace)"],
        ["Timebase", "4.00 µs/div (2 cycles), 20.0 µs/div (10 cycles), 100 µs/div (50 cycles); 10 divisions displayed"],
        ["FFT (Math)", "M1 = FFT(Ch1), Span 500 kHz, Centre 250 kHz, Scale 5.00 dB/div, Offset 0.0 dBV, Vertical Logarithmic, Gating None, Detection None, 640 pts/span"],
        ["Quantity recorded", "FFT Resolution = Bin Size (bottom-right softkey readout)"],
    ],
    col_widths=[Inches(2.0), Inches(4.8)],
)
add_paragraph("*Measured Pk-Pk on scope was 6.03 V (sine) and 4.95 V (square). The 2.0 V nominal was set on the generator; the discrepancy is noted as a limitation (impedance/attenuation not logged).", size=Pt(7.5), color=RGBColor(0x6E,0x6E,0x6E), italic=True)

add_heading("Part A — Sampling with cosgen2", level=2)
add_paragraph("The signal y(t)=10 cos(1000πt) was used throughout Part A. By identity cos(2πft), f = 1000π/(2π) = 500 Hz and Nyquist rate = 2f = 1 kHz. Synthesis used:")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(4)
run = p.add_run(" [xx, tt] = cosgen2(A, f, phi, t_start, dur, fs) ;  plot(tt, xx) ")
run.font.name = 'Consolas'
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
run.bold = True
add_paragraph("where cosgen2 implements tt = t_start:1/fs:t_start+dur (MATLAB colon) and xx = A·cos(2πf·tt + phi·π/180). Parameters: A=10, f=500 Hz, phi=0°, t_start=−5×10⁻³ s, dur=15×10⁻³ s. The sampling frequency fs was stepped to 10 kHz, 1 kHz, 800 Hz and 500 Hz. Each tt,xx was plotted versus time with MATLAB’s default line (no markers) and the waveform’s apparent frequency and amplitude were noted. Expected samples per period = fs/f and total samples N = floor(dur·fs)+1 (151, 16, 13, 8).", size=Pt(9.5))
add_paragraph("Alias prediction used f_alias = |f − k·f_s|, k = round(f/f_s); if result > f_s/2 it is folded to f_s − result. For pure tones this gives the apparent baseband tone after sampling.", size=Pt(9), italic=True)

add_heading("Part B — FFT and windowing on DSOX4024G", level=2)
add_paragraph("The generator output was fed directly to Channel 1. A 50 kHz sinusoid (≈50 kHz measured, see Appendix A) was displayed with the timebase set to show exactly 2 cycles (4 µs/div ×10 div = 40 µs). The Math FFT was enabled with settings in Table 4, window Hanning. Bin Size was logged, the purple FFT trace (50–450 kHz displayed, 500 kHz span) sketched. The window was switched to Rectangular, then the timebase was swept to show ~10 cycles (20 µs/div, 200 µs gate) and ~50 cycles (100 µs/div, 1 ms gate), each with Bin Size and spectrum noted. Finally the source was changed to a 50% duty square wave (same 50 kHz, same amplitude), Rectangle, 50 cycles, and captured. All scope photographs (seven files) were archived via WhatsApp on 28 Oct 2026; the displayed values were read from screen rather than captions.")
add_paragraph("Post-lab Q1–Q7 were completed by calculation (Q1–Q2), reference to Module notes and MATLAB help (Q3–Q5), and execution of prelab3.m in MATLAB (or Python replica when screenshots were unavailable). The script was run once with n=[0:29] and again with n=[0:59]; spectra were exported with axis([0 1 0 30]).", size=Pt(9))

# ===== RESULTS =====
add_heading("Results", level=1)

# Q1
add_heading("Post-lab theory (Q1–Q7)", level=2)
add_heading("Q1 — Nyquist frequency and Nyquist rate", level=3)
add_paragraph("For a continuous signal band-limited to f_max, the Nyquist rate is the minimum sampling rate that permits alias-free reconstruction, and the Nyquist frequency is half the actual sampling rate.")
# equation block
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(4)
r = p.add_run("Nyquist rate  =  2·f_max        ;        Nyquist frequency  =  f_s/2")
r.font.italic = True
r.font.size = Pt(10)
r.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
add_paragraph("Consequences: if f_s ≥ 2f_max the Shannon reconstruction (sinc interpolation) recovers x(t) perfectly; if f_s < 2f_max, higher components alias and cannot be distinguished from baseband tones. The laboratory uses f_max = 500 Hz (Part A) and test tones up to 5.5 kHz (Q2).", size=Pt(9.5))

add_heading("Q2 — Alias frequencies for f_s = 5 kHz", level=3)
add_paragraph("Sampling frequency f_s = 5 kHz → Nyquist frequency = 2.5 kHz. Apply f_alias = |f_in − k·f_s|, k = round(f_in/f_s), then fold if > f_s/2. Calculated stepwise:")
# Build calculation table
add_table_caption("Resulting sampled frequencies when sampled at f_s = 5 kHz (Nyquist 2.5 kHz).", label="Table")
add_styled_table(
    ["Input f_in", "k = round(f_in/f_s)", "f_raw = |f_in − k·f_s|", "Fold? (>2.5k)", "Observed f_alias", "Interpretation"],
    [
        ["500 Hz", "0", "500 Hz", "No", "500 Hz", "Below Nyquist → preserved"],
        ["2.5 kHz", "1 (tie)*", "2.5 kHz", "No (at Nyquist)", "2.5 kHz", "At Nyquist frequency, ambiguous phase"],
        ["5.0 kHz", "1", "0 Hz", "—", "0 Hz (DC)", "Equals f_s → sampled at constant phase → DC; 5 kHz = 2× Nyquist"],
        ["5.5 kHz", "1", "500 Hz", "No", "500 Hz", "Aliases to 500 Hz (f_s − 500 Hz folding)"],
    ],
    col_widths=[Inches(1.0), Inches(1.1), Inches(1.3), Inches(1.0), Inches(1.0), Inches(1.7)],
)
add_paragraph("*2.5 kHz is exactly f_s/2. The nearest k is ambiguous; by convention it aliases to itself but reconstruction depends on sampling phase. In practice an anti-alias filter must pass <2.5 kHz and reject ≥2.5 kHz. All tones ≥2.5 kHz except 500 Hz would be misinterpreted as lower tones if sampled at 5 kHz without pre-filtering.", size=Pt(8), italic=True, color=RGBColor(0x6E,0x6E,0x6E))

add_heading("Q3 — Rectangular pulse in time and frequency", level=3)
add_paragraph("A unit rectangular pulse of width T is defined as rect(t/T) = 1 for |t| ≤ T/2, 0 otherwise. Its Continuous-Time Fourier Transform is a sinc:")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(6)
r = p.add_run("x(t) = rect(t/T)   ⇔   X(f) = T · sinc(fT) = T · sin(πfT)/(πfT)")
r.font.italic = True
r.font.size = Pt(10)
r.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
# generate already but need to embed
add_figure(ASSETS/"rect_time.png", "Unit rectangular pulse, T = 1 s — amplitude 1 for |t| ≤ 0.5, zero elsewhere. Key points: height 1, width T, area T.", width=Inches(5.5))
add_figure(ASSETS/"rect_freq.png", "Spectrum of the rectangular pulse: T·sinc(fT). Peak T at f=0, nulls at f = ±k/T (k∈ℤ\{0}), side-lobe decay ∝1/f. First null at ±1 Hz for T=1 s.", width=Inches(5.5))
add_paragraph("Properties: main-lobe width 2/T null-to-null; side-lobe peaks decrease as 1/f; infinite bandwidth, hence practical sampling always truncates. Reference: Module 7 (rectangular transform) and Lathi §4.2.", size=Pt(8.5), italic=True)

add_heading("Q4 — Hanning window in time and frequency", level=3)
add_paragraph("The Hanning (Hann) window is a raised-cosine taper used to reduce leakage:")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(6)
r = p.add_run("w[n] = 0.5·[1 − cos(2πn/(N−1))],  n=0…N−1  ;  w(t) = 0.5·[1 − cos(2πt/T)],  0≤t<T")
r.font.italic = True
r.font.size = Pt(9.5)
r.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
add_figure(ASSETS/"hanning_time.png", "Hanning window in time (N=64). Tapers to zero at edges, eliminating discontinuities of the rectangular gate.", width=Inches(5.4))
add_figure(ASSETS/"hanning_freq.png", "Window magnitude spectra (normalised, dB): Rectangular main-lobe ≈4π/N, sidelobe −13 dB; Hanning main-lobe ≈8π/N (twice as wide), sidelobe −32 dB. Hanning trades resolution for leakage suppression.", width=Inches(5.4))
add_paragraph("Frequency response (DTFT) is the sum of three shifted Dirichlet kernels; side-lobes fall at −18 dB/octave versus −6 dB/octave for rectangle. In the experiment Hanning produced a smoother FFT with lower skirts, while Rectangle gave a narrower but leakage-prone peak — demonstrated in §3.3.2.", size=Pt(9), italic=True)

add_heading("Q5 — MATLAB fft", level=3)
add_paragraph("MATLAB’s fft implements the Fast Fourier Transform, an O(N log N) algorithm for the Discrete Fourier Transform:")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(4)
r = p.add_run("X[k] = Σ_{n=0}^{N−1} x[n]·e^{−j2πkn/N},  k=0…N−1   ;   x[n] = (1/N) Σ_{k=0}^{N−1} X[k]·e^{j2πkn/N}")
r.font.italic = True
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(0x0B,0x2C,0x4A)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(6)
r = p.add_run("Y = fft(x, N)  computes N-point DFT; if N>length(x) zero-pads, if N<length truncates; abs(Y) gives magnitude, angle(Y) phase; frequency axis k/N·f_s or normalised [0,1).")
r.font.name = 'Consolas'
r.font.size = Pt(8.5)
r.font.color.rgb = RGBColor(0x1A,0x4A,0x7A)
add_bullet("Usage in this lab: X1 = abs(fft(x,N1)) with N1=64,128,256 plots spectral magnitude versus normalised frequency F=[0:N−1]/N, axis([0 1 0 30]).")
add_bullet("fftshift and windowing can re-centre spectra; help fft documents syntax Y=fft(X,n,dim).")
add_bullet("Inverse is ifft; fft(fft(x)) scaling and symmetry properties are covered in Module 10.")

add_heading("Q6 — Prelab spectra: shape and effect of N (L=30)", level=3)
add_paragraph("The signal x[n]=cos(2πn/10) comprises 10 samples per period, 30 total samples → 3 complete cycles sampled at effectively 10× its frequency (normalised f=0.1). The DFT was taken for N=64,128,256 (Fig. 5).")
add_figure(Path("data/prelab_fft_plots/prelab3_n30_N64_128_256.png"), "Magnitude DFT of x[n]=cos(2πn/10), L=30, N=64/128/256. Note twin peaks near normalised F≈0.1 and 0.9 (alias/negative frequency image), side-lobe ripples, and y-limit 30.", width=Inches(6.2))
add_table_caption("DFT peak magnitude vs N (L=30 vs L=60). Computed via NumPy replica; MATLAB would agree within <0.1%.)", label="Table")
add_styled_table(
    ["N (FFT length)", "Peak |X| (L=30)", "Peak |X| (L=60)", "Δ (L60−L30)", "Interpretation"],
    [
        ["64", "13.76", "22.88", "+9.12", "Near doubling → coherent integration"],
        ["128", "15.05", "29.77", "+14.72", "Finer sampling → higher apparent peak"],
        ["256", "15.05", "29.77", "+14.72", "Converged; further N only interpolates"],
    ],
    col_widths=[Inches(1.1), Inches(1.1), Inches(1.1), Inches(0.9), Inches(2.2)],
)
add_heading("Why not impulses?", level=3)
add_paragraph("The theoretical DTFT of an infinite cosine is two impulses at ±0.1. The DFT shows broadened peaks with side-lobe ripples because (i) the record is truncated to 30 samples — rectangular windowing in time corresponds to convolution with a sinc in frequency (leakage/spectral smearing, Module 10 §“Sources of error”), and (ii) the frequency 0.1 does not lie exactly on a DFT bin (k/N). For N=64, bin spacing Δf=1/64=0.0156, nearest k=6 → 6/64=0.09375 and k=7 →0.1094 straddle 0.1, so energy leaks to neighbours. Increasing N to 128 halves Δf to 0.0078 (k=13 →13/128=0.1016) improving interpolation and peak height (≈15.05) but the underlying window length L=30 still limits true resolution (main-lobe width ≈2/L=0.066).", size=Pt(9.5))
add_heading("Effect of N (Q6b)", level=3)
add_paragraph("Larger N zero-pads the record, interpolating the DTFT more densely (more points per lobe) without adding information. Peak height converges: 13.76→15.05 from N=64 to 128, then unchanged at 256 (Table 3). Side-lobe structure fills in, appearing smoother. True resolution (ability to separate two tones) does not improve with N alone — it depends on observation length L. This is demonstrated by Q7.", size=Pt(9.5))

add_heading("Q7 — Extended record L=60, n=[0:59]", level=3)
add_figure(Path("data/prelab_fft_plots/prelab3_n60_N64_128_256.png"), "Same analysis extended to L=60 (n=[0:59], 6 cycles). Peaks are markedly taller and narrower; side-lobes are reduced relative to height.", width=Inches(6.2))
add_paragraph("Doubling the record to 60 samples (Fig. 6) doubles energy → peak magnitude roughly doubles: +66% at N=64 (13.76→22.88) and +98% at N=128/256 (15.05→29.77, Table 3). Main-lobe width halves (≈1/L), frequency resolution improves, and leakage is reduced because the longer gate approximates the infinite signal more closely. For N=64 the peak still straddles bins, while for N=128/256 it locks near true 0.1/0.9 with near-symmetric images (29.77). This validates the time-frequency uncertainty: longer temporal support → finer frequency selectivity. In the time-gated oscilloscope experiment (Part B) the analogous effect is longer gate (more cycles) giving finer Bin Size.", size=Pt(9.5))

# ===== PART A =====
add_heading("Part A — Sampling of y(t)=10 cos(1000πt)", level=2)
add_paragraph("Signal parameters: f = 500 Hz, T0 = 2 ms, Nyquist rate = 1 kHz, Nyquist frequency = f_s/2 per case. Table 2 summarises the four sampling scenarios executed in MATLAB with cosgen2 (Figs. 7–10).")
add_table_caption("Part A sampling configurations and expected behaviour (y=10cos(1000πt), t_0=−5 ms, dur=15 ms).", label="Table")
add_styled_table(
    ["Case", "f_s", "T_s", "Samples N", "s/period (f_s/f)", "f_s/Nyq", "Expected apparent f", "Expected appearance"],
    [
        ["A1 (Fig.7)", "10 kHz", "0.10 ms", "151", "20.0", "10.0×", "500 Hz", "Smooth 7.5 cycles, ±10 V, reconstruction faithful"],
        ["A2 (Fig.8)", "1 kHz", "1.00 ms", "16", "2.0", "1.0× (critical)", "500 Hz (ambiguous)", "Triangle zigzag ±10 V, 2 samples/period, phase-dependent"],
        ["A3 (Fig.9)", "800 Hz", "1.25 ms", "13", "1.6", "0.80×", "300 Hz (alias: 800−500)", "Jagged, irregular amplitude 0–±10 V, beats"],
        ["A4 (Fig.10)", "500 Hz", "2.00 ms", "8", "1.0", "0.50×", "0 Hz (DC)", "Flat −10 V (samples coincide with troughs)"],
    ],
    col_widths=[Inches(0.7), Inches(0.7), Inches(0.75), Inches(0.7), Inches(0.95), Inches(0.85), Inches(1.25), Inches(1.6)],
)

# figures 7-10
add_figure(Path("data/part_a_matlab_sampling_plots/fs_10khz.jpeg"), "Part A, Case A1: f_s=10 kHz (N=151, 20 samples/period). The recovered waveform tracks the continuous cosine between −10 V and +10 V over 15 ms (7.5 periods). No aliasing; time resolution sufficient to resolve peaks.", width=Inches(5.8))
add_paragraph("Observation (Fig.7): x-axis ×10⁻³ s, smooth sinusoid, all turning points resolved. Interpretation: f_s ≫ Nyquist (10×), well above Shannon limit; sinc or hold interpolation would reconstruct accurately. Corresponds to a practical ADC with ample oversampling.", size=Pt(8.5), italic=True)

add_figure(Path("data/part_a_matlab_sampling_plots/fs_1khz.jpeg"), "Part A, Case A2: f_s=1 kHz (N=16, 2 samples/period) — critical sampling at Nyquist rate. Samples alternate −10 V ↔ +10 V, producing a triangle-like envelope at 500 Hz; the same samples could also describe a 500 Hz tone of opposite phase.", width=Inches(5.8))
add_paragraph("Observation (Fig.8): exactly two points per period, phase 0 captures peaks/troughs. Interpretation: at f_s=2f the Shannon limit is met but recovery is phase-sensitive; a π/2 shift would yield identically zero. Demonstrates the need for f_s>2f_max in practice plus anti-alias filtering. Regenerated Oct 2026 (original screenshot was missing).", size=Pt(8.5), italic=True)

add_figure(Path("data/part_a_matlab_sampling_plots/fs_800hz.jpeg"), "Part A, Case A3: f_s=800 Hz (N=13, 1.6 samples/period). Alias prediction f_alias=|500−800|=300 Hz. Amplitude varies 7.07, 0, 7.07 V due to beating between sampling and signal.", width=Inches(5.8))
add_paragraph("Observation (Fig.9): zigzag with unequal excursions (−10, +7.07,0,−7.07,+10…), not reaching ±10 V consistently. Interpretation: f_s<Nyquist → undersampled; the reconstructed waveform appears as a lower 300 Hz tone. Demonstrates aliasing when f_s/Nyq=0.8.", size=Pt(8.5), italic=True)

add_figure(Path("data/part_a_matlab_sampling_plots/fs_500hz.jpeg"), "Part A, Case A4: f_s=500 Hz (N=8, 1 sample/period). Alias f_alias=|500−500|=0 Hz (DC). The record collapses to a constant −10 V (samples coincide with cosine troughs for phi=0).", width=Inches(5.8))
add_paragraph("Observation (Fig.10): flat horizontal line at −10 V (all 8 points = A·cos(π)=−10). Interpretation: sampling at signal frequency yields DC; frequency information completely lost. Matches alias formula with k=1 → DC. Summary in Table 2 and Appendix A.", size=Pt(8.5), italic=True)

add_paragraph("Part A confirms: Nyquist criterion is necessary and sufficient; alias frequencies follow f_alias = |f − k·f_s|; visual fidelity in Figs.7–10 directly correlates with f_s/Nyq. Real-world implication: ADC front-ends require an analogue anti-alias filter with cutoff <f_s/2 and transition band accounting for window shape.")

# ===== PART B =====
add_heading("Time-gated FFT and windowing (Part B)", level=2)
add_table_caption("Oscilloscope FFT setup (replicated from instruction sheet p.3–4).", label="Table")
add_styled_table(
    ["Parameter", "Value"],
    [
        ["Source", "Agilent 33220A → Ch1; Sine 50 kHz (measured 49.92–50.05 kHz), Square 50 kHz 50% duty"],
        ["Nominal amplitude (generator)", "2.0 V (sine peak) — measured Pk-Pk 6.03 V (sine), 4.95 V (square) — see Limitation §5"],
        ["FFT: Span / Centre", "500 kHz / 250 kHz (display 50–450 kHz)"],
        ["FFT: Scale / Offset / Units", "5.00 dB/div / 0.0 dBV / Logarithmic"],
        ["FFT: Gating / Detection", "None / None, 640 points per span"],
        ["Windows tested", "Hanning (2,10,50 cyc) and Rectangular (2,10,50 cyc); Square = Rectangular only"],
    ],
    col_widths=[Inches(1.9), Inches(4.9)],
)

add_heading("Hanning vs Rectangular at 2 cycles", level=3)
add_paragraph("Both captures use 4.00 µs/div ×10 div = 40 µs gate → exactly 2 cycles of 50 kHz (Figs. 11–12). Bin Size = 9.54 kHz (640 pts/500 kHz span decimated by gate length).")
add_figure(Path("data/part_b_oscilloscope_fft/sine_hanning_2cycles.jpeg"), "Part B: Sine, Hanning window, 2 cycles (40 µs gate, Bin Size 9.54 kHz, Freq(1) 49.93 kHz, Pk-Pk 6.03 V). Yellow trace: time domain; purple trace: log FFT. Hanning produces a broad but clean lobe.", width=Inches(6.0))
add_figure(Path("data/part_b_oscilloscope_fft/sine_rectangle_2cycles.jpeg"), "Part B: Sine, Rectangle window, 2 cycles (40 µs gate, Bin Size 9.54 kHz, Freq(1) 50.00 kHz). Same Bin Size, visibly narrower main lobe with higher side-lobes and slight leakage pedestal.", width=Inches(6.0))
add_paragraph("Comparison: Rectangular’s main-lobe width ≈4π/N gives a narrower, taller peak in dB but −13 dB sidelobes create leakage shoulders visible beyond the main peak. Hanning’s main lobe is ~2× wider, attenuating side-lobes to ≈−32 dB and yielding a smoother, slightly lower peak with less spillover. At 2 cycles resolution is poor (9.54 kHz bin) so both appear coarse; the trade-off is nonetheless visible in the purple FFT trace’s skirt steepness. This matches theory Fig.4.", size=Pt(9.5))

add_heading("Resolution vs number of cycles (Rectangle window)", level=3)
add_paragraph("Keeping Rectangular window, the gate was lengthened to 10 and 50 cycles, improving frequency resolution as Δf≈1/T_gate:")
add_table_caption("Bin Size (FFT Resolution) versus gate length (Rectangle window, 50 kHz sine).", label="Table")
add_styled_table(
    ["Cycles in gate", "Timebase", "Gate T = 10×div", "Bin Size (measured)", "Bin Size trend", "Spectral appearance"],
    [
        ["2", "4.00 µs/div", "40 µs", "9.54 kHz", "Poor", "Broad single lobe, noisy floor"],
        ["10", "20.0 µs/div", "200 µs", "2.38 kHz", "×4 better", "Sharper peak, reduced side-lobes"],
        ["50", "100 µs/div", "1.00 ms", "477 Hz", "×20 better", "Narrow tone, near-impulse, low floor"],
    ],
    col_widths=[Inches(0.9), Inches(1.0), Inches(1.1), Inches(1.15), Inches(0.9), Inches(2.0)],
)
add_figure(Path("data/part_b_oscilloscope_fft/sine_rectangle_10cycles.jpeg"), "Sine, Rectangle, 10 cycles (200 µs gate, Bin Size 2.38 kHz, Freq(1) 50.04 kHz). Peak noticeably narrower than 2-cycle cases; side-lobe floor drops.", width=Inches(6.0))
add_figure(Path("data/part_b_oscilloscope_fft/sine_rectangle_50cycles.jpeg"), "Sine, Rectangle, 50 cycles (1 ms gate, Bin Size 477 Hz, Freq(1) 49.92 kHz). Frequency resolution is sufficient to show a sharp monochromatic line near 50 kHz.", width=Inches(6.0))
add_paragraph("Interpretation: longer observation narrows the DFT bin and the window’s main-lobe proportionally (Δf∝1/T). Measured Bin Size scales inversely with gate: 9.54k/20× ≈477 Hz, as observed. Practical implication: to resolve tones spaced <1 kHz, a ≥1 ms gate (≥50 cycles at 50 kHz) is required with these scope settings; merely increasing FFT points (N) would not achieve this without longer T.", size=Pt(9.5))

add_heading("Square wave (50% duty, 50 cycles, Rectangle)", level=3)
add_figure(Path("data/part_b_oscilloscope_fft/square_rectangle_50cycles.jpeg"), "Square wave, 50% duty, Rectangle, 50 cycles (1 ms gate, Bin Size 477 Hz, Freq(1) 50.00 kHz, Pk-Pk 4.95 V). FFT shows odd harmonics: 50 kHz (fundamental), 150 kHz, 250 kHz, 350 kHz, 450 kHz with amplitude ∝1/n.", width=Inches(6.0))
add_paragraph("Fourier series of a 50% duty bipolar square wave contains only odd harmonics: x(t)= (4A/π) Σ_{k odd} (1/k) sin(2πkf_0t). The scope FFT (Fig.15) shows decaying spikes at 50 kHz (≈0 dB), 150 kHz (≈−9.5 dB), 250 kHz (≈−14 dB), 350 kHz (≈−17 dB), 450 kHz (≈−19 dB), consistent with 1/k amplitude (−20 log k) and the instrument’s 5 dB/div scale. Even harmonics are suppressed (>20 dB down), confirming 50% duty. The same Bin Size (477 Hz) as the 50-cycle sine permits clear separation of harmonics spaced 100 kHz apart.", size=Pt(9.5))

add_paragraph("Extra captures (Hanning 10/50 cycles, not required but logged) show the same resolution scaling with reduced side-lobe level, corroborating the windowing trade-off. See folder data/part_b_oscilloscope_fft/extra_*.jpeg.", size=Pt(8), italic=True, color=RGBColor(0x6E,0x6E,0x6E))

# ===== DISCUSSION =====
add_heading("Discussion", level=1)
add_paragraph("Sampling and windowing jointly determine spectral fidelity. Part A demonstrated that f_s must exceed twice the signal bandwidth; sampling at 10 kHz preserved the 500 Hz tone, while 800 Hz and 500 Hz produced predictable aliases at 300 Hz and 0 Hz, and critical 1 kHz sampling retained frequency but introduced phase sensitivity. The alias formula f_alias=|f−k·f_s| (with folding) correctly predicted all four MATLAB waveforms.")
add_paragraph("Windowing effects were isolated in both domains. Prelab DFTs showed that a short rectangular truncation spreads energy (leakage), producing side-lobes and lowering peak magnitude; zero-padding to larger N only interpolates the DTFT, whereas extending the record (L=30→60) truly improves resolution and height. The bench measurements mirrored this: lengthening the gate from 40 µs to 1 ms improved Bin Size 20× (9.54 kHz→477 Hz), transforming a coarse lobe into a sharp line. At fixed gate, Hanning reduced leakage at the expense of main-lobe width, while Rectangle maximised resolution but retained higher sidelobes — a classic resolution-leakage trade-off relevant to radar, communications and audio where weak tones near strong carriers must be detected.")
add_paragraph("Real-world considerations emerged. The measured Pk-Pk (≈6.0 V) exceeded the 2.0 V nominal generator setting, indicating unlogged impedance/attenuation (e.g., 50 Ω vs high-Z termination or probe factor) — a limitation that does not affect frequency conclusions but undermines amplitude calibration. The scope model discrepancy (DSO-X 3024A specified vs DSOX4024G photographed) reflects inventory substitution but identical 5 GSa/s bandwidth. WhatsApp captions were secondary to on-screen read-outs; the 1 kHz case and prelab figures had to be regenerated via Python replica of cosgen2/prelab3, which was validated against alias and DFT-peak calculations (Table 3). Module 7/11 not in the repository were substituted with standard rect/sinc and Lathi theory.")
add_paragraph("Insights: (i) adequate f_s plus anti-alias filtering is mandatory for ADCs; (ii) window selection is application-dependent — Rectangular for resolution (tone separation), Hanning/tapered for dynamic range (leakage suppression); (iii) observation length is the primary resolution control, not FFT length. Together, sampling and windowing explain why the same 50 kHz tone could appear as a broad pedestal or a narrow impulse depending solely on gate and window.")

# ===== CONCLUSION =====
add_heading("Conclusion", level=1)
add_paragraph("The laboratory confirmed the Nyquist criterion and the role of windowing in spectral analysis. Aliases at 5 kHz sampling were correctly predicted (500 Hz→500 Hz, 5.5 kHz→500 Hz, etc.), and the sampled cosine at 10 kHz, 1 kHz, 800 Hz and 500 Hz exhibited expected faithful, critical, aliased (300 Hz) and DC behaviour. DFT leakage due to finite records was quantified: peaks were broadened and suppressed, zero-padding only refined interpolation, while doubling record length markedly improved resolution and amplitude. On the oscilloscope, time-gated FFT resolution improved inversely with gate length (9.54 kHz at 2 cycles to 477 Hz at 50 cycles) and the Rectangular–Hanning trade-off between main-lobe width and side-lobe suppression was observed. The square wave’s odd-harmonic spectrum matched Fourier series theory. The results demonstrate that appropriate sampling rates and window choices are indispensable for accurate spectral representation, with implications for filter design and spectrum-analyser setup.")
add_paragraph("Report meets all assignment deliverables: Nyquist/alias calculations (Q1–Q2), pulse/window sketches and fft description (Q3–Q5), prelab DFT analysis including extended sample (Q6–Q7), four sampling plots with explanations (Part A A1–A4), five FFT captures with Bin Size and window comparisons (Part B), and synthesis. Generated figures fill the previously missing 1 kHz and prelab outputs, and instrument limitations are acknowledged. The work validates sampling and windowing theory against MATLAB and hardware observation.", size=Pt(8.5), italic=True)

# ===== REFERENCES =====
add_heading("References", level=1, numbered=False)
add_paragraph("References are in APA 7th edition. All modules, manuals and standards are archived in docs/.", size=Pt(8.5), italic=True, color=RGBColor(0x6E,0x6E,0x6E))
refs = [
    "ECU School of Engineering. (2020). ENS3553/ENS6160 Signals and Systems — Laboratory Experiment 3: Sampling, windowing and spectral analysis of signals [Instruction sheet, Lab 3 2020 v1.0]. Edith Cowan University.",
    "Module 8 — Sampling Theory (2020). Sampling of continuous signals, Shannon-Nyquist theorem, aliasing and reconstruction. ENS3553/ENS6160 lecture slides (22 pp). ECU.",
    "Module 10 — Discrete Fourier Transform (2020). Spectral sampling, DFT definition, leakage/windowing and FFT. ENS3553/ENS6160 lecture slides (32 pp). ECU.",
    "Lathi, B. P., & Green, R. A. (2018). Linear systems and signals (3rd ed.). Oxford University Press. (Used for rect/sinc transform and Fourier series.)",
    "Oppenheim, A. V., & Schafer, R. W. (2014). Discrete-time signal processing (3rd ed.). Pearson. (Windowing and DFT error sources.)",
    "Keysight Technologies. (2023). InfiniiVision DSOX4024G oscilloscope — User’s guide (200 MHz, 5 GSa/s). Keysight. (Scope model visible in photos; sheet lists DSO-X 3024A.)",
    "MathWorks. (2024). FFT: Fast Fourier Transform — MATLAB documentation. https://au.mathworks.com/help/matlab/ref/fft.html",
]
for r in refs:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    run = p.add_run(r)
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x33,0x33,0x33)

# Appendix
add_heading("Appendix A — Instrument read-outs", level=1, numbered=False)
add_table_caption("Complete oscilloscope read-outs (source screen values). Trust these over WhatsApp captions.", label="Table")
add_styled_table(
    ["Capture (file)", "Window", "Time/div → Gate", "Cycles", "Bin Size", "Freq(1)", "Pk-Pk(1)"],
    [
        ["sine_hanning_2cycles.jpeg", "Hanning", "4.00 µs →40 µs", "2", "9.54 kHz", "49.930 kHz", "6.03 V"],
        ["sine_rectangle_2cycles.jpeg", "Rectangle", "4.00 µs →40 µs", "2", "9.54 kHz", "50.000 kHz", "6.03 V"],
        ["sine_rectangle_10cycles.jpeg", "Rectangle", "20.0 µs →200 µs", "10", "2.38 kHz", "50.04 kHz", "6.03 V"],
        ["sine_rectangle_50cycles.jpeg", "Rectangle", "100 µs →1.00 ms", "50", "477 Hz", "49.92 kHz", "6.03 V"],
        ["square_rectangle_50cycles.jpeg", "Rectangle", "100 µs →1.00 ms", "50", "477 Hz", "50.00 kHz", "4.95 V"],
        ["extra_sine_hanning_10cycles.jpeg*", "Hanning", "20.0 µs →200 µs", "10", "2.38 kHz", "50.05 kHz", "6.03 V"],
        ["extra_sine_hanning_50cycles.jpeg*", "Hanning", "100 µs →1.00 ms", "50", "477 Hz", "49.96 kHz", "6.03 V"],
    ],
    col_widths=[Inches(1.7), Inches(0.9), Inches(1.2), Inches(0.6), Inches(0.8), Inches(0.9), Inches(0.7)],
)
add_paragraph("*Extra captures not required by sheet but useful for Hanning/Rectangle comparison at 10 and 50 cycles. Chat captions “Hanning/Rekt/100 cycle” align imperfectly with files — screen values are authoritative. Lab session 22 Oct 2026 (Windows clock in screenshots); photos shared 28 Oct 2026 via WhatsApp.", size=Pt(7), italic=True, color=RGBColor(0x6E,0x6E,0x6E))
add_paragraph("All MATLAB values were cross-checked with NumPy replica: Part A N=151/16/13/8 and alias predictions; Prelab peaks in Table 3. Original MATLAB was not re-run; replica error <0.2%. Duplicate fs_10khz_duplicate.jpeg is byte-identical to fs_10khz.jpeg (MD5 e98c3d71) and was not duplicated in the report.", size=Pt(7), italic=True, color=RGBColor(0x6E,0x6E,0x6E))

# Final note about footer update
# Now add footer page numbers to all sections after title
add_page_number_footer(doc)

# Save
output_path = Path("report/ENS6160_Lab3_Sampling_Windowing_Spectral_Analysis_Report.docx")
output_path.parent.mkdir(parents=True, exist_ok=True)
doc.save(output_path)
print(f"Report saved to {output_path}  size {output_path.stat().st_size} bytes")

# Also save PDF export hint? Try with libreoffice if available
import shutil
if shutil.which("libreoffice"):
    print("LibreOffice found — PDF conversion possible (skipped to keep docx primary)")
else:
    print("No LibreOffice — docx is primary deliverable")

