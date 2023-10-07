from flask import Flask
app = Flask(__name__) # buliding Application item

# building website home
@app.route('/') #This function is used to respond to website connections.
def index():
    return "Hello" #content

#start websit server
app.run()