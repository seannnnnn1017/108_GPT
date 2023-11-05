from flask import Flask, render_template, request, url_for, redirect
#the request object to access data the user will submit
#the url_for() function to generate URLs
#the redirect() function to redirect the user back to the index page after adding a todo.

#pip install Flask pymongo
from pymongo import MongoClient

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
        if find:
            print('this account is exist')
            
        else:
            print('No find this account or error.')
        return redirect(url_for('getting'))

    all_todos = todos.find()
    return render_template('demoLogin.html', todos=all_todos)

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


if __name__=="__main__":
    app.run()