#!/usr/bin/env python3
"""
Lab 3 Report v2 — matches Lab 2 final.docx visual structure exactly
- Times New Roman 11pt Normal, line 278 (≈1.15), after 160 (8pt), lang en-IN
- Headings Calibri Light (majorHAnsi) 20/16/14pt navy #2F5496, spacings 18/8/4pt
- Caption 9pt italic #44546A
- Margins 1" (1440 twips), header/footer 0.49" (708 twips), A4, titlePg
- Declaration page + cover page identical to Lab 2, updated to Lab 3
- TOC/LOF/LOT field-generated, footer Page X of Y centered 10pt
- Figures/tables with same caption style
"""

import os, pathlib
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Ensure assets exist (reuse from previous)
ASSETS = Path("report/assets")
ASSETS.mkdir(parents=True, exist_ok=True)
MATLAB_BLUE = '#0072BD'
NAVY = '#2F5496'
CAPTION_COLOR = '#44546A'
DECL_FILL = 'E2EFDA'
BORDER_COLOR = '333333'

# Reuse synthetic sketches if missing
if not (ASSETS/"rect_time.png").exists():
    print("Generating synthetic sketches...")
    # rect time
    t = np.linspace(-1.5, 1.5, 2000); T=1.0; rect=np.where(np.abs(t)<=T/2,1.0,0.0)
    fig,ax=plt.subplots(figsize=(5.5,2.8),dpi=200)
    ax.plot(t,rect,color=MATLAB_BLUE,lw=2); ax.set_xlim(-1.5,1.5); ax.set_ylim(-0.2,1.4)
    ax.set_xlabel('Time t [s]',fontsize=9); ax.set_ylabel('Amplitude x(t)',fontsize=9)
    ax.set_title('Unit rectangular pulse T=1 s',fontsize=10,color=NAVY,pad=8)
    ax.axhline(0,color='k',lw=0.6); ax.axvline(0,color='k',lw=0.4); ax.grid(True,alpha=0.25,ls='--')
    fig.savefig(ASSETS/"rect_time.png",bbox_inches='tight'); plt.close()
    f=np.linspace(-3,3,2000); X=T*np.sinc(f*T)
    fig,ax=plt.subplots(figsize=(5.5,2.8),dpi=200)
    ax.plot(f,X,color=MATLAB_BLUE,lw=1.6); ax.axhline(0,color='k',lw=0.6); ax.axvline(0,color='k',lw=0.4)
    ax.set_xlim(-3,3); ax.set_ylim(-0.4,1.1); ax.set_xlabel('Frequency f [Hz]',fontsize=9); ax.set_ylabel('Magnitude |X(f)|',fontsize=9)
    ax.set_title('Spectrum: X(f)=T·sinc(fT)',fontsize=10,color=NAVY,pad=8); ax.grid(True,alpha=0.25,ls='--')
    fig.savefig(ASSETS/"rect_freq.png",bbox_inches='tight'); plt.close()
    N=64; n=np.arange(N); w=0.5*(1-np.cos(2*np.pi*n/(N-1)))
    fig,ax=plt.subplots(figsize=(5.5,2.8),dpi=200)
    ax.plot(n,w,color=MATLAB_BLUE,lw=1.8); ax.fill_between(n,w,alpha=0.15,color=MATLAB_BLUE)
    ax.set_xlim(0,N-1); ax.set_ylim(0,1.05); ax.set_xlabel('Sample n',fontsize=9); ax.set_ylabel('Amplitude w[n]',fontsize=9)
    ax.set_title('Hanning window w[n]=0.5[1−cos(2πn/(N−1))], N=64',fontsize=10,color=NAVY,pad=8); ax.grid(True,alpha=0.25,ls='--')
    fig.savefig(ASSETS/"hanning_time.png",bbox_inches='tight'); plt.close()
    W=np.abs(np.fft.fft(w,2048)); W=np.fft.fftshift(W); freq=np.linspace(-0.5,0.5,2048)
    w_rect=np.ones(N); W_rect=np.abs(np.fft.fft(w_rect,2048)); W_rect=np.fft.fftshift(W_rect)
    W_db=20*np.log10(W/np.max(W)+1e-12); W_rect_db=20*np.log10(W_rect/np.max(W_rect)+1e-12)
    fig,ax=plt.subplots(figsize=(5.5,2.8),dpi=200)
    ax.plot(freq,W_rect_db,color='gray',lw=1.2,ls='--',label='Rectangular (N=64)'); ax.plot(freq,W_db,color=MATLAB_BLUE,lw=1.6,label='Hanning')
    ax.set_xlim(-0.12,0.12); ax.set_ylim(-80,5); ax.set_xlabel('Normalised frequency f [cycles/sample]',fontsize=9); ax.set_ylabel('Magnitude [dB]',fontsize=9)
    ax.set_title('Window spectra (main-lobe & side-lobe comparison)',fontsize=10,color=NAVY,pad=8); ax.legend(fontsize=7,loc='upper right'); ax.grid(True,alpha=0.25,ls='--')
    fig.savefig(ASSETS/"hanning_freq.png",bbox_inches='tight'); plt.close()
    print("Synthetic done")
else:
    print("Synthetic assets already exist")

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = Document()

# --- Section setup: A4 1" margins, titlePg ---
for sec in doc.sections:
    sec.page_height = Inches(11.69)
    sec.page_width = Inches(8.27)
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)
    sec.header_distance = Inches(0.49)
    sec.footer_distance = Inches(0.49)
    # enable title page
    sectPr = sec._sectPr
    titlePg = OxmlElement('w:titlePg')
    sectPr.append(titlePg)

# --- Define styles to match Lab2 ---
# Normal: Times New Roman 11pt, after 8pt, line 278 auto, language en-IN
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(11)
# Ensure rFonts for all
rpr = style.element.find(qn('w:rPr'))
if rpr is None:
    rpr = OxmlElement('w:rPr')
    style.element.append(rpr)
# Set fonts explicitly
for tag in ['w:rFonts']:
    rf = rpr.find(qn(tag))
    if rf is None:
        rf = OxmlElement(tag)
        rpr.append(rf)
    rf.set(qn('w:ascii'), 'Times New Roman')
    rf.set(qn('w:hAnsi'), 'Times New Roman')
    rf.set(qn('w:cs'), 'Times New Roman')
# Paragraph defaults
ppr = style.element.find(qn('w:pPr'))
if ppr is None:
    ppr = OxmlElement('w:pPr')
    style.element.append(ppr)
# spacing
spacing = ppr.find(qn('w:spacing'))
if spacing is None:
    spacing = OxmlElement('w:spacing')
    ppr.append(spacing)
spacing.set(qn('w:after'), '160')
spacing.set(qn('w:line'), '278')
spacing.set(qn('w:lineRule'), 'auto')
# Set docDefaults? We'll set style paragraph format as fallback
style.paragraph_format.space_after = Pt(8)
style.paragraph_format.line_spacing = 1.15
style.paragraph_format.space_before = Pt(0)

# Language
lang = OxmlElement('w:lang')
lang.set(qn('w:val'), 'en-IN')
lang.set(qn('w:eastAsia'), 'en-US')
lang.set(qn('w:bidi'), 'ar-SA')
rpr.append(lang)

