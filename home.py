from flask import Blueprint, render_template, request, redirect, url_for
from db_connection import get_db_connection

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET', 'POST'])
def home():
    
    return render_template('home.html')
