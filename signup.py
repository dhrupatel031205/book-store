from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_connection import get_db_connection

signup_bp = Blueprint('signup', __name__)
@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s', (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Username or email already exists. Please choose another.', 'error')
                return redirect(url_for('signup.signup'))

            cursor.execute('INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)',
                           (name, email, username, password))
            conn.commit()
            flash('Account created successfully! You can now log in.', 'success')
            
            return redirect(url_for('login.login'))  # Redirect to the login page
        except Exception as e:
            print(f"Error: {e}")
            flash('An error occurred during signup. Please try again.', 'error')
            return redirect(url_for('signup.signup'))
        finally:
            conn.close()

    return render_template('signup.html')
