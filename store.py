from flask import Blueprint, render_template, request, session, jsonify
from db_connection import get_db_connection

store_bp = Blueprint('store', __name__)

@store_bp.route('/store', methods=['GET'])
def store():
    username = session.get('username')
    if not username:
        return jsonify({'message': 'User not logged in'}), 401
    
    finalBookList = fetch_all_books_data()
    return render_template('store.html', booksData=finalBookList)

def fetch_all_books_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM books"
        cursor.execute(query)

        booksData = cursor.fetchall()
        return booksData
    except Exception as e:
        print(e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@store_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if not request.is_json:
        return jsonify({'message': 'Invalid request format'}), 400

    try:
        book_data = request.json
        username = session.get('username')
        if not username:
            return jsonify({'message': 'User not logged in'}), 401

        book_id = book_data.get('id')
        if not book_id:
            return jsonify({'message': 'Book ID not provided'}), 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            check_query = "SELECT * FROM cart WHERE username = %s AND book_id = %s"
            cursor.execute(check_query, (username, book_id))
            existing_book = cursor.fetchone()
            
            if existing_book:
                return jsonify({'message': 'Book already in cart'}), 400
            
            query = "INSERT INTO cart(username, book_id) VALUES(%s, %s)"
            cursor.execute(query, (username, book_id))
            conn.commit()
        except Exception as e:
            return jsonify({'message': str(e)}), 500
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
        return jsonify({'message': 'Book added to cart successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@store_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if not request.is_json:
        return jsonify({'message': 'Invalid request format'}), 400

    try:
        book_data = request.json
        book_id = book_data.get('id')
        username = session.get('username')
        if not username:
            return jsonify({'message': 'User not logged in'}), 401

        if not book_id:
            return jsonify({'message': 'Book ID not provided'}), 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "DELETE FROM cart WHERE username = %s AND book_id = %s"
            cursor.execute(query, (username, book_id))
            conn.commit()
        except Exception as e:
            return jsonify({'message': str(e)}), 500
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
        return jsonify({'message': 'Book removed from cart successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
