from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_connection import get_db_connection

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'username' not in session:
        return redirect(url_for('auth.login'))  
    
    username = session.get('username')
    cart_data = fetch_cart_details(username)
    
    session['cartData'] = cart_data if cart_data else []
    cart_t = total_cart_rate()
    return render_template('cart.html', cartData=session['cartData'],total = cart_t)

def fetch_cart_data(username):
    """Fetch all items from the cart table for the given username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT book_id, quantity FROM cart WHERE username = %s"
        cursor.execute(query, (username,))
        return cursor.fetchall()  # Returns a list of (book_id, quantity)
    except Exception as e:
        print(f"Error fetching cart data: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def fetch_book_data(book_id):
    """Fetch book details from the books table based on book_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM books WHERE id = %s"
        cursor.execute(query, (book_id,))
        return cursor.fetchone()  # Returns (id, title, author, price)
    except Exception as e:
        print(f"Error fetching book data: {e}")
        return None 
    finally:
        cursor.close()
        conn.close()

cart_total = []
def fetch_cart_details(username):
    """Fetch complete cart details with book data and quantities."""
    cart_items = fetch_cart_data(username)
    cart_details = []
    for book_id, quantity in cart_items:
        book = fetch_book_data(book_id)
        if book:
            cart_total.append(book[3] * quantity)
            book_dict = {
                'id': book[0],
                'title': book[1],
                'author': book[2],
                'price': float(book[3]),
                'quantity': quantity,
                'total_price': float(book[3]) * quantity,
                'img' : book[5]
            }
            cart_details.append(book_dict)
        else:
            print(f"Warning: Book with ID {book_id} not found!")
    
    return cart_details

@cart_bp.route('/checkout', methods=['GET'])
def checkout():
    if 'username' not in session:
        flash("You need to log in to checkout!", "danger")
        return redirect(url_for('auth.login'))
    
    username = session.get('username')
    cart_t = total_cart_rate()
    cart_data = session["cartData"]


    if not cart_data:
        flash("Your cart is empty. Add books before checkout!", "warning")
        return redirect(url_for('cart.cart'))
    
    total_price = sum(item['total_price'] for item in cart_data)
    return render_template('bill.html', cartData=cart_data, total= cart_t)

def cart_book_ids(username):
    """Get a list of book IDs in the user's cart."""
    return [item['id'] for item in fetch_cart_details(username)]

def generate_bill(username):
    """Calculate the total price of books in the cart."""
    return sum(item['total_price'] for item in fetch_cart_details(username))

def total_cart_rate():
    """Calculate total price dynamically instead of relying on a global variable."""
    total = sum(item['total_price'] for item in session.get('cartData', []))
    session['total'] = total
    return total
