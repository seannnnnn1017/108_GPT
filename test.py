from flask import Flask, render_template, request, jsonify
app = Flask(__name__, template_folder='templates',static_folder='static') # buliding application item
theme='light'
# building website home
@app.route('/',methods=['GET']) #This function is used to respond to website connections.
def index():
    check_number=request.args.get("check_number")
    if request.method=='GET':
        print(check_number)
    return render_template("test.html",theme=theme)



if __name__=="__main__":
    app.run()