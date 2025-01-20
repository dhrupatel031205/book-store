from flask import Blueprint, render_template, request, redirect, url_for,session
from db_connection import get_db_connection

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET', 'POST'])
def home():
    username = session['username']
    user_data = data(username)
    return render_template('home.html',username =username)

def data(username) :
    try :
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT 8 FROM users WHERE username = %s"
        cursor.execute(query,(username,))

        userdata = cursor.fetchall()

        return userdata
        
    except Exception as e :
        print(e)
        
    finally :
        cursor.close()
        conn.close()