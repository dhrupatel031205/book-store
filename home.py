from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_connection import get_db_connection

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET', 'POST'])
def home():
    username = session.get('username')  # Get the session username
    booksdata = data()  # Fetch books data
    reviews = fetch_reviews()  # Fetch reviews
    return render_template('home.html', books_data=booksdata, username=username, reviews=reviews)

def data():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM books LIMIT 4"  # Fetch 4 books
        cursor.execute(query)

        booksdata = cursor.fetchall()
        return booksdata

    except Exception as e:
        print(f"Error fetching books: {e}")
        return []  # Return an empty list if an error occurs

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@home_bp.route("/add_review", methods=['POST'])
def add_review():
    username = session.get('username')
    name = request.form.get('name')
    review = request.form.get('review')

    if not username:
        flash("You must be logged in to submit a review.", "danger")
        return redirect(url_for('home.home'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO reviews(username, name, review) VALUES(%s, %s, %s)"
        cursor.execute(query, (username, name, review))
        conn.commit()  # Commit the transaction
        flash("Review submitted successfully!", "success")
    except Exception as e:
        flash(f"Error submitting review: {str(e)}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for('home.home'))

def fetch_reviews():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT name, review FROM reviews ORDER BY id DESC LIMIT 4"  # Get last 4 reviews
        cursor.execute(query)
        reviews = cursor.fetchall()
        return reviews
    except Exception as e:
        flash(f"Error fetching reviews: {str(e)}", "danger")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
