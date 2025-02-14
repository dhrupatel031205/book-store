from your_database_module import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    order_data = db.Column(db.JSON, nullable=False)  # Store cart details
    total_price = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, order_data, total_price):
        self.username = username
        self.order_data = order_data
        self.total_price = total_price
