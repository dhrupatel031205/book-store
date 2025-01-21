from flask import Blueprint, render_template, request, redirect, url_for,session
from db_connection import get_db_connection

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    username = session['username']
    cart_data = fetch_cart_data(username)
    return render_template('cart.html',cart_data = cart_data)

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
