# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import mysql.connector
from mysql.connector import Error

# Create a Flask application instance
app = Flask(__name__)

'''This code creates a web application that allows users to view products, place orders, and manage their order quantities.
Database Connection: It connects to a MySQL database (Ordering_database) and creates necessary tables (products, orders, and order_items) if they do not already exist.'''

# MySQL connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '@Ftsvolvl9',  # Replace with your actual MySQL password
    'database': 'Ordering_database'  # Database name
}

# Function to connect to MySQL server without specifying a database
def create_server_connection():
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        if connection.is_connected():
            print("Connected to MySQL server")
        return connection
    except Error as e:
        print("Error while connecting to MySQL server:", e)
        return None

# Function to create the database if it doesn't exist
def create_database():
    connection = create_server_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Create the database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS Ordering_database")
            print("Database 'Ordering_database' created or already exists.")
        except Error as e:
            print("Error while creating database:", e)
        finally:
            cursor.close()
            connection.close()

# Function to connect to the specified database
def create_database_connection():
    try:
        # Establish a connection to the specified database
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to 'Ordering_database'")
        return connection
    except Error as e:
        print("Error while connecting to 'Ordering_database':", e)
        return None

# Function to initialize the database (create tables and insert example products)
def init_db():
    connection = create_database_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Create products table
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL
                )
            ''')

            # Create orders table
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_name VARCHAR(255) NOT NULL,
                    order_date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create order_items table
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT,
                    product_id INT,
                    quantity INT DEFAULT 1,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                )
            ''')

            # Insert example products if the table is empty
            cursor.execute('SELECT COUNT(*) FROM products')
            product_count = cursor.fetchone()[0]
            if product_count == 0:
                example_products = [
                    ('Product 1', 10.99),
                    ('Product 2', 15.49),
                    ('Product 3', 7.99),
                    ('Product 4', 20.00),
                    ('Product 5', 5.49)
                ]
                cursor.executemany('INSERT INTO products (name, price) VALUES (%s, %s)', example_products)
                print("Example products inserted successfully.")
            
            connection.commit()
            print("Tables created and example products inserted successfully (if they didn't exist).")

        except Error as e:
            print("Error while creating tables or inserting example products:", e)
        finally:
            cursor.close()
            connection.close()

# Home page displaying products
@app.route('/')
def index():
    connection = create_database_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('Order.html', products=products)

# Order page to add products to cart
@app.route('/order', methods=['POST'])
def order():
    customer_name = request.form['customer_name']
    selected_products = request.form.getlist('product_id')
    quantities = request.form.getlist('quantity')

    if not selected_products:
        return redirect(url_for('index'))

    # Insert order into orders table
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO orders (customer_name) VALUES (%s)', (customer_name,))
    order_id = cursor.lastrowid

    # Insert products into order_items table
    for product_id, quantity in zip(selected_products, quantities):
        cursor.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)', 
                       (order_id, product_id, quantity))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('order_summary', order_id=order_id))

# Order summary page
@app.route('/order_summary/<int:order_id>')
def order_summary(order_id):
    connection = create_database_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(''' 
        SELECT o.id, o.customer_name, p.name, oi.id AS order_item_id, oi.quantity, p.price, (oi.quantity * p.price) AS total_price 
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.id = %s
    ''', (order_id,))
    order_details = cursor.fetchall()
    cursor.close()
    connection.close()

    total_amount = sum(item['total_price'] for item in order_details)
    return render_template('order_summary.html', order_details=order_details, total_amount=total_amount)

# Increase quantity route
@app.route('/increase_quantity/<int:order_item_id>', methods=['POST'])
def increase_quantity(order_item_id):
    connection = create_database_connection()
    cursor = connection.cursor()

    # Update the quantity of the specific order item
    cursor.execute('UPDATE order_items SET quantity = quantity + 1 WHERE id = %s', (order_item_id,))
    connection.commit()

    cursor.close()
    connection.close()

    # Redirect to the order summary page after the update
    return redirect(request.referrer)

# Decrease quantity route
@app.route('/decrease_quantity/<int:order_item_id>', methods=['POST'])
def decrease_quantity(order_item_id):
    connection = create_database_connection()
    cursor = connection.cursor()

    # Update the quantity of the specific order item, ensuring it doesn't go below 1
    cursor.execute('UPDATE order_items SET quantity = GREATEST(quantity - 1, 1) WHERE id = %s', (order_item_id,))
    connection.commit()

    cursor.close()
    connection.close()

    # Redirect to the order summary page after the update
    return redirect(request.referrer)

# Main entry point of the application
if __name__ == '__main__':
    create_database()  # Create the database if it doesn't exist
    init_db()  # Initialize tables and insert example products
    app.run(debug=True)  # Run the Flask application in debug mode