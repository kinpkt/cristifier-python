from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyPDF2 import PdfReader, PdfWriter
import tempfile

# Register the font
pdfmetrics.registerFont(TTFont('THSarabunNew-Bold', 'THSarabunNew Bold.ttf'))

class PDFGenerator:
    def __init__(self, filename, data, comp_name, type):
        self.filename = filename
        self.data = data
        self.comp_name = comp_name
        self.type = type

    def create_pdf(self):
        pdf = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        elements = []
        table = self.create_table(self.data)
        elements.append(table)
        pdf.build(elements, onFirstPage=self.add_header, onLaterPages=self.add_header)

    def create_table(self, data):
        col_widths = [1*cm, 2.5*cm, 5*cm, 1.5*cm, 2*cm, 3*cm, 3*cm]

        # Prepare table data with Paragraph objects
        table_data = []
        for row in data:
            formatted_row = []
            for idx, cell in enumerate(row):
                if idx == 2:  # For the third column
                    formatted_cell = Paragraph(cell, self.get_paragraph_style('left'))
                else:
                    formatted_cell = Paragraph(cell, self.get_paragraph_style('center'))
                formatted_row.append(formatted_cell)
            table_data.append(formatted_row)

        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        # Add style
        style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'THSarabunNew-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),  # Left align third column content
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)
        return table

    def get_paragraph_style(self, alignment):
        return ParagraphStyle(
            name='Normal',
            fontName='THSarabunNew-Bold',
            fontSize=12,
            alignment={'left': 0, 'center': 1}[alignment]  # 0 for left, 1 for center
        )

    def add_header(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('THSarabunNew-Bold', 16)
        canvas.drawString(2*cm, A4[1] - 30, f'{self.comp_name} - Registration Paper ({self.type}) Page {canvas.getPageNumber()}')
        canvas.restoreState()

def merge_pdfs(pdf_paths, output_path):
    pdf_writer = PdfWriter()

    for path in pdf_paths:
        pdf_reader = PdfReader(path)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    with open(output_path, 'wb') as out:
        pdf_writer.write(out)

def generate_pdf(comp_id, data):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as returner_file, tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as first_timer_file, tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as merged_file:
        returner_pdf = PDFGenerator(returner_file.name, data[2], data[0], 'Returners')
        first_timer_pdf = PDFGenerator(first_timer_file.name, data[1], data[0], 'First-timers')

        returner_pdf.create_pdf()
        first_timer_pdf.create_pdf()

        merge_pdfs([returner_file.name, first_timer_file.name], merged_file.name)

        return merged_file.name
