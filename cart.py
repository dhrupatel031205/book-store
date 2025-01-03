from flask import Blueprint, render_template, request, redirect, url_for
from db_connection import get_db_connection

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    
    return render_template('cart.html')