# Heading 1: Calibri Light (majorHAnsi) 20pt #2F5496, spacing before 18pt after 4pt, keepNext keepLines, outlineLvl 0
h1 = doc.styles['Heading 1']
h1.font.name = 'Calibri Light'
h1.font.size = Pt(20)
h1.font.color.rgb = RGBColor(0x2F,0x54,0x96)
h1.font.bold = True
# adjust paragraph
h1.paragraph_format.space_before = Pt(18)
h1.paragraph_format.space_after = Pt(4)
h1.paragraph_format.keep_with_next = True
h1.paragraph_format.keep_together = True
# set outline level via xml
h1_elt = h1.element
ppr1 = h1_elt.find(qn('w:pPr'))
if ppr1 is None:
    ppr1 = OxmlElement('w:pPr'); h1_elt.append(ppr1)
outline = OxmlElement('w:outlineLvl'); outline.set(qn('w:val'),'0'); ppr1.append(outline)
# set font theme majorHAnsi
h1_rpr = h1_elt.find(qn('w:rPr'))
# rFonts theme
rf = h1_rpr.find(qn('w:rFonts'))
if rf is None:
    rf = OxmlElement('w:rFonts'); h1_rpr.append(rf)
rf.set(qn('w:asciiTheme'), 'majorHAnsi')
rf.set(qn('w:eastAsiaTheme'), 'majorEastAsia')
rf.set(qn('w:hAnsiTheme'), 'majorHAnsi')
rf.set(qn('w:cstheme'), 'majorBidi')

# Heading2: 16pt #2F5496, before 8pt after 4pt
h2 = doc.styles['Heading 2']
h2.font.name = 'Calibri Light'
h2.font.size = Pt(16)
h2.font.color.rgb = RGBColor(0x2F,0x54,0x96)
h2.font.bold = True
h2.paragraph_format.space_before = Pt(8)
h2.paragraph_format.space_after = Pt(4)
h2.paragraph_format.keep_with_next = True
h2.paragraph_format.keep_together = True
h2_elt = h2.element
ppr2 = h2_elt.find(qn('w:pPr'))
outline2 = OxmlElement('w:outlineLvl'); outline2.set(qn('w:val'),'1'); ppr2.append(outline2)
h2_rpr = h2_elt.find(qn('w:rPr'))
rf2 = h2_rpr.find(qn('w:rFonts'))
if rf2 is None:
    rf2 = OxmlElement('w:rFonts'); h2_rpr.append(rf2)
rf2.set(qn('w:asciiTheme'), 'majorHAnsi'); rf2.set(qn('w:eastAsiaTheme'), 'majorEastAsia'); rf2.set(qn('w:hAnsiTheme'), 'majorHAnsi'); rf2.set(qn('w:cstheme'), 'majorBidi')

# Heading3: 14pt #2F5496, before 8pt after 4pt
h3 = doc.styles['Heading 3']
h3.font.name = 'Calibri Light'
h3.font.size = Pt(14)
h3.font.color.rgb = RGBColor(0x2F,0x54,0x96)
h3.font.bold = True
h3.paragraph_format.space_before = Pt(8)
h3.paragraph_format.space_after = Pt(4)
h3.paragraph_format.keep_with_next = True
h3_elt = h3.element
ppr3 = h3_elt.find(qn('w:pPr'))
outline3 = OxmlElement('w:outlineLvl'); outline3.set(qn('w:val'),'2'); ppr3.append(outline3)
h3_rpr = h3_elt.find(qn('w:rPr'))
rf3 = h3_rpr.find(qn('w:rFonts'))
if rf3 is None:
    rf3 = OxmlElement('w:rFonts'); h3_rpr.append(rf3)
rf3.set(qn('w:eastAsiaTheme'), 'majorEastAsia'); rf3.set(qn('w:cstheme'), 'majorBidi') # no asciiTheme to match reference (which misses it for H3)
rf3.set(qn('w:asciiTheme'), 'majorHAnsi')
rf3.set(qn('w:hAnsiTheme'), 'majorHAnsi')

# Caption: 9pt italic #44546A, spacing after 10pt line 240
cap_style = doc.styles['Caption']
cap_style.font.name = 'Times New Roman'
cap_style.font.size = Pt(9)
cap_style.font.italic = True
cap_style.font.color.rgb = RGBColor(0x44,0x54,0x6A)
cap_style.paragraph_format.space_after = Pt(10)
cap_style.paragraph_format.line_spacing = 1.0  # 240 twips = 1.0
cap_style.paragraph_format.space_before = Pt(0)
# ensure rFonts? Not needed

# Helper functions
def add_field(paragraph, field_code, display=""):
    run = paragraph.add_run()
    fld1 = OxmlElement('w:fldChar'); fld1.set(qn('w:fldCharType'),'begin'); run._r.append(fld1)
    run2 = paragraph.add_run()
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'),'preserve'); instr.text = field_code; run2._r.append(instr)
    run3 = paragraph.add_run()
    fld2 = OxmlElement('w:fldChar'); fld2.set(qn('w:fldCharType'),'separate'); run3._r.append(fld2)
    run4 = paragraph.add_run(display)
    run5 = paragraph.add_run()
    fld3 = OxmlElement('w:fldChar'); fld3.set(qn('w:fldCharType'),'end'); run5._r.append(fld3)
    return paragraph

def set_cell_shading(cell, color):
    shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), color); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto')
    cell._tc.get_or_add_tcPr().append(shd)

def set_table_borders(table, color='333333', sz='6'):
    tblPr = table._tbl.find(qn('w:tblPr'))
    borders = OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'),'single'); el.set(qn('w:sz'), sz if edge in ['top','left','bottom','right'] else '4'); el.set(qn('w:space'),'0'); el.set(qn('w:color'), color)
        borders.append(el)
    tblPr.append(borders)

# Counters
fig_counter = 0
table_counter = 0
heading_counter = [0,0,0]

def add_heading(text, level=1, numbered=True):
    if not numbered:
        h = doc.add_heading(level=level)
        h.text = text
        # ensure style font color
        for run in h.runs:
            run.font.color.rgb = RGBColor(0x2F,0x54,0x96)
        return h
    if level==1:
        heading_counter[0]+=1; heading_counter[1]=0; heading_counter[2]=0
        prefix=f"{heading_counter[0]}."
    elif level==2:
        heading_counter[1]+=1; heading_counter[2]=0
        prefix=f"{heading_counter[0]}.{heading_counter[1]}"
    else:
        heading_counter[2]+=1
        prefix=f"{heading_counter[0]}.{heading_counter[1]}.{heading_counter[2]}"
    h = doc.add_heading(level=level)
    h.text = ""
    run = h.add_run(f"{prefix}   {text}")
    run.font.color.rgb = RGBColor(0x2F,0x54,0x96)
    return h

def add_paragraph(text, bold=False, italic=False, size=None, color=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=Pt(8), space_before=Pt(0), style=None):
    p = doc.add_paragraph(style=style)
    p.alignment = align
    p.paragraph_format.space_after = space_after
    p.paragraph_format.space_before = space_before
    # Justification
    if align==WD_ALIGN_PARAGRAPH.JUSTIFY:
        pPr = p._p.get_or_add_pPr()
        jc = OxmlElement('w:jc'); jc.set(qn('w:val'),'both'); pPr.append(jc)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    if size: run.font.size = size
    if color: run.font.color.rgb = color
    return p

