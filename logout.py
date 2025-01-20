from flask import Blueprint, render_template, request, redirect, url_for,session
from db_connection import get_db_connection

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    username = session['username']
    return render_template('logout.html',username = username)
