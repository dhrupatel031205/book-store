from flask import Blueprint, render_template, request, redirect, url_for, session
from db_connection import get_db_connection
from cart import fetch_book_data

aboutus_bp = Blueprint('aboutus', __name__)

@aboutus_bp.route('/profile', methods=['GET', 'POST'])
def aboutus():
    username = session.get('username')
    if not username:
        return redirect(url_for('login')) 

    user = fetch_user_data(username)
    order = send_orders_data(username)  # Fetch detailed order data
    return render_template('aboutus.html', userdata=user, orders=order)


@aboutus_bp.route('/update_profile', methods=['POST'])
def update_profile():
    username = session['username']
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']

    conn = get_db_connection()
    cursor = conn.cursor()
    
    update_query = "UPDATE users SET name = %s, email = %s, address = %s WHERE username = %s"

    cursor.execute(update_query, (name, email, address, username))
    conn.commit()
    conn.close()

    return redirect(url_for('aboutus.aboutus'))

def fetch_user_data(username):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        userdata = cursor.fetchall()  # Use fetchone() instead of fetchall() for a single user
        
        return userdata
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def orders(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "SELECT * FROM orders WHERE username = %s"
        cursor.execute(query, (username,))
        orders = cursor.fetchall()
        return orders
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()

def fetch_book_data(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT book_name, book_price FROM books WHERE id = %s"
        cursor.execute(query, (id,))

        books_data = cursor.fetchone()  # Use fetchone() for a single book
        return books_data
    except Exception as e:
        print(e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def send_orders_data(username):
    order_details = orders(username)
    final_details = []

    for order in order_details:
        book_ids = [int(num) for num in order[2].split() if num.isdigit()]
        books_info = [fetch_book_data(book_id) for book_id in book_ids]
        
        order_info = {
            "order_id": order[0],
            "username": order[1],
            "qty" : order[3],
            "books": books_info,
            "total_price": sum(book[1] for book in books_info if book)  # Calculate total price
        }
        final_details.append(order_info)
    
    return final_details