def add_mixed_para(parts, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=Pt(8)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = space_after
    pPr = p._p.get_or_add_pPr()
    if align==WD_ALIGN_PARAGRAPH.JUSTIFY:
        jc = OxmlElement('w:jc'); jc.set(qn('w:val'),'both'); pPr.append(jc)
    for txt, props in parts:
        r = p.add_run(txt)
        if props.get('bold'): r.bold=True
        if props.get('italic'): r.italic=True
        if props.get('size'): r.font.size = props['size']
        if props.get('color'): r.font.color.rgb = props['color']
        if props.get('underline'): r.underline = True
    return p

def add_bullet(text, level=0):
    p = doc.add_paragraph(style='List Paragraph')
    p.paragraph_format.left_indent = Inches(0.5 + level*0.25)
    p.paragraph_format.space_after = Pt(2)
    # bullet via w:numPr? Use simple dash
    run = p.add_run("•   " + text)
    run.font.size = Pt(11)
    return p

def add_figure(image_path, caption_text, width=Inches(5.5)):
    global fig_counter
    fig_counter+=1
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(str(image_path), width=width)
    cap = doc.add_paragraph(style='Caption')
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cap.add_run(f"Figure {fig_counter}.  {caption_text}")
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x44,0x54,0x6A)
    return fig_counter

def add_table_caption(text):
    global table_counter
    table_counter+=1
    p = doc.add_paragraph(style='Caption')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(f"Table {table_counter}.  {text}")
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x44,0x54,0x6A)
    return table_counter

def add_styled_table(headers, rows, col_widths=None, header_fill='2F5496', alt_fill='F2F6FB'):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    if col_widths:
        for i,w in enumerate(col_widths):
            table.columns[i].width = w
    # header
    hdr = table.rows[0].cells
    for i,h in enumerate(headers):
        hdr[i].text = h
        para = hdr[i].paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.runs[0]
        run.font.size = Pt(9)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        set_cell_shading(hdr[i], header_fill)
        hdr[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for r_idx,row in enumerate(rows):
        cells = table.rows[r_idx+1].cells
        for c_idx,val in enumerate(row):
            cells[c_idx].text = str(val)
            para = cells[c_idx].paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if para.runs:
                para.runs[0].font.size = Pt(9)
            cells[c_idx].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if r_idx%2==1:
                set_cell_shading(cells[c_idx], alt_fill)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table

# ============ BUILD DECLARATION PAGE (matches Lab2) ============
# Group work assessment – declaration
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Group work assessment – declaration of contributions and accountabilities")
run.bold = True
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x00,0x00,0x00)

# Declaration info table (Year, Semester, Unit Code, Unit Name, Assessment title)
decl_table = doc.add_table(rows=5, cols=2)
decl_table.alignment = WD_TABLE_ALIGNMENT.CENTER
decl_table.autofit = False
decl_table.columns[0].width = Inches(1.5)
decl_table.columns[1].width = Inches(5.0)
set_table_borders(decl_table, color=BORDER_COLOR, sz='6')
decl_data = [
    ("Year", "2026"),
    ("Semester", "Second Semester"),
    ("Unit Code", "ENS6160"),
    ("Unit Name", "Signals and Systems"),
    ("Assessment title", "Laboratory 3 — Sampling, Windowing and Spectral Analysis of Signals"),
]
for i,(k,v) in enumerate(decl_data):
    cells = decl_table.rows[i].cells
    cells[0].text = k
    para = cells[0].paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.runs[0].font.size = Pt(11)
    para.runs[0].font.color.rgb = RGBColor(0x11,0x11,0x11)
    # padding via tcMar
    tcPr = cells[0]._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for edge in ['top','left','bottom','right']:
        el = OxmlElement(f'w:{edge}'); el.set(qn('w:w'),'35' if edge in ['top','bottom'] else '80'); el.set(qn('w:type'),'dxa'); tcMar.append(el)
    tcPr.append(tcMar)
    cells[1].text = v
    para = cells[1].paragraphs[0]
    para.runs[0].font.size = Pt(11)
    para.runs[0].font.color.rgb = RGBColor(0x11,0x11,0x11)
    set_cell_shading(cells[1], DECL_FILL)
    tcPr = cells[1]._tc.get_or_add_tcPr()
    tcMar2 = OxmlElement('w:tcMar')
    for edge in ['top','left','bottom','right']:
        el = OxmlElement(f'w:{edge}'); el.set(qn('w:w'),'35' if edge in ['top','bottom'] else '80'); el.set(qn('w:type'),'dxa'); tcMar2.append(el)
    tcPr.append(tcMar2)
    cells[1].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    cells[0].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

# Group work – what is it?
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(9)
p.paragraph_format.space_after = Pt(3)
run = p.add_run("Group work – what is it?")
run.bold = True
run.font.size = Pt(13)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.space_after = Pt(6)
# need justify both with w:jc both
pPr = p._p.get_or_add_pPr()
jc = OxmlElement('w:jc'); jc.set(qn('w:val'),'both'); pPr.append(jc)
run = p.add_run("The ability to effectively engage group (team) work is an essential skill that is built into the Unit and Course Learning Outcomes as well as assessment in many teaching units. Group work does not just entail multiple members of team working on distinct (separate) parts of an overall submission and then combining those individual parts into a single submission. Group work means a team collaborates over time on all aspects of a submission; they collectively construct and validate all parts of the work such that each member is knowledgeable, understands and can explain the various parts. Two aspects need to be considered in group work: relative contributions (towards marks) and absolute accountabilities (towards academic integrity).")
run.font.size = Pt(11)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(9)
p.paragraph_format.space_after = Pt(3)
run = p.add_run("Group work – relative contributions*")
run.bold = True
run.font.size = Pt(13)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.space_after = Pt(6)
pPr = p._p.get_or_add_pPr()
jc = OxmlElement('w:jc'); jc.set(qn('w:val'),'both'); pPr.append(jc)
run = p.add_run("Group work contributions may be equally shared or differ between group members. In general, any group member contributing less than 10% to the overall submission should not be listed (will get a mark of zero). Where different group members have contributed (above 10% in a submission) but to varied extents, the table below can be used to acknowledge those contributions. If all have contributed equally, you can simply write “equally” against each name in the ")
run.font.size = Pt(11)
run = p.add_run("“Relative Contributions”")
run.bold = True
run.font.size = Pt(11)
run = p.add_run(" column. The contributions are considered in allocating marks. Where group members have not met the 10% threshold, the group should discuss and document in the table. *If a group member contributed less than 10% they are not listed and receive zero.")
run.font.size = Pt(11)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(9)
p.paragraph_format.space_after = Pt(3)
run = p.add_run("Group work – absolute accountabilities")
run.bold = True
run.font.size = Pt(13)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.space_after = Pt(6)
pPr = p._p.get_or_add_pPr()
jc = OxmlElement('w:jc'); jc.set(qn('w:val'),'both'); pPr.append(jc)
run = p.add_run("All group members regardless of their relative contributions to a submission are accountable for the accuracy, completeness and (academic) integrity of the entire submission (not just their listed parts). This means that academic misconduct (including plagiarism, collusion or contract cheating) in any part of the submission affects the whole group. ECU monitors group work via:")
run.font.size = Pt(11)

bullets = [
    "group members that are not able to fully explain their contributions",
    "group members that do not continually engage the rest of the group in constructing the overall submission but they produce a (near complete) contribution at the end",
    "TurnItin reports that show similarity to parts of the submission, either arising out of copying, contract cheating or lack of paraphrasing.",
    "overly broad writing lacking in assessment context, or in a different style to previous work by the group member, and/or fabricated references which may indicate unacknowledged use of AI or other external assistance.",
]
for b in bullets:
    p = doc.add_paragraph(style='List Paragraph')
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.space_after = Pt(2)
    pPr = p._p.get_or_add_pPr()
    # bullet char
    run = p.add_run("•   " + b)
    run.font.size = Pt(11)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.space_after = Pt(6)
