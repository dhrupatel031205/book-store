from flask import Blueprint, render_template, request, redirect, url_for
from db_connection import get_db_connection

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    
    return render_template('logout.html')
