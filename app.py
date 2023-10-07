from flask import Flask
your_application = Flask(__name__) # buliding application item

# building website home
@your_application.route('/') #This function is used to respond to website connections.
def index():
    return "Hello" #content

#start websit server
your_application.run()