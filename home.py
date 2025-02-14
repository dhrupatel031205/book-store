from flask import Blueprint, render_template, request, redirect, url_for, session
from db_connection import get_db_connection

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET', 'POST'])
def home():
    username = session.get('username')  # Use get() to avoid KeyError
    booksdata = data()
    return render_template('home.html', books_data=booksdata, username=username)

def data():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM books LIMIT 4"  # Fixed SQL syntax
        cursor.execute(query)

        booksdata = cursor.fetchall()
        return booksdata

    except Exception as e:
        print(f"Error: {e}")
        return []  # Return an empty list in case of an error

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
