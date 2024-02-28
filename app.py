from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'user',
    'password': 'pass',
    'database': 'trailhead'
}

app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
app.config['MYSQL_DATABASE_DB'] = 'trailhead'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

def get_mysql_connection():
    return mysql.connector.connect(
        user=app.config['MYSQL_DATABASE_USER'],
        password=app.config['MYSQL_DATABASE_PASSWORD'],
        host=app.config['MYSQL_DATABASE_HOST'],
        database=app.config['MYSQL_DATABASE_DB']
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/customers')
def list_customers():

    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('customers.html', customers=customers)

@app.route('/products')
def list_products():
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('products.html', products=products)

@app.route('/invoices')
def list_invoices():
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Invoices')
    invoices = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('invoices.html', invoices=invoices)

@app.route('/returns')
def list_returns():
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Returns')
    returns = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('returns.html', returns=returns)

@app.route('/reviews')
def list_reviews():
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Reviews')
    reviews = cursor.fetchall()
    cursor.execute("SELECT customerID FROM Customers")
    customer_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT productID FROM Products")
    product_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return render_template('reviews.html', reviews=reviews, customer_ids=customer_ids, product_ids=product_ids)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    customer_first_name = request.form['first_name']
    customer_last_name = request.form['last_name']
    customer_email = request.form['email']
    customer_address = request.form['address']
    customer_cell_phone = request.form['cell_phone']
    customer_home_phone = request.form['home_phone']
    is_premium_member = request.form.get('is_premium_member')
    is_premium_member = True if is_premium_member else False
    insert_query = "INSERT INTO Customers (nameFirst, nameLast, email, address, cellPhone, homePhone, isPremiumMember) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_data = (customer_first_name, customer_last_name, customer_email, customer_address, customer_cell_phone, customer_home_phone, is_premium_member)
    cursor.execute(insert_query, insert_data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/customers')

@app.route('/add_product', methods=['POST'])
def add_product():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    product_brand = request.form['product_brand']
    product_name = request.form['product_name']
    product_price = request.form['product_price']
    product_stock_quantity = request.form['product_stock_quantity']
    is_back_ordered = request.form.get('is_back_ordered')
    is_discontinued = request.form.get('is_discontinued')
    is_back_ordered = True if is_back_ordered else False
    is_discontinued = True if is_discontinued else False
    insert_query = "INSERT INTO Products (brand, productName, price, stockQty, backOrdered, discontinued) VALUES (%s, %s, %s, %s, %s, %s)"
    insert_data = (product_brand, product_name, product_price, product_stock_quantity, is_back_ordered, is_discontinued)
    cursor.execute(insert_query, insert_data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/products')

@app.route('/add_invoice', methods=['POST'])
def add_invoice():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    customer_id = request.form['customer_id']
    product_id = request.form['product_id']
    invoice_date = request.form['invoice_date']
    invoice_amount = request.form['invoice_amount']
    payment_method = request.form['payment_method']
    insert_query = "INSERT INTO Invoices (customerID, productID, invoiceDate, invoiceAmount, paymentMethod) VALUES (%s, %s, %s, %s, %s)"
    insert_data = (customer_id, product_id, invoice_date, invoice_amount, payment_method)
    cursor.execute(insert_query, insert_data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/invoices')

@app.route('/add_return', methods=['POST'])
def add_return():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    customer_id = request.form['customer_id']
    invoice_id = request.form['invoice_id']
    product_id = request.form['product_id']
    insert_query = "INSERT INTO Returns (customerID, invoiceID, productID) VALUES (%s, %s, %s)"
    insert_data = (customer_id, invoice_id, product_id)
    cursor.execute(insert_query, insert_data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/returns')

@app.route('/add_review', methods=['POST'])
def add_review():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    customer_id = request.form['customer_id']
    product_id = request.form['product_id']
    review_text = request.form['review_text']
    star_rating = request.form['star_rating']
    insert_query = "INSERT INTO Reviews (customerID, productID, reviewText, starRating) VALUES (%s, %s, %s, %s)"
    insert_data = (customer_id, product_id, review_text, star_rating)
    cursor.execute(insert_query, insert_data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/reviews')

@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def customer_detail(customer_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers WHERE customerID = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_customer.html', customer=customer)
    except mysql.connector.Error as err:
        return f"Error accessing database: {err}"

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products WHERE productID = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_product.html', product=product)

    except mysql.connector.Error as err:
        return f"Error accessing database: {err}"

@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
def review_detail(review_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reviews WHERE reviewID = %s", (review_id,))
        review = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_review.html', review=review)

    except mysql.connector.Error as err:
        return f"Error accessing database: {err}"


@app.route('/edit_invoice/<int:invoice_id>', methods=['GET', 'POST'])
def invoice_detail(invoice_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Invoices WHERE invoiceID = %s", (invoice_id,))
        invoice = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_invoice.html', invoice=invoice)

    except mysql.connector.Error as err:
        return f"Error accessing database: {err}"
        
@app.route('/edit_return/<int:return_id>', methods=['GET', 'POST'])
def return_detail(return_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Returns WHERE returnID = %s", (return_id,))
        return_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_return.html', return_data=return_data)

    except mysql.connector.Error as err:
        return f"Error accessing database: {err}"

@app.route('/delete_product', methods=['GET'])
def delete_product():
    product_id = request.args.get('product_id')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    delete_query = 'DELETE FROM Products WHERE productID = %s'
    cursor.execute(delete_query, (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/products') 
 
@app.route('/delete_customer', methods=['GET'])
def delete_customer():
    customer_id = request.args.get('customer_id')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    delete_query = 'DELETE FROM Customers WHERE customerID = %s'
    cursor.execute(delete_query, (customer_id,))
    conn.commit()  
    cursor.close()
    conn.close()
    return redirect('/customers')

@app.route('/delete_invoice', methods=['GET'])
def delete_invoice():
    invoice_id = request.args.get('invoice_id')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    delete_query = 'DELETE FROM Invoices WHERE invoiceID = %s'
    cursor.execute(delete_query, (invoice_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/invoices')

@app.route('/delete_review', methods=['GET'])
def delete_review():
    review_id = request.args.get('review_id')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    delete_query = 'DELETE FROM Reviews WHERE reviewID = %s'
    cursor.execute(delete_query, (review_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/reviews')

@app.route('/delete_return', methods=['GET'])
def delete_return():
    return_id = request.args.get('return_id')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    delete_query = 'DELETE FROM Returns WHERE returnID = %s'
    cursor.execute(delete_query, (return_id,))
    conn.commit() 
    cursor.close()
    conn.close()
    return redirect('/returns') 

@app.route('/update_customer', methods=['POST'])
def update_customer():
    try:
        customer_ID = request.form['customer_ID']
        customer_first_name = request.form['customer_first_name']
        customer_last_name = request.form['customer_last_name']
        customer_address = request.form['customer_address']
        customer_email = request.form['customer_email']
        customer_is_premium_member = 'customer_is_premium_member' in request.form
        customer_cell_phone = request.form['customer_cell_phone']
        customer_home_phone = request.form['customer_home_phone']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        update_query = """
            UPDATE Customers
            SET nameFirst = %s, nameLast = %s, address = %s, email = %s, isPremiumMember = %s, cellPhone = %s, homePhone = %s
            WHERE customerID = %s
        """
        cursor.execute(update_query, (customer_first_name, customer_last_name, customer_address, customer_email, customer_is_premium_member, customer_cell_phone, customer_home_phone, customer_ID))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/customers')
    except mysql.connector.Error as err:
        return f"Error updating customer: {err}"
 
@app.route('/update_product', methods=['POST'])
def update_product():
    try:
        
        product_id = request.form['product_id']
        product_brand = request.form['product_brand']
        product_name = request.form['product_name']
        product_price = request.form['product_price']
        product_stock_quantity = request.form['product_stock_quantity']
        is_back_ordered = 'is_back_ordered' in request.form
        is_discontinued = 'is_discontinued' in request.form
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        update_query = """
            UPDATE Products
            SET brand = %s, productName = %s, price = %s, stockQty = %s, backOrdered = %s, discontinued = %s
            WHERE productID = %s
        """
        cursor.execute(update_query, (product_brand, product_name, product_price, product_stock_quantity, is_back_ordered, is_discontinued, product_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/products')
    except mysql.connector.Error as err:
        return f"Error updating product: {err}"

@app.route('/update_invoice', methods=['POST'])
def update_invoice():
    try:
        
        invoice_id = request.form['invoice_id']
        customer_id = request.form['customer_id']
        product_id = request.form['product_id']
        invoice_date = request.form['invoice_date']
        invoice_amount = request.form['invoice_amount']
        payment_method = request.form['payment_method']
  
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        update_query = """
            UPDATE Invoices
            SET customerID = %s, productID = %s, invoiceDate = %s, invoiceAmount = %s, paymentMethod = %s
            WHERE invoiceID = %s
        """
        cursor.execute(update_query, (customer_id, product_id, invoice_date, invoice_amount, payment_method, invoice_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/invoices')
    except mysql.connector.Error as err:
        return f"Error updating invoice: {err}"

@app.route('/update_review', methods=['POST'])
def update_review():
    try:
        
        review_id = request.form['review_id']
        customer_id = request.form['customer_id']
        product_id = request.form['product_id']
        review_text = request.form['review_text']
        star_rating = request.form['star_rating']
  
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        update_query = """
            UPDATE Reviews
            SET customerID = %s, productID = %s,  reviewText = %s, starRating = %s
            WHERE reviewID = %s
        """
        cursor.execute(update_query, (customer_id, product_id, review_text, star_rating, review_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/reviews')
    except mysql.connector.Error as err:
        return f"Error updating review: {err}"

@app.route('/update_return', methods=['POST'])
def update_return():
    try:
        
        return_id = request.form['return_id']
        customer_id = request.form['customer_id']
        invoice_id = request.form['invoice_id']
        product_id = request.form['product_id']
  
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        update_query = """
            UPDATE Returns
            SET customerID = %s, productID = %s, invoiceID = %s
            WHERE returnID = %s
        """
        cursor.execute(update_query, (customer_id, product_id, invoice_id, return_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/returns')
    except mysql.connector.Error as err:
        return f"Error updating return: {err}"

@app.route('/customer_detail', methods=['GET', 'POST'])
def search_customer_detail():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        if customer_id:
            try:
                conn = get_mysql_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT *
                    FROM Customers
                    WHERE customerID = %s
                ''', (customer_id,))
                customer = cursor.fetchone()
                cursor.execute('''
                    SELECT *
                    FROM Invoices
                    WHERE customerID = %s
                ''', (customer_id,))
                invoices = cursor.fetchall()

                cursor.execute('''
                    SELECT *
                    FROM Returns
                    WHERE customerID = %s
                ''', (customer_id,))
                returns = cursor.fetchall()

                cursor.close()
                conn.close()

                return render_template('customer_detail.html', customer=customer, invoices=invoices, returns=returns)
            except mysql.connector.Error as err:
                return f"Error accessing database: {err}"
        else:
            return "Customer ID not provided."
    else:
        return render_template('customer_search.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=True)

