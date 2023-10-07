from flask import Flask, render_template
your_application = Flask(__name__, template_folder='templates',static_folder='static') # buliding application item

# building website home
@your_application.route('/') #This function is used to respond to website connections.
def index():
    return render_template("home.html")

@your_application.route('/hello') #other websit loaction
def hello():
    data="hello data" #Create a variable 
    return render_template('hello.php', data=data) #pass the variable to websit
#start websit server


if __name__=="__main__":
    your_application.run()