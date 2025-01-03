from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_connection import get_db_connection

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for('home.home'))  # Redirect to home page
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login.login'))

    return render_template('login.html')
