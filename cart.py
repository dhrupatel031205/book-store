from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_connection import get_db_connection

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'username' not in session:
        return redirect(url_for('auth.login'))  
    
    username = session['username']
    cart_data = send_cart_data(username)
    return render_template('cart.html', cartData=cart_data)

def fetch_cart_data(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM cart WHERE username = %s"
        cursor.execute(query, (username,))
        
        cart_data = cursor.fetchall()
        
        return cart_data
    except Exception as e:
        print(f"Error fetching cart data: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def fetch_book_data(book_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM books WHERE id = %s"
        cursor.execute(query, (book_id,))
        book_data = cursor.fetchone()  
        return book_data
    except Exception as e:
        print(e)
        return None 
    finally:
        cursor.close()
        conn.close()


def send_cart_data(username):
    book_list = fetch_cart_data(username)
    final_cart = []
    
    for b in book_list:
        book = fetch_book_data(b[0][2])  # Assuming book_id is in index 2
        print("Hello",book)
        
        if book:  # Ensure book is not None
            final_cart.append(book)
        else:
            print(f"Warning: Book with ID {b[2]} not found!")
    
    return final_cart
@cart_bp.route('/checkout', methods=['GET'])
def checkout():
    username = session['username']
    cart_data = fetch_cart_data(username)

    if not cart_data:  # Ensure cart is not empty
        flash("Your cart is empty. Add books before checkout!", "warning")
        return redirect(url_for('cart.cart'))  # Redirect back to cart
    
    total_price = 0
    for b in cart_data:
        if len(b) > 3:  # Ensure there is a valid index 3
            total_price += b[3]
        else:
            print(f"Error: Unexpected cart data structure: {b}")

    return render_template('bill.html', cartData=cart_data, total=total_price)

def cart_book_id(username) :
    books = []
    books_list = fetch_cart_data(username)
    for b in books_list :
        books.append(b[1])
    return books

def generate_bill(username):
    bill = 0
    books_list = fetch_cart_data(username)
    for b in books_list:
        bill += b[3] 
    return bill
