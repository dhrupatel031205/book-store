from flask import Blueprint, render_template, request, redirect, url_for, session,jsonify
from db_connection import get_db_connection

store_bp = Blueprint('store', __name__)

@store_bp.route('/store', methods=['GET', 'POST'])
def store():
    booksData = fetch_store_data()
    return render_template('store.html',booksData = booksData)

def fetch_store_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM books"
        cursor.execute(query)
        data = cursor.fetchall()

        return data
    
    except Exception as e :
        return e 

    finally :
        cursor.close()
        conn.close()


@store_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    book_data = request.get_json()
    addToCartDB(book_data)
    return jsonify({'message': 'Book added to cart successfully','book' : book_data}), 200

def addToCartDB(book) :
    username = session['username']
    try:
        conn = get_db_connection()    
        cursor = conn.cursor()

        query = 'INSERT INTO cart(username,book_id) VALUES (%s,%s)'
        cursor.execute(query,(username,book['id']))
        
        conn.commit()

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()