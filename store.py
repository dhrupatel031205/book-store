from flask import Blueprint, render_template, request, redirect, url_for
from db_connection import get_db_connection

store_bp = Blueprint('store', __name__)

@store_bp.route('/store', methods=['GET', 'POST'])
def store():
    
    return render_template('store.html')
