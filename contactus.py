from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_connection import get_db_connection

contactus_bp = Blueprint('contactus', __name__)

@contactus_bp.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not (name and email and message):
            flash("All fields are required!", "danger")
            return redirect(url_for('contactus.contactus'))

        data = [name, email, message]
        save_data(data) 
        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('contactus.contactus'))

    return render_template('contactus.html')

def save_data(data):
    username = session.get('username')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO `contact_us` (`username`, `name`, `email`, `message`) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, data[0], data[1], data[2]))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()
