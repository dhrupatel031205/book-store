from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_connection import get_db_connection
from review_queue import review_queue  # Import the queue instance

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET', 'POST'])
def home():
    username = session.get('username')  # Get the session username
    booksdata = fetch_books()  # Fetch books data
    reviews = review_queue.get_reviews()  # Get reviews from the queue
    return render_template('home.html', books_data=booksdata, username=username, reviews=reviews)

def fetch_books():
    """Fetch book data from the database."""
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

    review_queue.add_review(name, review)  # Add review to queue and database
    flash("Review submitted successfully!", "success")
    return redirect(url_for('home.home'))
