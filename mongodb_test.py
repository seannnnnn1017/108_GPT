from flask import Flask, render_template, request, url_for, redirect,session
#the request object to access data the user will submit
#the url_for() function to generate URLs
#the redirect() function to redirect the user back to the index page after adding a todo.

import os
#pip install Flask pymongo
from pymongo import MongoClient
from sha512 import sha512

from datetime import timedelta
app = Flask(__name__)
#When you instantiate the MongoClient(), you pass it the host of your MongoDB server, 
#which is localhost in our case, and the port, which is 27017 here.
client = MongoClient('localhost', 27017)
#Into the 'flask_db' database. If this database does not exist, a new database will be created.
db = client.flask_db
#create a collection called 'todos' on the 'flask_db' 
todos = db.todos

#login in test
demo_db=client.demo
account=demo_db.account


app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

@app.route('/', methods=('GET', 'POST'))
def index():
    all_account=account.find()
    print(all_account[0])
    print(type(all_account[0]))
    if request.method=='POST':
        #Obtain form data from HTML
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        find=False
        for i in all_account:
            if i['username'] ==username:
                find=True
                break
        if find:
            print('this account is exist')
            print(i['password'])
            print(sha512(password))
            if sha512(password) == i['password']:
                print('login')
                session['username']=username
                return redirect(url_for('test_session'))
            else:
                print('password error')
            
        else:
            print('No find this account or error.')


    name=session.get('username')
    return render_template('demoLogin.html', name=name)

@app.route("/get", methods=('GET', 'POST'))
def getting():
    all_todos = todos.find()
    print(all_todos[0])
    if request.method=='POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('getting'))

    
    return render_template('databaseGet.html', todos=all_todos)

#Demo session
@app.route('/session', methods=["GET", "POST"])
def test_session():
    


    #getting session
    name=session.get('username')
    
    #delete session
    #session['username']=False
    return render_template('demoLoginOut.html', name=name)

#background process happening without any refreshing
@app.route('/logout')
def logout():
    session['username']=None
    print ("Logout")
    return render_template('demoLogin.html', name=name)
if __name__=="__main__":
    app.run()