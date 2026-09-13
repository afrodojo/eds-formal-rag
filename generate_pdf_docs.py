# generate_pdf_docs.py - Technical Documentation PDF Generator
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_filename = "EDS_Overwatch_Technical_Documentation.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
styles = getSampleStyleSheet()

# Custom Color Palette
DARK_NAVY = colors.HexColor("#0f172a")
CYAN_ACCENT = colors.HexColor("#0284c7")
TEXT_COLOR = colors.HexColor("#334155")

title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=22,
    textColor=DARK_NAVY,
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=12,
    textColor=CYAN_ACCENT,
    spaceAfter=15
)

h1_style = ParagraphStyle(
    "Heading1Custom",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=14,
    textColor=DARK_NAVY,
    spaceBefore=12,
    spaceAfter=6
)

body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10,
    textColor=TEXT_COLOR,
    leading=14,
    spaceAfter=8
)

code_style = ParagraphStyle(
    "CodeCustom",
    parent=styles["Normal"],
    fontName="Courier",
    fontSize=9,
    textColor=colors.HexColor("#0f172a"),
    backColor=colors.HexColor("#f1f5f9"),
    borderPadding=6,
    spaceAfter=8
)

story = []

# Title Banner
story.append(Paragraph("🛡️ Zero-Gravity SOC Command Center & Overwatch AI", title_style))
story.append(Paragraph("System Architecture, Mathematical Proofs, Requirements & FAQ Specification", subtitle_style))
story.append(HRFlowable(width="100%", thickness=2, color=CYAN_ACCENT, spaceAfter=15))

# Section 1: System Overview
story.append(Paragraph("1. System Architecture & Core Capabilities", h1_style))
story.append(Paragraph(
    "The <b>Emerging Defense Solutions (EDS) SOC Command Center</b> provides deterministic verification for LLM token decoding alongside real-time hardware digital twin telemetry. Operating under AMD SEV-SNP guest enclaves (VMPL 0), the system enforces policy constraints using the Z3 SMT logic solver while delivering hands-free operational control via a speech-to-speech assistant modeled after JARVIS with a Jamaican accent.",
    body_style
))

# Section 2: Mathematical Framework
story.append(Paragraph("2. Mathematical Framework & Formal Proofs", h1_style))
story.append(Paragraph("<b>Monad Logit Transformation:</b> Candidate token output logits L_i are modified deterministically prior to decoding:", body_style))
story.append(Paragraph("<b>L_hat_i = L_i + log( Phi(v_i) )</b>", code_style))
story.append(Paragraph("Where <b>Phi(v_i) = 1</b> if Z3 SMT evaluation returns SAT, and <b>0</b> if UNSAT (reducing candidate logit to -infinity and guaranteeing <b>P_violation = 0</b>).", body_style))
story.append(Paragraph("<b>Formal Access Control Property:</b>", body_style))
story.append(Paragraph("<b>HasCUI(v_i) => ( IsEncryptedEnclave AND IsVerifiedSession )</b>", code_style))

# Section 3: Requirements Table
story.append(Paragraph("3. Hardware & Power Requirements", h1_style))
table_data = [
    ["Hardware Accelerator", "Power Draw (kW)", "Thermal Recovery Efficiency"],
    ["Cerebras CS-4 Engine", "28.00 kW", "91% Heat Exhaust Captured"],
    ["Cerebras CS-3 Engine", "23.00 kW", "91% Heat Exhaust Captured"],
    ["NVIDIA B200 HGX Cluster", "14.30 kW", "91% Heat Exhaust Captured"],
    ["NVIDIA H200 HGX Cluster", "7.00 kW", "91% Heat Exhaust Captured"],
    ["AMD AI Halo Unit", "0.75 kW", "Direct Liquid Immersion"]
]
t = Table(table_data, colWidths=[200, 140, 180])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK_NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0,0), (-1,0), 6),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ('FONTSIZE', (0,0), (-1,-1), 9),
]))
story.append(t)
story.append(Spacer(1, 12))

# Section 4: Troubleshooting Guide
story.append(Paragraph("4. Troubleshooting & Operational Fixes", h1_style))
trouble_data = [
    ["Symptom / Error", "Root Cause", "Resolution Strategy"],
    ["Port 7870 in use", "Orphaned Python server process", "Execute: Stop-Process -Name 'python' -Force"],
    ["ElevenLabs 401 Error", "Key missing tts_write access", "Generate Full Access key at elevenlabs.io"],
    ["Silent Audio Playback", "Browser autoplay policy block", "Base64 HTML5 stream auto-plays automatically"]
]
t2 = Table(trouble_data, colWidths=[150, 170, 200])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), CYAN_ACCENT),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ('FONTSIZE', (0,0), (-1,-1), 9),
]))
story.append(t2)

doc.build(story)
print(f"[SUCCESS] Technical Documentation generated: {pdf_filename}")