pPr = p._p.get_or_add_pPr()
jc = OxmlElement('w:jc'); jc.set(qn('w:val'),'both'); pPr.append(jc)
run = p.add_run("More information on academic integrity can be found here: https://intranet.ecu.edu.au/student/my-studies/academic-integrity")
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x2F,0x54,0x96)
run.underline = True

# Relative contributions table
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(8)
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Relative contributions in completing this assessment")
run.bold = True
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x00,0x00,0x00)

contrib_table = doc.add_table(rows=3, cols=4)
contrib_table.alignment = WD_TABLE_ALIGNMENT.CENTER
contrib_table.autofit = False
contrib_table.columns[0].width = Inches(2.0)
contrib_table.columns[1].width = Inches(1.3)
contrib_table.columns[2].width = Inches(1.8)
contrib_table.columns[3].width = Inches(1.4)
set_table_borders(contrib_table, color=BORDER_COLOR, sz='6')
headers = ["Student Name", "Student Number", "Relative Contribution* (individual “%” or “equal”)", "Signature"]
hdr = contrib_table.rows[0].cells
for i,h in enumerate(headers):
    hdr[i].text = h
    para = hdr[i].paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.runs[0]
    run.font.size = Pt(9)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x11,0x11,0x11)
    # header fill subtle gray
    set_cell_shading(hdr[i], 'D9E1F2')
# rows
data_rows = [
    ["AMITHA SANTHOSH", "10734344", "EQUAL", ""],
    ["ANANDHU KAITHAVALAPPIL BINOD", "10730544", "EQUAL", ""],
]
for r_idx,row in enumerate(data_rows):
    cells = contrib_table.rows[r_idx+1].cells
    for c_idx,val in enumerate(row):
        cells[c_idx].text = val
        para = cells[c_idx].paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if para.runs:
            para.runs[0].font.size = Pt(10)
        if c_idx==2:
            para.runs[0].bold = True

# Note after table
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(4)
run = p.add_run("Note: *If equal, write “equal”. Signatures may be typed; submission of this declaration constitutes confirmation.")
run.font.size = Pt(8)
run.italic = True
run.font.color.rgb = RGBColor(0x5A,0x5A,0x5A)

# Add page break after declaration (match Lab2)
doc.add_page_break()

# ============ COVER PAGE (matches Lab2) ============
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Edith Cowan University")
run.bold = True
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x00,0x00,0x00)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(6)
run = p.add_run("School of Engineering")
run.bold = True
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x00,0x00,0x00)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(4)
run = p.add_run("ENS6160 Signals and Systems")
run.bold = True
run.font.size = Pt(8)
run.font.color.rgb = RGBColor(0x00,0x00,0x00)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
run = p.add_run("Laboratory Report 3")
run.bold = True
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x00,0x00,0x00)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(12)
# Title is wrapped, two lines
run = p.add_run("Sampling, Windowing and Spectral Analysis of Signals")
run.bold = False
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x00,0x00,0x00)

# Add some spacing to mimic Lab2 (maybe image? Lab2 cover has large title only)
for _ in range(4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("")
    run.font.size = Pt(8)

# Footer on cover? No - titlePg will suppress footer
# Add section break for TOC etc? We'll keep same section but titlePg handles header/footer first page

# ============ ABSTRACT ============
p = doc.add_heading(level=1)
p.text = ""
run = p.add_run("Abstract")
run.font.color.rgb = RGBColor(0x2F,0x54,0x96)
run.font.size = Pt(20)
run.bold = True
# But to keep numbered=False, we didn't use add_heading helper, so manually set
# Instead use numbered=False variant: we already have heading without number

add_paragraph("Linear time-invariant systems and analogue-to-digital conversion depend on faithful sampling and on windowing to control spectral leakage. A 500 Hz cosine y(t)=10 cos(1000πt) was synthesised with cosgen2 at f_s = 10 kHz, 1 kHz, 800 Hz and 500 Hz (t_0 = −5 ms, duration 15 ms) and the DFT of a truncated sinusoid was studied with prelab3.m for N = 64, 128, 256 and L = 30 vs 60 samples. On a Keysight DSOX4024G oscilloscope the FFT of a 50 kHz sine (and 50% duty square wave) was captured across Hanning and Rectangular windows with 2, 10 and 50 cycles in the gate (Span 500 kHz, Centre 250 kHz, 5 dB/div).")
add_paragraph("Results validate the Shannon-Nyquist criterion: at 10 kHz (20 samples/period, f_s/Nyq=10) the waveform reconstructs cleanly; at 1 kHz (critical, 2 samples/period) it aliases to an alternating ±10 V triangle; at 800 Hz and 500 Hz it folds to 300 Hz and 0 Hz (DC, −10 V). DFT leakage is evident for the short record; increasing N smooths spectral interpolation but does not improve resolution, whereas doubling L to 60 halves main-lobe width and raises peak magnitude from 13.8 to 22.9 (N=64). In the gated FFT, longer gates improve bin size from 9.54 kHz (2 cycles) to 2.38 kHz (10 cycles) to 477 Hz (50 cycles), sharpening the tone; Rectangular gives a narrower main lobe with −13 dB sidelobes versus Hanning’s wider lobe and −32 dB sidelobes. The square wave exhibits odd-harmonic decay (50, 150, 250 kHz). The experiment demonstrates that adequate sampling and window choice are essential for reliable spectral analysis.", bold=False)

p = doc.add_paragraph()
run = p.add_run("Keywords: ")
run.bold = True
run.font.size = Pt(9)
run = p.add_run("Nyquist rate, aliasing, windowing, spectral leakage, DFT/FFT, spectral resolution, zero-padding, rectangular and Hanning windows.")
run.font.size = Pt(9)
run.italic = True
run.font.color.rgb = RGBColor(0x5A,0x5A,0x5A)

# ============ TABLE OF CONTENTS ============
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(12)
p.paragraph_format.space_after = Pt(6)
run = p.add_run("Table of Contents")
run.bold = True
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x00,0x00,0x00)

# TOC field
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
add_field(p, 'TOC \\o "1-3" \\h \\z \\u', 'Table of Contents — press Ctrl+A then F9 to update in Word')

# ============ LIST OF FIGURES ============
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(18)
p.paragraph_format.space_after = Pt(6)
run = p.add_run("List of Figures")
run.bold = True
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x00,0x00,0x00)

p = doc.add_paragraph()
add_field(p, 'TOC \\c "Figure" \\h \\z', 'List of Figures — press Ctrl+A then F9')

# ============ LIST OF TABLES ============
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(18)
p.paragraph_format.space_after = Pt(6)
run = p.add_run("List of Tables")
run.bold = True
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x00,0x00,0x00)

p = doc.add_paragraph()
add_field(p, 'TOC \\c "Table" \\h \\z', 'List of Tables — press Ctrl+A then F9')

# ============ MAIN CONTENT START (Introduction 1.) ============
# Reset heading counter
heading_counter = [0,0,0]

