from cs50 import SQL
import sys
from fpdf import FPDF
import csv
from num2words import num2words
import datetime


# Create database
#open("acc.db", "a").close()
db = SQL("sqlite:///acc.db")

# Create tables
#db.execute("CREATE TABLE clients (id INTEGER, name TEXT, address TEXT, phone NUMERIC UNIQUE, email TEXT UNIQUE, PRIMARY KEY(id))")
#db.execute("CREATE TABLE products(client_id INTEGER, product TEXT, quantity INTEGER, units TEXT, cost INTEGER, product_id INTEGER, PRIMARY KEY(product_id) FOREIGN KEY(client_id) REFERENCES clients(id))")
#db.execute("CREATE TABLE customers(client_id INTEGER, name TEXT NOT NULL, mobile TEXT, address TEXT NOT NULL, email TEXT, tin NUMERIC, bill REAL DEFAULT 0.0, customer_id INTEGER, PRIMARY KEY(customer_id) FOREIGN KEY(client_id) REFERENCES clients(id))")
#db.execute("CREATE TABLE categories(category TEXT, product_id INTEGER, FOREIGN KEY(product_id) REFERENCES products(product_id))")
#db.execute("CREATE TABLE transactions(customer_id INTEGER, product_id INTEGER, quantity INTEGER, transaction_id INTEGER, FOREIGN KEY(customer_id) REFERENCES customers(customer_id), FOREIGN KEY(product_id) REFERENCES products(product_id), PRIMARY KEY(transaction_id))")
class Business:

    def __init__(self, name, address, phone, email):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email

class Customer:

    def __init__(self, name, mobile, address, email, tin, bill=0.0):
        self.name = name
        self.mobile = mobile
        self.address = address
        self.email = email
        self.tin = tin
        self.bill = bill

    #def __str__(self):
        #return {"name": self.name, "mobile": self.mobile, "address": self.address, "email": self.email, "tin": self.tin, "bill": self.bill}

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
        client = client_(id_)
        self.cell(30, 10, client, border=0, align="C")
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
        for row in csv.reader(csv_file, delimiter="."):
            if not headings:  # extracting column names from first row:
                headings = row
            else:
                rows.append(row)
    return headings, rows

