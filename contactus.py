from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_connection import get_db_connection
from flask_mail import Mail, Message

contactus_bp = Blueprint('contactus', __name__)

# Configure Flask-Mail
mail = Mail()

def configure_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'd6207729@gmail.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = ''  # Replace with your app password
    app.config['MAIL_DEFAULT_SENDER'] = 'd6207729@gmail.com'
    mail.init_app(app)

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
        send_email(name, email, message)

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('contactus.contactus'))

    return render_template('contactus.html')

def save_data(data):
    username = session.get('username', 'Guest')  # Use 'Guest' if not logged in
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

def send_email(name, email, message):
    try:
        subject = f"New Contact Us Message from {name}"
        recipient = "d62077299@gmail.com"
        body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

        msg = Message(subject, recipients=[recipient], body=body)
        mail.send(msg)
    except Exception as e:
        print(f"Email error: {e}")