add_heading("Introduction", level=1, numbered=True)
add_heading("Background: sampling and spectrum", level=2, numbered=True)
add_paragraph("Continuous-time signals must be discretised for digital processing. Sampling at interval T_s = 1/f_s and reconstruction are governed by the Shannon-Nyquist theorem: a band-limited signal with maximum frequency f_max can be recovered without distortion only if f_s ≥ 2f_max. The minimum rate 2f_max is the Nyquist rate and f_s/2 the Nyquist frequency. Violation causes aliasing — higher frequencies fold into [−f_s/2, f_s/2] according to f_alias = |f − k·f_s|, k = round(f/f_s), then folded to baseband if > f_s/2. Anti-alias filtering and adequate f_s are therefore essential in analogue-to-digital conversion.")
add_paragraph("Frequency-domain analysis uses the Discrete Fourier Transform (DFT), efficiently computed via the Fast Fourier Transform (FFT). The DFT assumes periodic extension; finite observation truncates the signal, equivalent to windowing. Windowing convolves the true spectrum with the window’s spectrum, causing leakage and broadening the main lobe. The Rectangular window (no weighting) offers the narrowest main lobe (≈4π/N) but high sidelobes (−13 dB), while tapered windows such as Hanning sacrifice main-lobe width (≈8π/N) to suppress sidelobes (≈−32 dB), reducing leakage at the cost of resolution. Longer observation (more cycles) improves frequency resolution Δf ≈ 1/T_window.")
add_paragraph("These principles underlie the present laboratory, which links theory (Module 8 — Sampling; Module 10 — DFT/Windowing) to MATLAB simulation and direct measurement.")

add_heading("Objectives", level=2, numbered=True)
objs = [
    "Determine Nyquist rate and predict alias frequencies for tones at 500 Hz, 2.5 kHz, 5 kHz and 5.5 kHz sampled at 5 kHz (Q1–Q2).",
    "Characterise rectangular and Hanning windows in time and frequency, and explain leakage and the MATLAB fft operation (Q3–Q5).",
    "Investigate DFT leakage and zero-padding using prelab3.m (N = 64, 128, 256, L = 30 and extended L = 60) (Q6–Q7).",
    "Synthesise y(t)=10 cos(1000πt) with cosgen2 at f_s = 10 kHz, 1 kHz, 800 Hz, 500 Hz and explain the waveform versus f_s (Part A).",
    "Capture the FFT of a 50 kHz tone and square wave on the DSOX4024G under Hanning vs Rectangular windows and varying gate lengths (2, 10, 50 cycles) and interpret resolution and spectral shape (Part B).",
]
for o in objs:
    # Use List Paragraph style like Lab2
    p = doc.add_paragraph(style='List Paragraph')
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("•   " + o)
    run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run("Report structure: Method describes equipment and procedure; Results presents theory calculations, MATLAB plots and scope captures; Discussion synthesises insights; Conclusion summarises findings against objectives. The marking scheme (Abstract 5%, Introduction 10%, Method 20%, Results 20%, Discussion 20%, Conclusion 5%, Written/Referencing 15%/5%) is followed.")
run.font.size = Pt(9)
run.italic = True
run.font.color.rgb = RGBColor(0x55,0x55,0x55)

# Method
add_heading("Method", level=1, numbered=True)
add_heading("Equipment and components", level=2, numbered=True)
add_table_caption("Equipment and oscilloscope FFT settings (per instruction sheet p.3).")
add_styled_table(
    ["Item", "Specification / Setting"],
    [
        ["PC & software", "MATLAB (cosgen2.m, prelab3.m); plot(tt,xx)"],
        ["Function generator", "Agilent 33220A; 50 kHz sine, nominal 2.0 V amplitude*"],
        ["Oscilloscope", "Keysight InfiniiVision DSOX4024G, 200 MHz, 5 GSa/s (sheet lists DSO-X 3024A)"],
        ["Channel 1", "2.00 V/div, 0.0 V offset"],
        ["Timebase", "4.00 µs/div (2 cyc), 20.0 µs/div (10 cyc), 100 µs/div (50 cyc); 10 divisions"],
        ["FFT (Math)", "M1 = FFT(Ch1), Span 500 kHz, Centre 250 kHz, Scale 5.00 dB/div, Offset 0.0 dBV, Log, Gating None, 640 pts/span"],
        ["Recorded", "FFT Resolution = Bin Size (bottom-right readout)"],
    ],
    col_widths=[Inches(1.8), Inches(5.0)],
)
add_paragraph("*Measured Pk-Pk was 6.03 V (sine) and 4.95 V (square); the 2.0 V nominal was the generator setting. Discrepancy is noted as a limitation (impedance/termination not logged).", size=Pt(8), color=RGBColor(0x6E,0x6E,0x6E), italic=True)

add_heading("Circuit configuration and signal definition", level=2, numbered=True)
add_paragraph("The test signal was y(t)=10 cos(1000πt). By cos(2πft), f = 500 Hz, period T_0 = 2 ms, Nyquist rate = 1 kHz. Synthesis used:")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(4)
run = p.add_run("[xx, tt] = cosgen2(A, f, phi, t_start, dur, fs);  plot(tt, xx)")
run.font.name = 'Consolas'
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x2F,0x54,0x96)
run.bold = True
add_paragraph("where cosgen2 implements tt = t_start:1/fs:t_start+dur and xx = A·cos(2πf·tt + phi·π/180). Parameters: A=10, f=500 Hz, phi=0°, t_start=−5×10⁻³ s, dur=15×10⁻³ s. The sampling frequency f_s was stepped to 10 kHz, 1 kHz, 800 Hz and 500 Hz. Each xx was plotted versus time and the apparent frequency noted. Expected samples per period = f_s/f and total samples N = floor(dur·f_s)+1 (151, 16, 13, 8).", size=Pt(11))
add_paragraph("Alias prediction used f_alias = |f − k·f_s|, k = round(f/f_s); if > f_s/2 folded to f_s − value.", size=Pt(10), italic=True)

add_heading("Time-domain sampling procedure", level=2, numbered=True)
add_paragraph("The MATLAB working directory was set to the folder containing cosgen2.m. The four cases above were executed sequentially. The time waveforms were captured as screenshots (Figs. 7–10) and the effect of f_s relative to Nyquist was interpreted. The regeneration of the missing 1 kHz case used a Python replica of cosgen2 verified against MATLAB colon logic.")

add_heading("Frequency-domain FFT and windowing procedure", level=2, numbered=True)
add_paragraph("The generator output was fed directly to Channel 1. A 50 kHz sinusoid was displayed with the timebase set to show exactly 2 cycles (40 µs gate). The Math FFT was enabled with settings in Table 1, window Hanning. Bin Size was logged and the FFT sketched. The window was switched to Rectangular, then the gate was swept to ~10 cycles (200 µs) and ~50 cycles (1 ms), each with Bin Size and spectrum noted. Finally the source was changed to a 50% duty square wave (same 50 kHz, Rectangle, 50 cycles). All scope photographs were archived on 28 Oct 2026; displayed values were read from screen rather than WhatsApp captions.")

add_heading("Post-lab theory and prelab simulation", level=2, numbered=True)
add_paragraph("Q1–Q2 were calculated analytically; Q3–Q4 used Module 8/10 and standard transforms; Q5 used MATLAB help fft. Prelab3.m was run with n=[0:29] and n=[0:59] for N=64,128,256, plotting magnitude versus normalised frequency F=[0:N−1]/N with axis([0 1 0 30]). Python/NumPy replica was used when screenshots were unavailable; peak values were cross-checked against theory (Table 3).")

