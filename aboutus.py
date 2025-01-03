from flask import Blueprint, render_template, request, redirect, url_for
from db_connection import get_db_connection

aboutus_bp = Blueprint('aboutus', __name__)

@aboutus_bp.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    
    return render_template('aboutus.html')
