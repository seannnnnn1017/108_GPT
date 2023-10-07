from flask import Flask, render_template
your_application = Flask(__name__, template_folder='templates') # buliding application item

# building website home
@your_application.route('/') #This function is used to respond to website connections.
def index():
    return render_template("home.html")

@your_application.route('/hello')
def hello():
    return render_template('hello.php')
#start websit server
your_application.run()