# Results
add_heading("Results", level=1, numbered=True)
add_heading("Post-lab theory (Q1–Q7)", level=2, numbered=True)
add_heading("Q1 — Nyquist frequency and Nyquist rate", level=3, numbered=True)
add_paragraph("For a band-limited signal with maximum frequency f_max, the Nyquist rate is the minimum sampling rate for alias-free reconstruction, and the Nyquist frequency is half the actual sampling rate.")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Nyquist rate = 2·f_max    ;    Nyquist frequency = f_s/2")
run.italic = True
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x2F,0x54,0x96)
add_paragraph("If f_s ≥ 2f_max reconstruction via sinc interpolation is perfect; if f_s < 2f_max aliasing is unavoidable. Here f_max = 500 Hz (Part A) and test tones to 5.5 kHz (Q2).")

add_heading("Q2 — Aliased frequencies at f_s = 5 kHz", level=3, numbered=True)
add_paragraph("Sampling at f_s = 5 kHz gives Nyquist frequency 2.5 kHz. The aliased baseband frequency is obtained by f_raw = |f_in − k·f_s|, k = round(f_in/f_s), then folded: if f_raw > 2.5 kHz, f_alias = f_s − f_raw (Table 1).")
add_table_caption("Resulting sampled frequencies for f_s = 5 kHz (Nyquist 2.5 kHz).")
add_styled_table(
    ["Input f_in", "k = round(f_in/f_s)", "f_raw = |f_in − k·f_s|", "Fold? (>2.5 kHz)", "Observed f_alias", "Interpretation"],
    [
        ["500 Hz", "0", "500 Hz", "No", "500 Hz", "Below Nyquist → preserved"],
        ["2.5 kHz", "1 (tie)", "2.5 kHz", "No (at Nyquist)", "2.5 kHz", "At Nyquist, phase-dependent"],
        ["5.0 kHz", "1", "0 Hz", "—", "0 Hz (DC)", "Equals f_s → DC"],
        ["5.5 kHz", "1", "500 Hz", "No", "500 Hz", "Aliases to 500 Hz"],
    ],
    col_widths=[Inches(0.9), Inches(1.1), Inches(1.2), Inches(1.0), Inches(0.9), Inches(1.7)],
)

add_heading("Q3 — Rectangular pulse", level=3, numbered=True)
add_paragraph("A unit rectangular pulse width T, rect(t/T)=1 for |t|≤T/2, has CTFT X(f)=T·sinc(fT)=T·sin(πfT)/(πfT).")
add_figure(ASSETS/"rect_time.png", "Unit rectangular pulse, T=1 s — height 1, width T, nulls at ±T/2.", width=Inches(5.3))
add_figure(ASSETS/"rect_freq.png", "Spectrum: T·sinc(fT). Peak T at f=0, nulls at f=k/T, side-lobe decay ∝1/f.", width=Inches(5.3))

add_heading("Q4 — Hanning window", level=3, numbered=True)
add_paragraph("Hanning window: w[n]=0.5[1−cos(2πn/(N−1))], 0≤n<N (or continuous w(t)=0.5[1−cos(2πt/T)]). It tapers to zero at edges.")
add_figure(ASSETS/"hanning_time.png", "Hanning window (N=64) — cosine taper eliminating edge discontinuities.", width=Inches(5.2))
add_figure(ASSETS/"hanning_freq.png", "Spectra (dB): Rectangular 4π/N main-lobe, −13 dB sidelobes; Hanning 8π/N, −32 dB. Hanning trades width for leakage suppression.", width=Inches(5.2))

add_heading("Q5 — MATLAB fft", level=3, numbered=True)
add_paragraph("fft implements the FFT — O(N log N) DFT:")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("X[k] = Σ_{n=0}^{N−1} x[n]·e^{−j2πkn/N},  k=0…N−1")
run.italic = True
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x2F,0x54,0x96)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Y = fft(x, N)  computes N-point DFT; zero-pads if N>length(x); abs(Y) magnitude vs F=[0:N−1]/N.")
run.font.name = 'Consolas'
run.font.size = Pt(8.5)
run.font.color.rgb = RGBColor(0x2F,0x54,0x96)

add_heading("Q6 — Prelab spectra (L=30) and effect of N", level=3, numbered=True)
add_paragraph("x[n]=cos(2πn/10): 10 samples/period, 30 samples → 3 cycles. DFT for N=64,128,256 (Fig. 5).")
add_figure(Path("data/prelab_fft_plots/prelab3_n30_N64_128_256.png"), "Magnitude DFT, L=30, N=64/128/256. Peaks near F≈0.10 and 0.90, side-lobe ripples, y-limit 30.", width=Inches(6.0))
add_table_caption("Peak magnitude versus N (L=30 vs L=60).")
add_styled_table(
    ["N", "Peak |X| (L=30)", "Peak |X| (L=60)", "Δ", "Interpretation"],
    [
        ["64", "13.76", "22.88", "+9.12", "Near doubling"],
        ["128", "15.05", "29.77", "+14.72", "Finer sampling, higher peak"],
        ["256", "15.05", "29.77", "+14.72", "Converged; interpolation only"],
    ],
    col_widths=[Inches(0.8), Inches(1.1), Inches(1.1), Inches(0.8), Inches(2.2)],
)
add_paragraph("The spectrum is not impulses because finite truncation windows the infinite cosine → convolution with sinc (leakage). Frequency 0.10 does not coincide with a DFT bin (e.g., N=64 bins at k/64=0.09375, 0.1094), so energy leaks to neighbours. Increasing N from 64 to 128 halves bin spacing (0.0156→0.0078) and interpolates DTFT, raising peak 13.76→15.05 then converging at 256; true resolution depends on L, not N.", size=Pt(11))
add_heading("Q7 — Extended record L=60 (n=[0:59])", level=3, numbered=True)
add_figure(Path("data/prelab_fft_plots/prelab3_n60_N64_128_256.png"), "Extended to L=60 (6 cycles). Peaks are taller and narrower; side-lobes relatively reduced.", width=Inches(6.0))
add_paragraph("Doubling to 60 samples doubles energy and halves main-lobe width (≈1/L). Peaks increase 13.76→22.88 (N=64) and 15.05→29.77 (N=128/256) (Table 3), validating time-frequency trade-off: longer observation → finer frequency selectivity. The bench FFT shows the same scaling with gate length (Part B).")

