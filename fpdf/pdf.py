from fpdf import FPDF

import csv
from fpdf import FPDF


class PDF(FPDF):

    def colored_table(self, headings, rows, col_widths=(47.5, 47.5, 47.5, 47.5)):
        # Colors, line width and bold font:
        self.set_fill_color(220, 220, 220)
        self.set_text_color(0)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)
        self.set_font(style="B", size=10, family="helvetica")
        for col_width, heading in zip(col_widths, headings):
            self.cell(col_width, 10, heading, border=0, align="C", fill=True)
        self.ln()
        # Color and font restoration:
        self.set_fill_color(220, 220, 220)
        self.set_text_color(0)
        self.set_font("helvetica")
        fill = False
        for row in rows:
            self.cell(col_widths[0], 6, row[0], border="B", align="L", fill=fill)
            self.cell(col_widths[1], 6, row[1], border="B", align="C", fill=fill)
            self.cell(col_widths[2], 6, row[2], border="B", align="C", fill=fill)
            self.cell(col_widths[3], 6, row[3], border="B", align="C", fill=fill)
            self.ln()
            fill = not fill
        self.cell(sum(col_widths), 0, "", "T")
    def header(self):
        # Rendering logo:
        self.image("builders.jpg", 10, 8, 33)
        # Setting font: helvetica bold 15
        self.set_font("helvetica", "B", 15)
        # Moving cursor to the right:
        self.cell(80)
        # Printing title:
        self.cell(30, 10, "Builder's Co", border=0, align="C")
        # Performing a line break:
        self.ln(20)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def load_data_from_csv(csv_filepath):
    headings, rows = [], []
    with open(csv_filepath, encoding="utf8") as csv_file:
        for row in csv.reader(csv_file, delimiter=","):
            if not headings:  # extracting column names from first row:
                headings = row
            else:
                rows.append(row)
    return headings, rows
def parameters_(a, b):
    headings = a
    rows = b
    return headings, rows


titles = ['Items', 'Price', 'Quantity', 'Amount'] 
content = [['Thermal Printer', 120000, 2, 240000.0], ['Fire HD 10', 500000, 2, 1000000.0]]
f = open("output.txt", "w")
f.write(f"{titles[0]},{titles[1]},{titles[2]},{titles[3]}\n")
for i in range(len(content)):
    f.write(f"{content[i][0]},{content[i][1]},{content[i][2]},{content[i][3]}\n")
f.close()


col_names, data = load_data_from_csv("output.txt")
print(col_names)
print(data)
pdf = PDF()
pdf.set_font("helvetica", size=14)
pdf.add_page()
pdf.set_fill_color(220, 220, 220)
pdf.set_text_color(0)
pdf.set_draw_color(0, 0, 0)
pdf.set_line_width(0.3)
pdf.set_font(style="B", size=16, family="helvetica")
pdf.cell(0, 10, "Invoice", border=0, align="C", fill=True)
pdf.ln()
pdf.set_font("helvetica", "", 10)
pdf.cell(120, 10, "To:", align="L")
pdf.cell(80, 10, "Bill No:", align="L")
pdf.ln(5)
pdf.cell(120, 10, "Kitaka", align="L")
pdf.cell(80, 10, "Date:", align="L")
pdf.ln(5)
pdf.cell(0, 10, "Kampala")
pdf.ln(5)
pdf.cell(0, 10, "+256784980479")
pdf.ln(5)
pdf.cell(0, 10, "kitakaedwin@gmail.com")
pdf.ln()
pdf.colored_table(col_names, data)
pdf.ln(0)
pdf.set_fill_color(220, 220, 220)
pdf.set_text_color(0)
pdf.set_draw_color(0, 0, 0)
pdf.set_line_width(0.3)
pdf.set_font(style="B", size=10, family="helvetica")
pdf.cell(100, 5, "", align="L")
pdf.cell(90, 5, "TOTAL", border=0, align="L", fill=True)
pdf.ln(5)
pdf.set_font(style="", size=10, family="helvetica")
pdf.cell(100, 5, "", align="L")
pdf.cell(90, 5, "Amount in words:", border=0, align="L", fill=False)
pdf.ln(7)
pdf.cell(100, 5, "", align="L")
pdf.cell(90, 5, "Builder's Co", border=0, align="R", fill=False)
pdf.ln()
pdf.line(x1=160, y1=120, x2=200, y2=120)
pdf.ln(5)
pdf.cell(100, 5, "", align="L")
pdf.cell(90, 20, "Authorized Signatory", border=0, align="R", fill=False)
pdf.output("tuto5.pdf")
