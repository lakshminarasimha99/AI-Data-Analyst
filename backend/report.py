import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def create_pdf_report(filepath, chart_paths, predictions):
    os.makedirs("static", exist_ok=True)
    report_path = "static/report.pdf"

    df = pd.read_csv(filepath)

    # ── Styles ──────────────────────────────────────────────────────────────
    doc = SimpleDocTemplate(
        report_path, pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'],
        fontSize=22, textColor=colors.HexColor('#5B6EF5'),
        alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=11, textColor=colors.HexColor('#607090'),
        alignment=TA_CENTER, spaceAfter=18
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Heading2'],
        fontSize=13, textColor=colors.HexColor('#A78BFA'),
        spaceAfter=8, spaceBefore=16, fontName='Helvetica-Bold'
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#4A5568'),
        spaceAfter=4
    )

    story = []

    # ── Title block ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("AI Data Analyst Report", title_style))
    story.append(Paragraph(
        f"Dataset: <b>{os.path.basename(filepath)}</b> &nbsp;·&nbsp; "
        f"{df.shape[0]:,} rows &nbsp;·&nbsp; {df.shape[1]} columns",
        subtitle_style
    ))
    story.append(HRFlowable(
        width="100%", thickness=1,
        color=colors.HexColor('#5B6EF5'), spaceAfter=16
    ))

    # ── Dataset Summary ──────────────────────────────────────────────────────
    story.append(Paragraph("Dataset Summary", section_style))

    desc = df.describe().round(2)
    header_row = ['Column'] + list(desc.columns)
    table_data = [header_row]
    for stat in desc.index:
        row = [stat] + [str(desc.loc[stat, c]) for c in desc.columns]
        table_data.append(row)

    col_w = (6.5 * inch) / len(header_row)
    t = Table(table_data, colWidths=[col_w] * len(header_row), repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  colors.HexColor('#5B6EF5')),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  colors.white),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0),  8.5),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE',      (0, 1), (-1, -1), 8),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.HexColor('#F7F9FF'), colors.HexColor('#EEF1FB')]),
        ('GRID',          (0, 0), (-1, -1), 0.4, colors.HexColor('#D1D9F0')),
        ('ROWHEIGHT',     (0, 0), (-1, -1), 16),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)

    # ── Trend Predictions ────────────────────────────────────────────────────
    story.append(Paragraph("Trend Predictions (Linear Regression)", section_style))
    if predictions and not predictions.get('message'):
        pred_data = [['Column', 'Next Predicted Value', 'Direction']]
        for col, pred in predictions.items():
            if isinstance(pred, dict):
                pred_data.append([
                    col,
                    f"{pred['next_predicted']:.4f}",
                    '▲ Up' if pred['trend'] == 'up' else '▼ Down'
                ])
            else:
                pred_data.append([col, '—', pred])

        pt = Table(pred_data, colWidths=[2.5 * inch, 2 * inch, 2 * inch])
        pt.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, 0),  colors.HexColor('#8B5CF6')),
            ('TEXTCOLOR',     (0, 0), (-1, 0),  colors.white),
            ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
            ('FONTSIZE',      (0, 0), (-1, -1), 9),
            ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.HexColor('#F9F5FF'), colors.HexColor('#F3EEFF')]),
            ('GRID',          (0, 0), (-1, -1), 0.4, colors.HexColor('#DDD0F5')),
            ('ROWHEIGHT',     (0, 0), (-1, -1), 18),
            ('TOPPADDING',    (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(pt)
    else:
        story.append(Paragraph(
            predictions.get('message', 'No predictions available.'), body_style
        ))

    # ── Charts ───────────────────────────────────────────────────────────────
    story.append(Paragraph("Generated Charts", section_style))
    for chart in chart_paths:
        chart_fp = f"static/{chart}"
        if os.path.exists(chart_fp):
            story.append(Spacer(1, 0.1 * inch))
            img = Image(chart_fp, width=6 * inch, height=3.8 * inch)
            story.append(img)
            story.append(Spacer(1, 0.15 * inch))

    doc.build(story)
    return report_path