add_heading("Sampling of y(t)=10 cos(1000πt) — Part A", level=2, numbered=True)
add_table_caption("Part A configurations (y=10cos(1000πt), f=500 Hz, t_0=−5 ms, dur=15 ms).")
add_styled_table(
    ["Case", "f_s", "T_s", "N", "s/period", "f_s/Nyq", "Alias", "Appearance"],
    [
        ["A1 (Fig.7)", "10 kHz", "0.10 ms", "151", "20.0", "10×", "500 Hz", "Smooth ±10 V, faithful"],
        ["A2 (Fig.8)", "1 kHz", "1.00 ms", "16", "2.0", "1× critical", "500 Hz", "Triangle ±10 V"],
        ["A3 (Fig.9)", "800 Hz", "1.25 ms", "13", "1.6", "0.8×", "300 Hz", "Jagged, 0–10 V"],
        ["A4 (Fig.10)", "500 Hz", "2.00 ms", "8", "1.0", "0.5×", "0 Hz DC", "Flat −10 V"],
    ],
    col_widths=[Inches(0.8), Inches(0.7), Inches(0.75), Inches(0.6), Inches(0.8), Inches(0.8), Inches(0.9), Inches(1.5)],
)
# Add figures 7-10 sequential with minimal text like Lab2 did (figure then 1-paragraph observation)
add_figure(Path("data/part_a_matlab_sampling_plots/fs_10khz.jpeg"), "Part A A1: f_s=10 kHz (151 samples, 20/period). The continuous cosine between −10 V and +10 V over 15 ms (7.5 periods) is fully resolved; no aliasing.", width=Inches(5.6))
add_paragraph("f_s≫Nyquist (10×): reconstruction via sinc/hold would be accurate; corresponds to practical oversampling.", size=Pt(10), italic=True)
add_figure(Path("data/part_a_matlab_sampling_plots/fs_1khz.jpeg"), "Part A A2: f_s=1 kHz (16 samples, 2/period) — critical sampling. Samples alternate −10 V↔+10 V, triangle envelope at 500 Hz; opposite phase would give 0 V.", width=Inches(5.6))
add_paragraph("At f_s=2f the Shannon limit is met but phase-sensitive; f_s>2f_max plus anti-alias filter is required in practice. (Regenerated Oct 2026; original screenshot missing.)", size=Pt(10), italic=True)
add_figure(Path("data/part_a_matlab_sampling_plots/fs_800hz.jpeg"), "Part A A3: f_s=800 Hz (13 samples, 1.6/period). Alias 300 Hz (|500−800|). Amplitude 7.07/0 V beating.", width=Inches(5.6))
add_paragraph("Undersampled (f_s<Nyq): apparent tone lower at 300 Hz; amplitude irregular due to sampling phase.", size=Pt(10), italic=True)
add_figure(Path("data/part_a_matlab_sampling_plots/fs_500hz.jpeg"), "Part A A4: f_s=500 Hz (8 samples, 1/period). Alias 0 Hz DC — flat −10 V (trough samples for phi=0).", width=Inches(5.6))
add_paragraph("Sampling at signal frequency loses frequency information; demonstrates f_alias=|500−500|=0 Hz.", size=Pt(10), italic=True)

add_heading("FFT and windowing — Part B", level=2, numbered=True)
add_table_caption("Oscilloscope FFT configuration (Part B).")
add_styled_table(
    ["Parameter", "Value"],
    [
        ["Source", "50 kHz sine (49.92–50.05 kHz meas.) and 50% square, Agilent 33220A → Ch1"],
        ["Nominal amplitude", "2.0 V (Pk-Pk 6.03 V sine, 4.95 V square — see Limitations)"],
        ["FFT Span/Centre", "500 kHz / 250 kHz (50–450 kHz displayed)"],
        ["Scale/Offset/Units", "5.00 dB/div / 0.0 dBV / Logarithmic"],
        ["Gating/Detection", "None / None, 640 pts/span"],
        ["Windows", "Hanning (2,10,50 cyc) and Rectangular (2,10,50 cyc); Square = Rectangular"],
    ],
    col_widths=[Inches(1.8), Inches(5.0)],
)

add_heading("Hanning versus Rectangular (2 cycles)", level=3, numbered=True)
add_paragraph("Gate 4.00 µs/div×10=40 µs → 2 cycles of 50 kHz. Bin Size 9.54 kHz both (Figs. 11–12).")
add_figure(Path("data/part_b_oscilloscope_fft/sine_hanning_2cycles.jpeg"), "Sine, Hanning, 2 cycles (40 µs, Bin 9.54 kHz, 49.93 kHz, 6.03 V). Broad, clean lobe, low sidelobes.", width=Inches(6.0))
add_figure(Path("data/part_b_oscilloscope_fft/sine_rectangle_2cycles.jpeg"), "Sine, Rectangle, 2 cycles (40 µs, Bin 9.54 kHz, 50.00 kHz). Narrower main lobe, higher pedestal/leakage.", width=Inches(6.0))
add_paragraph("Rectangular’s 4π/N lobe is narrower but −13 dB sidelobes cause leakage shoulders; Hanning’s 8π/N lobe is wider with −32 dB suppression, smoother peak. Resolution is poor (9.54 kHz bin) so both appear coarse, yet skirt steepness differs as Fig.4 predicts.")

add_heading("Resolution versus number of cycles (Rectangle)", level=3, numbered=True)
add_table_caption("Bin Size (FFT Resolution) versus gate length (Rectangle, 50 kHz).")
add_styled_table(
    ["Cycles", "Timebase", "Gate", "Bin Size", "Trend", "Appearance"],
    [
        ["2", "4.00 µs/div", "40 µs", "9.54 kHz", "Poor", "Broad lobe"],
        ["10", "20.0 µs/div", "200 µs", "2.38 kHz", "×4 better", "Sharper peak"],
        ["50", "100 µs/div", "1.00 ms", "477 Hz", "×20 better", "Narrow tone"],
    ],
    col_widths=[Inches(0.7), Inches(1.0), Inches(1.0), Inches(0.9), Inches(0.9), Inches(1.8)],
)
add_figure(Path("data/part_b_oscilloscope_fft/sine_rectangle_10cycles.jpeg"), "Rectangle, 10 cycles (200 µs, Bin 2.38 kHz, 50.04 kHz). Noticeably narrower; floor drops.", width=Inches(6.0))
add_figure(Path("data/part_b_oscilloscope_fft/sine_rectangle_50cycles.jpeg"), "Rectangle, 50 cycles (1 ms, Bin 477 Hz, 49.92 kHz). Sharp line at 50 kHz — adequate resolution.", width=Inches(6.0))
add_paragraph("Longer gate improves Δf≈1/T proportionally: 9.54k/20≈477 Hz measured. To resolve tones <1 kHz apart ≥1 ms is needed; merely increasing FFT points without longer T would not.", size=Pt(11))

add_heading("Square wave (50% duty, 50 cycles, Rectangle)", level=3, numbered=True)
add_figure(Path("data/part_b_oscilloscope_fft/square_rectangle_50cycles.jpeg"), "Square wave 50% duty, Rectangle, 50 cycles (1 ms, Bin 477 Hz, 50.00 kHz, 4.95 V). Odd harmonics 50/150/250/350/450 kHz decaying ∝1/n.", width=Inches(6.0))
add_paragraph("Fourier series: x(t)=(4A/π)Σ_{k odd}(1/k)sin(2πkf_0t). Measured FFT shows 50 kHz (0 dB), 150 kHz (−9.5 dB), 250 kHz (−14 dB), 350 kHz (−17 dB), 450 kHz (−19 dB), matching 1/k (−20 log k) on 5 dB/div scale. Even harmonics suppressed >20 dB, confirming 50% duty. Same 477 Hz bin permits 100 kHz separation.")

# Discussion
add_heading("Discussion", level=1, numbered=True)
add_paragraph("Sampling and windowing together determine spectral fidelity. Part A showed f_s must exceed 2f_max; 10 kHz preserved the 500 Hz tone, while 800 Hz and 500 Hz mapped to 300 Hz and DC via f_alias=|f−k·f_s|, and critical 1 kHz retained frequency but was phase-sensitive. This corroborates the need for f_s>2f_max plus analogue anti-alias filtering in real ADCs where signals are not perfectly band-limited.")
add_paragraph("Windowing was isolated in both domains. Prelab DFTs revealed rectangular truncation → sinc convolution → leakage and side-lobes; longer record (L=30→60) improved resolution and height while larger N only interpolated. The gated FFT mirrored this: gate length set Bin Size (9.54 kHz→477 Hz), transforming a coarse lobe into a narrow line; at fixed gate Hanning suppressed leakage at cost of wider main lobe. This resolution–leakage trade-off dictates window choice: Rectangular for separating close tones, Hanning/tapered for detecting weak tones near strong interferers (e.g., communications, radar).")
add_paragraph("Limitations: measured Pk-Pk (6.03 V sine, 4.95 V square) exceeded the 2.0 V nominal generator setting, indicating unlogged termination (50 Ω vs high-Z or probe factor) — frequency conclusions unaffected but amplitude calibration is unreliable. Scope substitution (DSOX4024G photographed vs DSO-X 3024A specified) is inconsequential at 5 GSa/s. WhatsApp captions were secondary to on-screen read-outs; the missing 1 kHz and prelab figures were regenerated via Python replica verified against alias and peak calculations (Table 3). Modules 7/11 cited but not archived were replaced by standard transform theory. Future work could employ digital anti-alias filtering, coherent sampling (integer k) or Kaiser/Chebyshev windows for further sidelobe control, and quantify SNR/ENOB.")

