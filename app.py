import flask
from login import login_bp
from logout import logout_bp
from signup import signup_bp
from store import store_bp
from home import home_bp
from cart import cart_bp
from aboutus import aboutus_bp
from contactus import contactus_bp

app = flask.Flask(__name__)

app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(store_bp)
app.register_blueprint(home_bp)
app.register_blueprint(aboutus_bp)
app.register_blueprint(contactus_bp)
app.register_blueprint(cart_bp)

app.secret_key = '321'
@app.route("/") 
def home() :
    return flask.render_template("main.html")

if __name__ == "__main__" :
    app.run(debug = True)