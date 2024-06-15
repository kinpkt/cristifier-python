from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Register the font
pdfmetrics.registerFont(TTFont('THSarabunNew', 'THSarabunNew.ttf'))
pdfmetrics.registerFont(TTFont('THSarabunNew-Bold', 'THSarabunNew Bold.ttf'))

class PDFWithTable:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

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
            for cell in row:
                formatted_cell = Paragraph(cell, self.get_paragraph_style())
                formatted_row.append(formatted_cell)
            table_data.append(formatted_row)

        table = Table(table_data, colWidths=col_widths)

        # Add style
        style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'THSarabunNew-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-2, -1), 'CENTER'),  # Center align first and second column
            ('ALIGN', (-1, 0), (-1, -1), 'LEFT'),   # Left align third column
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)
        return table

    def get_paragraph_style(self):
        return ParagraphStyle(
            name='Normal',
            fontName='THSarabunNew-Bold',
            fontSize=12,
        )

    def add_header(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('THSarabunNew-Bold', 16)
        canvas.drawString(2*cm, A4[1] - 30, f'Cubing at Paradise Park Bangkok 2024 - Registration Table Page {canvas.getPageNumber()} of {doc.page}')
        canvas.restoreState()

# Example data
data = [
    ['ID', 'WCA ID', 'Name', 'Gender', 'Country', 'Sign', 'Remark'],
    ['2', '2018PRON02', 'Phakinthorn Pronmongkolsuk', 'Male', 'Thailand', '', ''],
    ['1', '2009CHAI01', 'Tanai Chaikraveephand', 'Male', 'Thailand', '', ''],
    # Add more rows as needed
]

# Create PDF
pdf_creator = PDFWithTable('custom_table.pdf', data)
pdf_creator.create_pdf()
