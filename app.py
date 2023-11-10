from flask import Flask, render_template, request, jsonify
app = Flask(__name__, template_folder='templates',static_folder='static') # buliding application item
theme='light'
# building website home
@app.route('/') #This function is used to respond to website connections.
def index():
    global theme
    return render_template("index.html",theme=theme)


@app.route('/update_theme', methods=['POST'])
def update_theme():
    global theme
    data = request.get_json()
    theme = data.get('theme')
    print(theme)
    # 在这里，您可以将主题保存到会话、数据库或其他地方
    # 以便在后续页面中使用
    # 也可以使用 Flask-Session 扩展来管理会话状态

    return jsonify({'message': 'Theme updated successfully'})

@app.route("/activity")
def activity():
    return render_template('activity.html',theme=theme)

@app.route("/personal_information")
def personal_information():
    return render_template('personal_information.html',theme=theme)


if __name__=="__main__":
    app.run()