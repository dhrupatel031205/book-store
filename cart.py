from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_connection import get_db_connection

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'username' not in session:
        return redirect(url_for('auth.login'))  
    
    username = session.get('username')
    cart_data = send_cart_data(username)
    
    session['cartData'] = cart_data if cart_data else []  # Ensure session key always has a value
    return render_template('cart.html', cartData=session['cartData'])

def fetch_cart_data(username):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM cart WHERE username = %s"
        cursor.execute(query, (username,))
        
        cart_data = cursor.fetchall()
        return cart_data if cart_data else []
    except Exception as e:
        print(f"Error fetching cart data: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_book_data(book_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM books WHERE id = %s"
        cursor.execute(query, (book_id,))
        book_data = cursor.fetchone()  
        return book_data if book_data else None
    except Exception as e:
        print(f"Error fetching book data: {e}")
        return None 
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def send_cart_data(username):
    book_list = fetch_cart_data(username)
    final_cart = []
    
    for b in book_list:
        book = fetch_book_data(b[2])  # Assuming book_id is in index 2
        if book:
            final_cart.append(book)
        else:
            print(f"Warning: Book with ID {b[2]} not found!")
    
    return final_cart if final_cart else []

@cart_bp.route('/checkout', methods=['GET'])
def checkout():
    username = session.get('username')
    if not username:
        flash("You need to log in to checkout!", "danger")
        return redirect(url_for('auth.login'))  # Redirect to login page

    cart_data = send_cart_data(username)

    if not cart_data:
        flash("Your cart is empty. Add books before checkout!", "warning")
        return redirect(url_for('cart.cart'))  

    total_price = sum(float(b[3]) for b in cart_data)

    return render_template('bill.html', cartData=cart_data, total=total_price)

def cart_book_id(username):
    books_list = fetch_cart_data(username)
    return [b[1] for b in books_list]

def generate_bill(username):
    books_list = fetch_cart_data(username)
    return sum(b[3] for b in books_list)
