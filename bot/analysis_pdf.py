# ✅ [3] analysis_pdf.py - النسخة الشاملة لتقرير PDF برسوم بيانية

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Image, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
import os

def generate_analysis_pdf_reportlab_en(results, output_path="uploaded/analysis_report.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    font_path = "fonts/DejaVuSans.ttf"
    pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='NormalDejaVu', fontName='DejaVu', fontSize=12))
    styles.add(ParagraphStyle(name='BoldDejaVu', fontName='DejaVu', fontSize=14, spaceAfter=10))

    elements = []
    elements.append(Paragraph("Data Analysis Report", styles['BoldDejaVu']))
    elements.append(Spacer(1, 12))

    summary = (
        f"- File Shape: {results['shape'][0]} rows × {results['shape'][1]} columns<br/>"
        f"- Numeric Columns: {len(results['numeric_cols'])}<br/>"
        f"- Text Columns: {len(results['text_cols'])}<br/>"
        f"- Date Columns: {len(results['date_cols'])}<br/>"
        f"- Cleaning applied: removed empty/constant/duplicate rows/columns, filled nulls.<br/>"
    )
    elements.append(Paragraph(summary, styles['NormalDejaVu']))
    elements.append(Spacer(1, 12))

    def build_table(data, title):
        elements.append(Paragraph(title, styles['BoldDejaVu']))
        data = [[str(cell) for cell in row] for row in data]
        table = Table(data, repeatRows=1, colWidths=[doc.width / len(data[0])] * len(data[0]))
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    stats = results['stats']
    transposed_stats = stats.transpose()
    transposed_stats.insert(0, 'Metric', transposed_stats.index)
    stats_data = [transposed_stats.columns.tolist()] + transposed_stats.values.tolist()
    build_table(stats_data, "Statistical Summary (Numeric Columns)")

    if results.get('chart_path'):
        elements.append(PageBreak())
        elements.append(Paragraph("Top Category Frequency", styles['BoldDejaVu']))
        elements.append(Spacer(1, 12))
        elements.append(Image(results['chart_path'], width=480, height=300))

    if results.get('corr_path'):
        elements.append(PageBreak())
        elements.append(Paragraph("Correlation Matrix (Numeric Columns)", styles['BoldDejaVu']))
        elements.append(Spacer(1, 12))
        elements.append(Image(results['corr_path'], width=500, height=350))

    # ✅ إضافة التنبؤ (إن وُجد)
    if results.get('prediction_result'):
        elements.append(PageBreak())
        elements.append(Paragraph("Prediction Summary", styles['BoldDejaVu']))
        elements.append(Spacer(1, 12))
        pred = results['prediction_result']
        text = (
            f"Target Column: <b>{pred['target']}</b><br/>"
            f"R² Score: <b>{pred['r2_score']}</b><br/><br/>"
            "Sample Predictions (Actual → Predicted):<br/>"
        )
        for actual, pred_val in pred['sample_prediction']:
            text += f"• {round(actual,2)} → {round(pred_val,2)}<br/>"
        elements.append(Paragraph(text, styles['NormalDejaVu']))
        elements.append(Spacer(1, 12))

    if results.get('prediction_chart_path'):
        elements.append(Image(results['prediction_chart_path'], width=480, height=300))

    doc.build(elements)
    return output_path
