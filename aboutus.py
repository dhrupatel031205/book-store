from flask import Blueprint, render_template, request, redirect, url_for, session
from db_connection import get_db_connection

aboutus_bp = Blueprint('aboutus', __name__)

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
        print("Database error:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@aboutus_bp.route('/profile', methods=['GET', 'POST'])
def aboutus():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirect if not logged in

    user = fetch_user_data(username)
    cart = session.get('cartData')

    return render_template('aboutus.html', userdata=user)
