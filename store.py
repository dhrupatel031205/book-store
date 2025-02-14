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
        quantity = book_data.get('quantity', 1)  # Default to 1 if not provided

        if not book_id:
            return jsonify({'message': 'Book ID not provided'}), 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check available stock from books table
            qty_query = "SELECT qty FROM books WHERE id = %s"
            cursor.execute(qty_query, (book_id,))
            book_qty = cursor.fetchone()

            if not book_qty:
                return jsonify({'message': 'Book not found'}), 404

            available_qty = book_qty[0]

            if available_qty < quantity:
                return jsonify({'message': 'Not enough stock available'}), 400

            # Check if the book is already in the cart
            check_query = "SELECT quantity FROM cart WHERE username = %s AND book_id = %s"
            cursor.execute(check_query, (username, book_id))
            existing_book = cursor.fetchone()

            if existing_book:
                # If book is already in the cart, update the quantity
                new_quantity = existing_book[0] + quantity
                update_cart_query = "UPDATE cart SET quantity = %s WHERE username = %s AND book_id = %s"
                cursor.execute(update_cart_query, (new_quantity, username, book_id))
            else:
                # Insert new book with quantity
                insert_cart_query = "INSERT INTO cart(username, book_id, quantity) VALUES(%s, %s, %s)"
                cursor.execute(insert_cart_query, (username, book_id, quantity))

            # Decrease the quantity from books database
            update_qty_query = "UPDATE books SET qty = qty - %s WHERE id = %s"
            cursor.execute(update_qty_query, (quantity, book_id))

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
        book_id = book_data.get('id')  # Fix key mismatch
        username = session.get('username')

        if not username:
            return jsonify({'success': False, 'message': 'User not logged in'}), 401

        if not book_id:
            return jsonify({'success': False, 'message': 'Book ID not provided'}), 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "DELETE FROM cart WHERE username = %s AND book_id = %s"
            cursor.execute(query, (username, book_id))
            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({'success': True, 'message': 'Book removed from cart successfully'}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