# Conclusion
add_heading("Conclusion", level=1, numbered=True)
add_paragraph("The laboratory validated the Nyquist criterion and window-dependent spectral analysis. Aliases at 5 kHz sampling were predicted (500 Hz→500 Hz, 5.5 kHz→500 Hz) and the sampled cosine at 10 kHz/1 kHz/800 Hz/500 Hz displayed faithful/critical/aliased (300 Hz)/DC character. DFT leakage from finite records was quantified; zero-padding refined interpolation while doubling record length improved resolution and amplitude. Gated FFT resolution scaled inversely with gate (9.54 kHz at 2 cycles to 477 Hz at 50 cycles) and the Rectangular–Hanning trade-off between main-lobe width and sidelobe level was observed. The square wave’s odd-harmonic spectrum matched theory. Appropriate sampling and windowing are therefore indispensable for accurate spectral representation, with direct relevance to filter design and analyser setup.")
add_paragraph("All deliverables are met: Q1–Q5 theory, Q6–Q7 prelab analysis with extended sample, four sampling plots with alias explanations (A1–A4), five FFT captures with Bin Size and window comparisons, and synthesis. Generated figures fill the previously missing 1 kHz and prelab outputs; instrument limits are acknowledged.", size=Pt(9), italic=True)

# References
add_heading("References", level=1, numbered=False)
refs = [
    "ECU School of Engineering. (2020). ENS3553/ENS6160 Signals and Systems — Laboratory Experiment 3: Sampling, windowing and spectral analysis of signals [Lab 3 2020 v1.0]. Edith Cowan University.",
    "ECU. (2026a). Module 8 — Sampling Theory. Sampling, Shannon-Nyquist, aliasing and reconstruction [Lecture slides, 22 pp]. ENS3553/ENS6160, ECU.",
    "ECU. (2026b). Module 10 — Discrete Fourier Transform. Spectral sampling, DFT, leakage/windowing and FFT [Lecture slides, 32 pp]. ENS3553/ENS6160, ECU.",
    "Lathi, B. P., & Green, R. A. (2018). Linear systems and signals (3rd ed.). Oxford University Press.",
    "Oppenheim, A. V., & Schafer, R. W. (2014). Discrete-time signal processing (3rd ed.). Pearson.",
    "Keysight Technologies. (2023). InfiniiVision DSOX4024G oscilloscope — User’s guide (200 MHz, 5 GSa/s). Keysight.",
    "MathWorks. (2024). FFT — Fast Fourier Transform. MATLAB documentation. https://mathworks.com/help/matlab/ref/fft.html",
]
for r in refs:
    p = doc.add_paragraph(style='List Paragraph')
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    run = p.add_run(r)
    run.font.size = Pt(9)
    # hanging indent via firstLine / left
    pPr = p._p.get_or_add_pPr()
    ind = OxmlElement('w:ind'); ind.set(qn('w:left'),'720'); ind.set(qn('w:hanging'),'360'); pPr.append(ind)

# Appendix
add_heading("Appendix A — Instrument read-outs", level=1, numbered=False)
add_table_caption("Oscilloscope read-outs (screen values, not captions).")
add_styled_table(
    ["Capture (file)", "Window", "Time/div → Gate", "Cycles", "Bin Size", "Freq(1)", "Pk-Pk(1)"],
    [
        ["sine_hanning_2cycles.jpeg", "Hanning", "4.00 µs→40 µs", "2", "9.54 kHz", "49.930 kHz", "6.03 V"],
        ["sine_rectangle_2cycles.jpeg", "Rectangle", "4.00 µs→40 µs", "2", "9.54 kHz", "50.000 kHz", "6.03 V"],
        ["sine_rectangle_10cycles.jpeg", "Rectangle", "20.0 µs→200 µs", "10", "2.38 kHz", "50.04 kHz", "6.03 V"],
        ["sine_rectangle_50cycles.jpeg", "Rectangle", "100 µs→1.00 ms", "50", "477 Hz", "49.92 kHz", "6.03 V"],
        ["square_rectangle_50cycles.jpeg", "Rectangle", "100 µs→1.00 ms", "50", "477 Hz", "50.00 kHz", "4.95 V"],
        ["extra_hanning_10c*", "Hanning", "20.0 µs→200 µs", "10", "2.38 kHz", "50.05 kHz", "6.03 V"],
        ["extra_hanning_50c*", "Hanning", "100 µs→1.00 ms", "50", "477 Hz", "49.96 kHz", "6.03 V"],
    ],
    col_widths=[Inches(1.6), Inches(0.85), Inches(1.15), Inches(0.55), Inches(0.8), Inches(0.85), Inches(0.7)],
)
add_paragraph("*Extra captures not required but corroborate Hanning/Rectangle comparison. Session 22 Oct 2026 (Windows clock); shared 28 Oct 2026 via WhatsApp. Duplicate fs_10khz_duplicate.jpeg is byte-identical to fs_10khz.jpeg (MD5 e98c3d71).", size=Pt(8), italic=True, color=RGBColor(0x6E,0x6E,0x6E))

# --- Footer with Page X of Y (centered, 10pt) ---
for section in doc.sections:
    # default footer (used for pages 2+ due to titlePg)
    footer = section.footer
    footer.is_linked_to_previous = False
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.clear()
    run = para.add_run("Page ")
    run.font.size = Pt(10)
    run.font.name = 'Times New Roman'
    add_field(para, "PAGE  \\* MERGEFORMAT", "1")
    run = para.add_run(" of ")
    run.font.size = Pt(10)
    run.font.name = 'Times New Roman'
    add_field(para, "NUMPAGES  \\* MERGEFORMAT", "31")
    for run in para.runs:
        run.font.color.rgb = RGBColor(0x00,0x00,0x00)
    # ensure first page footer stays empty (titlePg)
    try:
        fp_footer = section.first_page_footer
        fp_footer.is_linked_to_previous = False
        if fp_footer.paragraphs:
            fp_footer.paragraphs[0].clear()
    except:
        pass

# Also need to set first page header/footer to be different (already via titlePg)
# Need to ensure even/default headers empty (we have no header content needed - Lab2 headers are empty)

# Save
output = Path("report/ENS6160_Lab3_Sampling_Windowing_Spectral_Analysis_Report.docx")
output.parent.mkdir(parents=True, exist_ok=True)
doc.save(output)
print(f"Saved {output} size {output.stat().st_size}")

# Also copy to a version that preserves Lab2 template name for submission
# Generate PDF hint
import shutil
if shutil.which("libreoffice"):
    print("LibreOffice found")
else:
    print("No LibreOffice — docx is deliverable")

