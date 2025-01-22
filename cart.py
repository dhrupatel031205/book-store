from flask import Blueprint, render_template, request, redirect, url_for,session
from db_connection import get_db_connection
from store import stackFetch,fetch_all_books_data
cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    username = session['username']
    cart_data = fetch_cart_data(username)
    final_cart_data = send_cart_data(cart_data)
    return render_template('cart.html',cartData = final_cart_data)

def fetch_cart_data(username) :
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM cart WHERE username = %s"
        cursor.execute(query,(username,))
        
        cart_data = cursor.fetchall()

        return cart_data
    except Exception as e :
        return e

    finally :
        cursor.close()
        conn.close()


def fetch_book_data(book_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM books WHERE id = %s"
        cursor.execute(query,(book_id,))

        booksData = cursor.fetchall()
        return booksData
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def send_cart_data(cart) :
    final_cart = []
    for bookC in cart :
        book = fetch_book_data(bookC[2])
        final_cart.append(book)
    return final_cart