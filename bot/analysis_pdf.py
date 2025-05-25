from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
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

    # Title
    elements.append(Paragraph("Data Analysis Report", styles['BoldDejaVu']))
    elements.append(Spacer(1, 12))

    # Summary
    summary = (
        "- The data file was successfully loaded.<br/>"
        "- Empty rows and columns were completely removed.<br/>"
        "- Missing values were filled with 0 or 'undefined' based on column type.<br/>"
        "- Statistical analysis was performed on numeric columns only.<br/>"
        "- A bar chart was generated for the most frequent categorical column.<br/>"
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

    # Nulls before
    nulls_before = results['nulls_before'].reset_index().values.tolist()
    nulls_before.insert(0, ["Column", "Missing Before"])
    build_table(nulls_before, "Missing Values Before Cleaning")

    # Nulls after
    nulls_after = results['nulls_after'].reset_index().values.tolist()
    nulls_after.insert(0, ["Column", "Missing After"])
    build_table(nulls_after, "Missing Values After Cleaning")

    # Stats table (transposed for better layout)
    stats = results['stats']
    transposed_stats = stats.transpose()
    transposed_stats.insert(0, 'Metric', transposed_stats.index)
    stats_data = [transposed_stats.columns.tolist()] + transposed_stats.values.tolist()
    build_table(stats_data, "Statistical Summary (Numeric Columns)")

    # Chart
    if results.get('chart_path'):
        elements.append(PageBreak())
        elements.append(Paragraph("Most Frequent Category Chart", styles['BoldDejaVu']))
        elements.append(Spacer(1, 12))
        elements.append(Image(results['chart_path'], width=500, height=300))

    doc.build(elements)
    return output_path
