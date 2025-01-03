from flask import Blueprint, render_template, request, redirect, url_for
from db_connection import get_db_connection

contactus_bp = Blueprint('contactus', __name__)

@contactus_bp.route('/contactus', methods=['GET', 'POST'])
def contactus():
    
    return render_template('contactus.html')
