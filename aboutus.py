from flask import Blueprint, render_template, request, redirect, url_for,session
from db_connection import get_db_connection

aboutus_bp = Blueprint('aboutus', __name__)

@aboutus_bp.route('/profile', methods=['GET', 'POST'])
def aboutus():
    username = session['username']
    user = fetch_user_data(username)
    return render_template('aboutus.html',userdata = user)

def fetch_user_data(username) :
    try :
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query,(username,))

        userdata = cursor.fetchall()
        return userdata
    except Exception as e :
        print(e)
        
    finally :
        cursor.close()
        conn.close()