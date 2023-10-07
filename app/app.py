from flask import Flask, render_template
app = Flask(__name__, template_folder='templates',static_folder='static') # buliding application item

# building website home
@app.route('/') #This function is used to respond to website connections.
def index():
    return render_template("home.html")

@app.route('/hello') #other websit loaction
def hello():
    data="hello data" #Create a variable 
    return render_template('hello.php', data=data) #pass the variable to websit
#start websit server


if __name__=="__main__":
    app.run()