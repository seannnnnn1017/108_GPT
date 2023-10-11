from flask import Flask, render_template, request
app = Flask(__name__, template_folder='templates',static_folder='static') # buliding application item

# building website home
@app.route('/') #This function is used to respond to website connections.
def index():
    return render_template("index.html")

@app.route('/hello') #other websit loaction
def hello():
    data="hello data" #Create a variable 
    return render_template('hello.php', data=data) #pass the variable to websit
#start websit server

@app.route('/form') 
def test_form():
    return render_template("test_form.html")

@app.route('/user/<username>',methods=["GET","POST"])
def get_user(username):
    return "hello "+username

@app.route('/data_get',methods=["GET","POST"])
def test_data(): #http://127.0.0.1:5000/data_get?a=111&b=23
    print(request.args) #use to get after url variable
    print(request.args.get("a"),request.args.get("b"))

    #print(request.headers)
    print(request.headers.get('User-Agent'))

    print(request.form.get('username'),request.form.get('password'))
    return 'success'

@app.route("/file_get") #getting file data
def file_get():
    #read file
    data=[]
    with open("./data/demo_data.txt") as fin:
        for line in fin:
            line=line[:-1]
            times,number=line.split("	")
            data.append((times,number))
    #return html
    return render_template("file_get.html",data=data)

@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/test1")
def test1():
    return render_template('test1.html')


if __name__=="__main__":
    app.run()