def main():
    global id_
    id_ = input("User ID: ")
    # Adding new business
    if len(sys.argv) == 1:
        name = input("Business Name: ")
        address = input("Business address: ")
        phone = input("Phone Number: ")
        email = input("Email address: ")
        new_user = Business(name, address, phone, email)
        db.execute("INSERT INTO clients (name, address, phone, email) VALUES(?, ?, ?, ?)", name, address, phone, email)
        user_id = db.execute("SELECT id FROM clients WHERE email = ?", email)
        print(f"Your User ID is {user_id}")

    if len(sys.argv) > 1:
        if sys.argv[1] == "newProduct":
            product = input("Product Name: ")
            quantity = input("Quantity: ")
            units = input("Units: ")
            cost = input("Product Cost: ")
            id_ = input("User ID: ")
            db.execute("INSERT INTO products (client_id, product, quantity, units, cost) VALUES(?, ?, ?, ?, ?)", id_, product, quantity, units, cost)

        if sys.argv[1] == "addStock":
            id_ = input("User ID: ")
            product = input("Product Name: ")
            product_id = get_productID(product, id_)
            quantity = int(input("Quantity: "))
            #Upddating product quantity of specific client(Business)
            product_stock = db.execute("SELECT quantity FROM products WHERE client_id = ? AND product_id = ?", id_, product_id)
            product_stock = product_stock[0]
            product_stock = int(product_stock["quantity"])
            new_stock = product_stock + quantity
            db.execute("UPDATE products SET quantity = ? WHERE client_id = ? AND product_id = ?", new_stock, id_, product_id)
        
        if sys.argv[1] == "addSale":
            x = datetime.datetime.now()
            x = x.strftime("%d/%m/%Y")
            counter = 0
            #id_ = input("User ID: ")
            mobile = input("Mobile Number: ")
            numbers = db.execute("SELECT mobile FROM customers")
            contacts = []
            for dict_ in numbers:
                contacts.append(dict_["mobile"])
            if mobile not in contacts:
                name = input("Customer Name: ")
                address = input("Address: ")
                email = input("Email: ")
                tin = input("TIN: ")
                new_customer = Customer(name, mobile, address, email, tin)
                db.execute("INSERT INTO customers (client_id, name, mobile, address, email, tin) VALUES (?, ?, ?, ?, ?, ?)", id_, name, mobile, address, email, tin)
                customer_id = get_customerID(mobile, id_)
                current_customer = {"name": new_customer.name, "mobile": new_customer.mobile, "address": new_customer.address, "email": new_customer.email, "tin": new_customer.tin, "bill": new_customer.bill}
                customer_carrier = current_customer
            else:
                current_customer = db.execute("SELECT name, mobile, address, email, tin, bill FROM customers WHERE mobile = ?", mobile)
                customer_id = get_customerID(mobile, id_)
                customer_carrier = current_customer
            content = []
            while True:
                if product := input("Add Product: "):
                    current_customer = customer_carrier
                    list1 = []
                    product_id = get_productID(product, id_)
                    prod = db.execute("SELECT product FROM products WHERE client_id = ? AND product_id = ?", id_, product_id)
                    products = []
                    for dict_ in prod:
                        products.append(dict_["product"])
                        if product in products:
                            quantity = int(input("Quantity: "))
                            #Upddating product quantity of specific client(Business)
                            product_stock = db.execute("SELECT quantity FROM products WHERE client_id = ? AND product_id = ?", id_, product_id)
                            product_stock = product_stock[0]
                            product_stock = int(product_stock["quantity"])
                            if quantity < product_stock:
                                new_stock = product_stock - quantity
                                db.execute("UPDATE products SET quantity = ? WHERE client_id = ? AND product_id = ?", new_stock, id_, product_id)
                                price = db.execute("SELECT cost FROM products WHERE client_id = ? AND product_id = ?", id_, product_id)
                                price = price[0]
                                price = price["cost"]
                                price = int(price)
                                bill = quantity * price
                                bill = float(bill)
                                current_customer = current_customer[0]
                                current_customer["bill"] = bill
                                current_invoice = current_customer
                                owed = db.execute("SELECT bill FROM customers WHERE client_id = ? AND customer_id = ?",id_, customer_id)
                                owed = owed[0]
                                owed = owed["bill"]
                                bill = owed + bill
                                db.execute("UPDATE customers SET bill = ? WHERE client_id = ? AND customer_id = ?", bill, id_, customer_id)
                                current_invoice["product"] = product
                                current_invoice["quantity"] = quantity
                                current_invoice["price"] = price
                                db.execute("INSERT INTO transactions(customer_id, product_id, quantity) VALUES(?, ?, ?)", customer_id, product_id, quantity)
                                counter += 1
                                list1 = [current_invoice["product"], current_invoice["price"], current_invoice["quantity"], current_invoice["bill"]]
                                content.append(list1)
                else:
                    break
            titles = ['Items', 'Price', 'Quantity', 'Amount'] 
            TOTAL = 0
            print(current_invoice)
            client = client_(id_)
            f = open("output.txt", "w")
            f.write(f"{titles[0]}.{titles[1]}.{titles[2]}.{titles[3]}\n")
            for i in range(len(content)):
                TOTAL += content[i][3]
                content[i][3] = "UGX {:,.0f}".format(content[i][3])
                content[i][1] = "UGX {:,.0f}".format(content[i][1])
                f.write(f"{content[i][0]}.{content[i][1]}.{content[i][2]}.{content[i][3]}\n")
                words = num2words(TOTAL)
                TOTAL = "UGX {:,.0f}".format(TOTAL)
            f.close()      
            # Printing Invoice
            col_names, data = load_data_from_csv("output.txt")
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
            pdf.cell(120, 10, current_invoice["name"], align="L")
            pdf.cell(80, 10, f"Date: {x}", align="L")
            pdf.ln(5)
            pdf.cell(0, 10, current_invoice["address"])
            pdf.ln(5)
            pdf.cell(0, 10, current_invoice["mobile"])
            pdf.ln(5)
            pdf.cell(0, 10, current_invoice["email"])
            pdf.ln()
            pdf.colored_table(col_names, data)
            pdf.ln(0)
            pdf.set_fill_color(220, 220, 220)
            pdf.set_text_color(0)
            pdf.set_draw_color(0, 0, 0)
            pdf.set_line_width(0.3)
            pdf.set_font(style="B", size=10, family="helvetica")
            pdf.cell(100, 5, "", align="L")
            pdf.cell(42.5, 5, "TOTAL: ", border=0, align="L", fill=True)
            pdf.cell(47.5, 5, TOTAL, border=0, align="C", fill=True)
            pdf.ln(5)
            pdf.set_font(style="", size=10, family="helvetica")
            pdf.cell(100, 5, "", align="L")
            pdf.cell(90, 5, f"Amount in words: {words.title()}", border=0, align="L", fill=False)
            pdf.ln(7)
            pdf.cell(100, 5, "", align="L")
            pdf.cell(90, 5, client, border=0, align="R", fill=False)
            pdf.ln()
            pdf.line(x1=160, y1=120, x2=200, y2=120)
            pdf.ln(5)
            pdf.cell(100, 5, "", align="L")
            pdf.cell(90, 30, "Authorized Signatory", border=0, align="R", fill=False)
            pdf.output("invoice.pdf")



def get_customerID(mobile, id_):
    customer_id = db.execute("SELECT customer_id FROM customers WHERE mobile = ? AND client_id = ?", mobile, id_)
    customer_id = customer_id[0]
    customer_id = customer_id["customer_id"]
    return customer_id   

def get_productID(product, id_):
    if product_id := db.execute("SELECT product_id FROM products WHERE product = ? AND client_id = ?", product, id_):
        product_id = product_id[0]
        product_id = product_id["product_id"]
        return product_id 
    else:
        sys.exit("Please add as New Product")          

def client_(id_):
    client = db.execute("SELECT name FROM clients WHERE id = ?", id_)
    client = client[0]
    client = client["name"]
    return client

if __name__=="__main__":
    main()