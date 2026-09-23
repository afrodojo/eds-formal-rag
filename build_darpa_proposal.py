import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def create_darpa_pdf(filename="DARPA_AEGIS_MONAD_Proposal.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
    )
    styles = getSampleStyleSheet()
    story = []

    # Custom Styles
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=20, leading=24, alignment=TA_CENTER, textColor=colors.HexColor('#0F172A'))
    sub_title_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#475569'))
    h1_style = ParagraphStyle('SectionH1', parent=styles['Heading2'], fontSize=13, leading=17, textColor=colors.HexColor('#1E3A8A'), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14, alignment=TA_JUSTIFY, textColor=colors.HexColor('#1E293B'), spaceBefore=4, spaceAfter=4)
    code_style = ParagraphStyle('CodeBlock', parent=styles['Normal'], fontName='Courier', fontSize=9, leading=12, textColor=colors.HexColor('#0F172A'))

    # Title Block
    story.append(Paragraph("<b>DARPA TECHNICAL PROGRAM PROPOSAL</b>", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>PROJECT AEGIS-MONAD</b><br/><i>Autonomous Enclave Formal Verification & Grid-Isolated SOC Infrastructure</i>", sub_title_style))
    story.append(Spacer(1, 8))
    
    # Metadata Box
    meta_data = [
        [Paragraph("<b>Proposed Program Manager:</b> Asaad Morman (D.A.S. Candidate, Bowie State University)", body_style)],
        [Paragraph("<b>Target Offices:</b> DARPA Information Innovation Office (I2O) / Defense Sciences Office (DSO)", body_style)],
        [Paragraph("<b>Classification:</b> UNCLASSIFIED // CUI // Defense Research Baseline", body_style)],
        [Paragraph("<b>Digital Provenance Invariant:</b> <code>HW_KEY_0x889_BSU_DAS_2026_EDR</code>", code_style)]
    ]
    t_meta = Table(meta_data, colWidths=[500])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#94A3B8'), spaceBefore=5, spaceAfter=10))

    # Catechism Content
    q_data = [
        ("1. What are you trying to do? (No Jargon Statement)", 
         "We are building a defense-grade Security Operations Center (SOC) artificial intelligence that cannot be tricked into leaking classified secrets or executing unauthorized actions. The system mathematically screens every single thought and decision <i>before</i> the AI outputs it, operates inside encrypted hardware vaults, and manages its own off-grid power and heat recovery for tactical deployment in hostile environments."),
        
        ("2. How is it done today, and what are the limits of current practice?",
         "• <b>Probabilistic Guardrails:</b> Current AI safety in SOCs relies on post-hoc filtering, RLHF, or system instructions. These methods are soft and probabilistic—adversarial prompt injections reliably bypass them, leading to a non-zero probability of CUI leakage (P_violation > 0).<br/>"
         "• <b>Separated Hardware Isolation:</b> Existing architectures treat software TEEs and vector databases as disconnected layers, leaving embeddings vulnerable to inversion attacks.<br/>"
         "• <b>Grid Dependency:</b> High-performance AI hardware clusters require fixed commercial power grids with no integrated thermal or microgrid adaptation for expeditionary edge posts."),
        
        ("3. What is new in your approach and why do you think it will be successful?",
         "AEGIS-MONAD shifts AI safety from probabilistic filtering to <b>deterministic formal mathematical proof</b> integrated directly into token decoding:<br/><br/>"
         "• <b>Monad SMT Logit Transformation Operator:</b> Before softmax sampling, candidate logits L_i are constrained deterministically by a Z3 SMT logic solver graph:<br/>"
         "&nbsp;&nbsp;&nbsp;&nbsp;<b>L_hat_i = L_i + log Phi(v_i)</b><br/>"
         "Where Phi(v_i) evaluates to 1 if SMT_Verify(v_i) = SAT, and 0 if UNSAT. If a token violates security policy, log(0) = -infinity, reducing selection probability to <b>exactly zero (P_violation = 0)</b>.<br/><br/>"
         "• <b>Steganographic Provenance & Differential Privacy:</b> Vectors are perturbed via Gaussian noise bounded by (epsilon, delta)-DP and embedded with zero-width steganographic markers (U+200B/U+200C) bound to HW_KEY_0x889_BSU_DAS_2026_EDR.<br/><br/>"
         "• <b>Datacenter & Microgrid Telemetry Twin:</b> Real-time optimization balances compute draw against off-grid solar, battery reserves, and direct immersion heat capture using the Grid Isolation Index (GI)."),
        
        ("4. Who cares? If you are successful, what difference will it make?",
         "• <b>DoD & Intelligence Community:</b> Enables immediate, safe deployment of autonomous LLM agents in CUI/Classified environments without fear of prompt injection or data spillage.<br/>"
         "• <b>Expeditionary Command Posts:</b> Gives forward units an AI SOC command center capable of operating 90%+ off-grid while capturing compute exhaust heat to support local microgrids.<br/>"
         "• <b>Defense Industrial Base (DIB):</b> Establishes the nation's first hardware-attested, formally verified standard for AI governance."),
        
        ("5. What are the risks and the payoffs?",
         "• <b>Payoff:</b> The DoD acquires a provably secure, zero-violation AI reasoning and infrastructure framework—moving from reactive patch security to mathematical immunity.<br/>"
         "• <b>Risk & Mitigation (Latency):</b> Z3 SMT evaluation adds latency -> Enforce a 5ms thread-isolated timeout and parallelize SMT context checks across multi-threaded C++ workers.<br/>"
         "• <b>Risk & Mitigation (Memory Faults):</b> C++ native memory faults under concurrency -> Demonstrated thread-local z3.Context() isolation, eliminating cross-thread race conditions.")
    ]

    for title, text in q_data:
        story.append(Paragraph(f"<b>{title}</b>", h1_style))
        story.append(Paragraph(text, body_style))
        story.append(Spacer(1, 4))

    # Q6: Budget Table
    story.append(Paragraph("<b>6. How much will it cost?</b>", h1_style))
    story.append(Paragraph("<b>Total Program Budget: $32.0M over 36 months (3 Phases).</b>", body_style))
    
    budget_data = [
        ["Cost Category", "Phase I (M1-12)", "Phase II (M13-24)", "Phase III (M25-36)", "Total"],
        ["Formal Logic & Enclave R&D", "$4.5M", "$3.0M", "$1.5M", "$9.0M"],
        ["Hardware Enclave Testbed", "$3.5M", "$2.5M", "$1.0M", "$7.0M"],
        ["Microgrid & Thermal Twin", "$1.5M", "$4.0M", "$2.5M", "$8.0M"],
        ["Red Team Cyber Testing", "$0.5M", "$2.5M", "$5.0M", "$8.0M"],
        ["Total Program Cost", "$10.0M", "$12.0M", "$10.0M", "$32.0M"]
    ]
    t_budget = Table(budget_data, colWidths=[160, 85, 85, 85, 85])
    t_budget.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F1F5F9')),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_budget)
    story.append(Spacer(1, 8))

    # Q7 & Q8
    q_remaining = [
        ("7. How long will it take?",
         "<b>Total Duration: 36 Months.</b><br/>"
         "• <b>Phase I (Mos 1–12):</b> Formal Mathematical Proofs, Z3 SMT C++ acceleration (<2ms), AMD SEV-SNP attestation.<br/>"
         "• <b>Phase II (Mos 13–24):</b> Hardware Twin & Tactical Voice Deployment across Cerebras CS-4 & NVIDIA HGX clusters.<br/>"
         "• <b>Phase III (Mos 25–36):</b> Adversarial Red Teaming (100k automated prompt injections) & USCYBERCOM Transition."),
        
        ("8. What are the midterm and final 'exams' to check for success?",
         "• <b>Midterm Exam (Month 18):</b> Execute a 48-hour continuous stress test under 500 parallel thread sessions. Achieve P_violation = 0.0000% across 10,000,000 token decisions with GI > 0.85.<br/>"
         "• <b>Final Exam (Month 36 Operational Red Team):</b> Subject the system to an unconstrained 30-day Adversarial Red Team attack. Pass condition: 0 successful privilege escalations, 0 CUI token spillages, sub-10ms total decoding latency penalty, and 100% data provenance verification via HW_KEY_0x889_BSU_DAS_2026_EDR.")
    ]

    for title, text in q_remaining:
        story.append(Paragraph(f"<b>{title}</b>", h1_style))
        story.append(Paragraph(text, body_style))
        story.append(Spacer(1, 4))

    doc.build(story)
    print(f"[SUCCESS] PDF generated successfully: {filename}")

if __name__ == "__main__":
    create_darpa_pdf()
