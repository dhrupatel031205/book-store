from flask import Blueprint, render_template, request, redirect, url_for, session
from db_connection import get_db_connection
from cart import fetch_book_data

aboutus_bp = Blueprint('aboutus', __name__)

@aboutus_bp.route('/profile', methods=['GET', 'POST'])
def aboutus():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirect if not logged in

    user = fetch_user_data(username)
    order = orders(username)
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
        userdata = cursor.fetchall()
        
        return userdata
    except Exception as e:
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def orders(username):
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "SELECT order_id, book_id, qty, bill_amount, order_date FROM orders WHERE username = %s ORDER BY order_date DESC"
        cursor.execute(query, (username,))
        orders = cursor.fetchall()
        return orders
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        