from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)

NAVY = colors.HexColor("#1f2a44")
PRIMARY = colors.HexColor("#2d5be3")
MUTED = colors.HexColor("#64748b")
LIGHT_BG = colors.HexColor("#f7f9fc")
GREEN = colors.HexColor("#16a34a")
BORDER = colors.HexColor("#e5e7eb")
TEXT = colors.HexColor("#333333")

RIASEC_LABELS = {'R': 'Realistic', 'I': 'Investigative', 'A': 'Artistic', 'S': 'Social', 'E': 'Enterprising', 'C': 'Conventional'}
APTITUDE_LABELS = {'logical': 'Logical Reasoning', 'verbal': 'Verbal Ability', 'numerical': 'Numerical Ability'}


def _score_table(data):
    table = Table(data, colWidths=[100 * mm, 40 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return table


def generate_report_pdf(user, result, career_courses):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=22 * mm, bottomMargin=18 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
        title="CareerCompass Assessment Report",
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ReportTitle', fontSize=22, leading=26, textColor=NAVY, fontName='Helvetica-Bold', spaceAfter=4))
    styles.add(ParagraphStyle(name='HeaderSub', fontSize=13, leading=16, textColor=PRIMARY, fontName='Helvetica-Bold', spaceAfter=8))
    styles.add(ParagraphStyle(name='ReportMeta', fontSize=10.5, leading=14, textColor=MUTED, spaceAfter=12))
    styles.add(ParagraphStyle(name='SectionHeading', fontSize=14, leading=17, textColor=NAVY, fontName='Helvetica-Bold', spaceBefore=16, spaceAfter=8))
    styles.add(ParagraphStyle(name='CareerName', fontSize=13, leading=16, textColor=NAVY, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='MatchBadge', fontSize=9.5, leading=12, textColor=GREEN, fontName='Helvetica-Bold', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Body', fontSize=9.5, textColor=TEXT, leading=13, spaceAfter=4))
    styles.add(ParagraphStyle(name='CourseName', fontSize=10.5, leading=13, textColor=NAVY, fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=2))
    styles.add(ParagraphStyle(name='Small', fontSize=8.5, textColor=MUTED, leading=12, spaceAfter=4))
    styles.add(ParagraphStyle(name='OfferingName', fontSize=9.5, leading=12, textColor=NAVY, fontName='Helvetica-Bold', leftIndent=8, spaceBefore=5, spaceAfter=1))
    styles.add(ParagraphStyle(name='OfferingLine', fontSize=8.8, textColor=TEXT, leftIndent=8, leading=12, spaceAfter=1))
    styles.add(ParagraphStyle(name='OfferingLink', fontSize=8.8, textColor=PRIMARY, leftIndent=8, leading=12, spaceAfter=9))

    story = []

    story.append(Paragraph("CareerCompass", styles['ReportTitle']))
    story.append(Paragraph("Career Assessment Report", styles['HeaderSub']))
    story.append(Paragraph(
        f"Prepared for <b>{escape(user.name)}</b> &nbsp;|&nbsp; {escape(result.level)} Passout Track "
        f"&nbsp;|&nbsp; Generated on {result.created_at.strftime('%d %B %Y')}",
        styles['ReportMeta']
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER, spaceAfter=8))

    story.append(Paragraph("Interest Profile (RIASEC)", styles['SectionHeading']))
    riasec_data = [["Trait", "Score"]]
    for key, label in RIASEC_LABELS.items():
        riasec_data.append([label, f"{result.riasec_scores.get(key, 0)}%"])
    story.append(_score_table(riasec_data))

    story.append(Paragraph("Aptitude Scores", styles['SectionHeading']))
    apt_data = [["Skill", "Score"]]
    for key, label in APTITUDE_LABELS.items():
        apt_data.append([label, f"{result.aptitude_scores.get(key, 0)}%"])
    story.append(_score_table(apt_data))

    story.append(Paragraph("Your Top Career Matches", styles['SectionHeading']))

    for i, career in enumerate(result.recommended_careers, start=1):
        career_flowables = []

        header = Table(
            [[Paragraph(f"#{i}  {escape(career['name'])}", styles['CareerName']),
              Paragraph(f"{career['match_percent']}% match", styles['MatchBadge'])]],
            colWidths=[130 * mm, 30 * mm]
        )
        header.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        career_flowables.append(Spacer(1, 10))
        career_flowables.append(header)
        career_flowables.append(Paragraph(escape(career.get('description', '')), styles['Body']))

        courses = career_courses.get(career['career_id'], [])
        for course in courses:
            career_flowables.append(Paragraph(escape(course['course_name']), styles['CourseName']))
            career_flowables.append(Paragraph(escape(course['course_description']), styles['Small']))
            for offering in course['offerings']:
                career_flowables.append(Paragraph(f"<b>{escape(offering['college_name'])}</b>", styles['OfferingName']))
                career_flowables.append(Paragraph(escape(offering['address']), styles['OfferingLine']))
                career_flowables.append(Paragraph(
                    f"Contact: {escape(offering['contact'])} &nbsp;|&nbsp; Fees: {escape(offering['fees'])}",
                    styles['OfferingLine']
                ))
                career_flowables.append(Paragraph(
                    f"Apply: <link href='{offering['apply_link']}' color='#2d5be3'>{escape(offering['apply_link'])}</link>",
                    styles['OfferingLink']
                ))

        # Keep each full career card together so it never splits mid-block across a page
        story.append(KeepTogether(career_flowables))

    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "This report is generated by CareerCompass based on your assessment responses. "
        "Course fees are approximate and may change — please verify with the college directly before applying.",
        styles['Small']
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer