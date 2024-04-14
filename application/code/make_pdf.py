"""
Generates a PDF file containing pictures and tables.
"""

from reportlab.pdfbase import pdfmetrics  # Register font
from reportlab.pdfbase.ttfonts import TTFont  # Font class
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image  # Classes related to report content
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # Text styles
from reportlab.lib import colors  # Color module
from reportlab.lib.units import inch  # Unit: inch

from numpy import isnan


# Registering a font named 'futura' with the file 'futura.ttf'.
# pdfmetrics.registerFont(TTFont('helvetica', 'helvetica.ttf'))
pdfmetrics.registerFont(TTFont('futura', 'futura.ttf'))

# Getting a list of styles that can be used in the document.
style_list = getSampleStyleSheet()
print(style_list)


class BuildPDF:
    def __init__(self, page_weight=595.27, page_height=841.889, page_margin=0.5*inch,
                 text_font='futura', heading_text_font='futura',
                 main_title_size=20, sub_title_size=10, heading1_size=15, heading2_size=13, text_size=10,
                 line_space=2, table_text_size=(10, 8), table_col_weight=120, img_size=(6*inch,4*inch)):

        self.weight = page_weight  # Limit of PDF width
        self.height = page_height  # Limit of PDF height
        self.margin = page_margin  # Set PDF margins

        self.font_heading = heading_text_font  # Title font
        self.font_body = text_font  # Body text font

        self.main_title_size = main_title_size  # Main title size
        self.sub_title_size = sub_title_size  # Subtitle size
        self.heading1_size = heading1_size  # Heading 1 size
        self.heading2_size = heading2_size  # Heading 2 size
        self.text_size = text_size  # Text size
        self.space = line_space  # Spacing between each module

        self.table_text_size = table_text_size  # Table text size, format is (title size, content size)
        self.table_col_weight = table_col_weight  # Table width

        self.img_size = img_size  # Image size, format is (width, height)
        self.sub_nums = 1

        self.pdf_ = list()

    def insert_main_title(self, title_name=None):
        """
        Insert main title
        """
        font_ = style_list['Title']
        font_.fontName = self.font_heading
        font_.fontSize = self.main_title_size
        font_.spaceAfter = self.space * 10
        font_.textColor = colors.black
        font_.alignment = 1
        font_.bold = True

        self.pdf_.append(Paragraph(title_name, font_))

    def insert_sub_title(self, title_name=None):
        """
        Insert sub-title
        """
        font_ = style_list['Title']
        font_.fontName = self.font_heading
        font_.fontSize = self.sub_title_size
        font_.spaceAfter = self.space * 5
        font_.textColor = colors.black
        font_.alignment = 1
        font_.bold = True
            
        self.pdf_.append(Paragraph(title_name, font_))

    def insert_heading1(self, text=None):
        """
        insert Heading 1
        """
        font_ = style_list['Heading1']
        font_.fontName = self.font_heading
        font_.fontSize = self.heading1_size
        font_.spaceAfter = self.space
        font_.textColor = colors.black
        font_.alignment = 0
        font_.bold = True

        self.pdf_.append(Paragraph(text, font_))

    def insert_heading2(self, text=None):
        """
        insert Heading 1
        """
        font_ = style_list['Heading2']
        font_.fontName = self.font_heading
        font_.fontSize = self.heading2_size
        font_.spaceAfter = self.space
        font_.textColor = colors.black
        font_.alignment = 0
        font_.bold = True

        self.pdf_.append(Paragraph(text, font_))

    def insert_text(self, text=None, font_color=colors.black):
        """
        Insert text
        Default is black, if font_color is provided, it will be set accordingly.
        """
        font_ = style_list['Normal']
        font_.fontName = self.font_body
        font_.fontSize = self.text_size
        font_.wordWrap = 'None'  # Set the text wrapping mode to English mode
        font_.alignment = 4  # Set the text alignment to justified
        font_.firstLineIndent = 24
        font_.leading = self.text_size*1.5
        font_.spaceAfter = self.space
        font_.textColor = font_color

        self.pdf_.append(Paragraph(text, font_))

    def insert_image(self, image_path=None, chg_pct=None):
        """
        Insert image
        By default, use the set size; if chg_pct is provided, scale accordingly
        """
        if chg_pct:
            img = Image(image_path, width=chg_pct*100, height=chg_pct*100, kind='percentage')
        else:
            img = Image(image_path)
            img.drawWidth = self.img_size[0]
            img.drawHeight = self.img_size[1]
        self.pdf_.append(img)

        caption_style = ParagraphStyle(
            name='ImageCaption',
            fontName='futura',
            fontSize=self.text_size,
            textColor=colors.black,
            alignment=1,
            leading=self.text_size * 1.5,
            spaceBefore=self.space,
            spaceAfter=self.space * 5
        )
        caption_text = f"Figure{self.sub_nums}"
        self.pdf_.append(Paragraph(caption_text, caption_style))
        self.sub_nums += 1

    def insert_table(self, input, args):
        """
        Insert table
        input -> title: Title row
        input -> values： Content rows
        """
        if input == 'title':
            style = [
                ('FONTNAME', (0, 0), (-1, 0), self.font_body),  # Set font for the first row
                ('LEADING', (0, 0), (-1, 0), self.table_text_size[0]*1.5),  # Set length of the first row cells
                ('FONTSIZE', (0, 0), (-1, 0), self.table_text_size[0]),  # Set font size for the first row
                ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),  # Set background color for the first row
            ]
            colWidths = self.table_col_weight
            spaceAfter = 0  # Connect with content rows, no space
            self.sub_nums += 1

        else:
            style = [
                ('FONTNAME', (0, 0), (-1, -1), self.font_body),  # Font for rows 2 to the last row
                ('FONTSIZE', (0, 0), (-1, -1), self.table_text_size[1]),  # Font size for rows 2 to the last row
            ]
            colWidths = self.table_col_weight/len(args[0])
            spaceAfter = self.space
        
        style += [('ALIGN', (0, 0), (-1, -1), 'CENTER'),   # Align all cells in the table horizontally
                  ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Align all cells in the table vertically
                  ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Set text color in the table
                  ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Set table grid color to grey with line width of 0.5
                  ]
        
        table = Table(args, colWidths=colWidths, style=style, spaceAfter=spaceAfter)

        self.pdf_.append(table)

    def normal_format(self, value, multiply = 1):
        """
        Normalize data format
        """
        if isinstance(value, float):
            if isnan(value):
                icell = ''
            else:
                icell = str(round(value * multiply, 2))
        elif isinstance(value, str):
            icell = value
        else:
            icell = str(value)

        return icell
    
    def export_pdf(self, file_dir):
        """
        Output file according to the required length of PDF
        """
        doc = SimpleDocTemplate(file_dir, pagesize=(self.weight, self.height),
                                leftMargin=self.margin, rightMargin=self.margin,
                                topMargin=self.margin, bottomMargin=self.margin)
        doc.build(self.pdf_)

    def export_test(self):
        """
        Test output effect
        """

        self.pdf_ = list()

        self.insert_main_title('Financial Market Report')
        self.insert_sub_title('2024-04-14')
        self.insert_text('This report is written for weekly/monthly review of the Financial Market in China.')
        self.export_pdf('Financial Market Report.pdf')
        

if __name__ == '__main__':
    file = BuildPDF()
    file.export_test()