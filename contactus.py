from flask import Blueprint, render_template, request, redirect, url_for, session
from db_connection import get_db_connection

contactus_bp = Blueprint('contactus', __name__)

@contactus_bp.route('/contactus', methods=['GET', 'POST'])
def contactus():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    data = [name,email,message]
    save_data(data)
    return render_template('contactus.html')

def save_data(data) :
    username = session['username']
    try :
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO `contact_us`( `username`, `name`, `email`, `message`) VALUES (%s,%s,%s,%s)"

        cursor.execute(query,(username, data[0],data[1],data[2]))
        conn.commit()
    except Exception as e :
        print(e)
        
    finally :
        cursor.close()
        conn.close()

    
        