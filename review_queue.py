from db_connection import get_db_connection

class FixedQueue:
    def __init__(self, size=4):
        self.queue = []
        self.size = size
        self.load_reviews()
    
    def enqueue(self, item):
        if len(self.queue) < self.size:
            self.queue.append(item)
        else:
            self.queue.pop(0)  # Remove oldest review
            self.queue.append(item)
    
    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def display(self):
        print("Queue:", self.queue)
    
    def load_reviews(self):
        """Fetch all reviews from the database and load the last 4 into the queue."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT name, review FROM reviews ORDER BY id DESC LIMIT 4"
            cursor.execute(query)
            reviews = cursor.fetchall()
            
            for review in reviews:
                self.enqueue(review)
        except Exception as e:
            print(f"Error fetching reviews: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def add_review(self, name, review):
        """Add a new review to the queue and store it in the database."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO reviews (name, review) VALUES (%s, %s)"
            cursor.execute(query, (name, review))
            conn.commit()
            
            self.enqueue((name, review))  # Add to queue
        except Exception as e:
            print(f"Error adding review: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_reviews(self):
        """Return the reviews currently in the queue."""
        return self.queue

# Create a global queue instance
review_queue = FixedQueue()
