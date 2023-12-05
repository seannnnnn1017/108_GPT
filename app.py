from flask import Flask, render_template, request, url_for, redirect,session,jsonify,abort,redirect
from datetime import datetime, timedelta
import os
from pymongo import MongoClient
from sha512 import sha512
from datetime import timedelta
import requests
#send Email
import email.message
import smtplib

#google Login
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import pathlib

#openai
import openai
from dotenv import dotenv_values
import time

app = Flask(__name__)
client = MongoClient('mongodb+srv://op23756778:Sean23756778@cluster0.xqmycmu.mongodb.net/')

#cancel the request SSL,HTTPS 
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#google API setting
GOOGLE_CLIENT_ID = "168531082727-cg9gvj0iu8p2so59jg5sqdq7isqi40f9.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://one08-gpt-demo.onrender.com/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

#account database
demo_db=client.demo
#account database
account=demo_db.account
#Query the database for sign up requests.
check=demo_db.check
check.create_index("expireAt", expireAfterSeconds=0)
#Query the database for password reset requests.
reset_ask=demo_db.Reset_ask
reset_ask.create_index("expireAt", expireAfterSeconds=0)
#session need a secret key to encryption data
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)


#session defind

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('homepage/before_login.html')

@app.route('/loginpage', methods=('GET', 'POST'))
def loginpage():

    if session.get('username'):
        return redirect(url_for('main'))
    else:
        session["google_id"] =None
        session["email"] = None
        session["username"] = None
        session["picture"] = None
        session['fist_login']=False
    all_account=account.find()
    if request.method=='POST':
        #Obtain form data from HTML
        Email = request.form['email']
        password = request.form['password']
        print(Email,password)
        find=False
        for i in all_account:
            if i['email'] ==Email:
                find=True
                break
        if find:
            print('this account is exist')
            print(i['password'])
            print(sha512(password))
            if sha512(password) == i['password']:
                print('login')
                session['username']= i['username']
                return redirect(url_for('main'))
            else:
                return render_template('Member_login_system/demoLogin.html', error='password error')

            
        else:
            return render_template('Member_login_system/demoLogin.html', error='No find this account or error.')



    return render_template('Member_login_system/demoLogin.html')

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    try:
        flow.fetch_token(authorization_response=request.url)

        if session.get("state") != request.args.get("state"):
            raise Exception("State does not match!")

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        session["google_id"] = id_info.get("sub")
        session["email"] = id_info.get("email")
        session["username"] = id_info.get("name")
        session["picture"] = id_info.get("picture")

        all_account=account.find()
        find=False
        for i in all_account:
            if i['email'] ==session.get('email'):
                find=True
                session["username"]=i['username']
                break
        if find:
            return redirect("/main")
        else:
            print('not sign up')
            session['fist_login']=True
            return redirect(url_for('Fist_google_login'))
    except Exception as e:
        # Log the exception and handle it appropriately
        print(f"Exception in callback: {e}")
        return f"Exception in callback: {e}"
    
@app.route('/Fist_google_login', methods=('GET', 'POST'))
def Fist_google_login():
    if session.get('fist_login'):
        if request.method=='POST':
            username = request.form['username']
            password = request.form['password']
            email = session["email"]
            repeat_password=request.form['repeat-password']

            if repeat_password!=password:
                return render_template('Member_login_system/FistGoogleLogin.html',state='repeat password error',email=session["email"])
            if len(password) <8:
                return render_template('Member_login_system/FistGoogleLogin.html',state='password need to have 8 or more characters',email=session["email"])
            all_account=account.find()
            for i in all_account:
                if i['email'] ==email:
                    return render_template('Member_login_system/FistGoogleLogin.html',state='the email exist',email=session["email"])
            check_number=username+sha512(email)[:10]+sha512(password)[:10]
            check.insert_one({'email': email,
                              'username': username,
                                'password': sha512(password),
                                'check number':check_number,
                                'expireAt': datetime.utcnow() + timedelta(days=1)})
            query = {"check number": check_number}
            accounts=check.find(query)
            for i in accounts:
                print(i['email'])
            del i["_id"]
            del i["expireAt"]
            account.insert_one(i)
            query = {'email': i['email']}
            check.delete_many(query)
            session['fist_login']=False
            return redirect(url_for('main'))
        return render_template('Member_login_system/demoFistGoogleLogin.html',email=session["email"])
    else:
        return redirect(url_for('loginpage'))
#壞掉中
@app.route('/update_theme', methods=['POST'])
def update_theme():
    global theme
    data = request.get_json()
    theme = data.get('theme')
    print(theme)

@app.route('/main', methods=('GET', 'POST'))
def main():
    if session.get('username'):
        pass
    else:
        print('not login')
        return redirect(url_for('loginpage'))
    return render_template('Member_login_system/demoMain.html', name=session.get('username'),picture=session["picture"])

@app.route('/register', methods=('GET', 'POST'))
def register():
    if  not session.get('username'):
        if request.method=='POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            repeat_password=request.form['repeat-password']

            if repeat_password!=password:
                return render_template('Member_login_system/demoRegister.html',state='repeat password error')
            if len(password) <8:
                return render_template('Member_login_system/demoRegister.html',state='password need to have 8 or more characters')
            all_account=account.find()
            for i in all_account:
                if i['email'] ==email:
                    return render_template('Member_login_system/demoRegister.html',state='the email exist')
            check_number=username+sha512(email)[:10]+sha512(password)[:10]
            check.insert_one({'email': email,
                              'username': username,
                                'password': sha512(password),
                                'check number':check_number,
                                'expireAt': datetime.utcnow() + timedelta(days=1)})
            send_verify_email(email,check_number)
            return render_template('Member_login_system/demoRegisterAfter.html',username=username,email=email)
            
    else: 
        print('you are login')
        return redirect(url_for('loginpage'))
    return render_template('Member_login_system/demoRegister.html')

@app.route('/Check', methods=('GET', 'POST'))
def check_email():
    check_number=request.args.get("check_number")
    if request.method=='GET':
        print(check_number)
        query = {"check number": check_number}
        accounts=check.find(query)
        for i in accounts:
            print(i['email'])
        del i["_id"]
        del i["expireAt"]
        account.insert_one(i)
        query = {'email': i['email']}
        check.delete_many(query)
    return render_template('Member_login_system/demoCheckEmail.html')

@app.route('/forget', methods=('GET', 'POST'))
def forget():
    if  not session.get('username'):
        if request.method=='POST':
            email = request.form['email']
            all_account=account.find()
            find_email=False
            for i in all_account:
                if i['email'] ==email:
                    find_email=True
                    break
            if find_email:
                reset_ask.insert_one({  'email': email,
                                        'check number':i['check number'],
                                        'expireAt': datetime.utcnow() + timedelta(days=1)})
                
                send_reset_email(i['email'],i['check number'])
                return render_template('Member_login_system/demoForgetPasswordAfter.html',email=email)
            else:
                return render_template('Member_login_system/demoForgetPassword.html',state='the email not exist')
    return render_template('Member_login_system/demoForgetPassword.html',state='')

@app.route('/reset_password', methods=('GET', 'POST'))
def reset_password():
    check_number=request.args.get("check_number")
    email=request.args.get("email")
    print(check_number,email)
    if request.method=='POST':
        query = {"check number": check_number}
        accounts=account.find_one(query)
        if not accounts:
            print('ERROR')
            return render_template('Member_login_system/demoResetPassword.html')
            
        password = request.form['password']
        repeat_password=request.form['repeat-password']
        print(password,repeat_password)
        if repeat_password!=password:
            return render_template('Member_login_system/demoResetPassword.html',state='repeat password error',email=email)
        if len(password) <8:
            return render_template('Member_login_system/demoResetPassword.html',state='password need to have 8 or more characters',email=email)
        reset_ask.delete_many(query)
        account.update_one(query, {'$set': {'password': sha512(password)}})
        return render_template('Member_login_system/demoResetPasswordAfter.html',email=email)
    return render_template('Member_login_system/demoResetPassword.html',email=email)

@app.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('loginpage'))


@app.route('/assist', methods=('GET', 'POST'))
def assist():
    layer_list=[]
    if request.method=='POST':
        for i in range(1,11):
            layer_value=request.form.get(f'Layer {i}')
            layer_list.append(layer_value)
            print(layer_list)
        result_data=generate_text(layer_list,department="人工智慧系",support="多元表現綜整心得")
        return render_template('Assist_writing.html',result_data=result_data)
    return  render_template('Assist_writing.html')
 

 
def send_verify_email(to_email, check_number):
    # Set up email credentials
    email_address = 'op23756778@gmail.com'
    email_password = 'hgqm nqjq pjcb pqzc'

    if email_password is None:
        print("Error: Email password not set.")
        exit()

   # Create message object
    msg = email.message.EmailMessage()
    msg["From"] = email_address
    msg["To"] = to_email
    msg["Subject"] = "108&GPT 帳號驗證碼"
    verification_link = url_for('check_email', check_number=check_number, _external=True)
    print(verification_link)
    # Email content
    msg.add_alternative(f"""
                        <h3>測試網站驗證帳號創建</h3>安安這是寄送郵件測試
                           <a href="{verification_link}">Verify Email</a>
                        """, subtype="html")

    # Connect to SMTP Server (Gmail) and send email
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(email_address, email_password)
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

def send_reset_email(to_email, check_number):
    # Set up email credentials
    email_address = 'op23756778@gmail.com'
    email_password = 'hgqm nqjq pjcb pqzc'

    if email_password is None:
        print("Error: Email password not set.")
        exit()

   # Create message object
    msg = email.message.EmailMessage()
    msg["From"] = email_address
    msg["To"] = to_email
    msg["Subject"] = "108&GPT 忘記密碼"
    verification_link = url_for('reset_password', check_number=check_number,email=to_email, _external=True)

    # Email content
    msg.add_alternative(f"""
                        <h3>聽說妳忘記密碼了 笑死</h3>按這個link去改密碼吧
                           <a href="{verification_link}">Reset Password</a>
                        """, subtype="html")

    # Connect to SMTP Server (Gmail) and send email
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(email_address, email_password)
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

def generate_text(ans_list,department="人工智慧系",support="多元表現綜整心得"):
    with open(".\data\多元表現綜整心得.txt", "r", encoding = "utf-8") as file:
        AI_quesntions = [line.strip() for line in file.readlines()]
        file.close()
        
    config = dotenv_values("C:/Users/user/Desktop/env.txt")
    openai.api_key = config["API_KEY"]

    messages = [{"role": "system", "content": "zh-Tw 你要幫準備申請大學的高中生撰寫學習歷程 字數大約1000字"}]

    for i in range(len(AI_quesntions)):
        ans=''
        for item in ans_list:
            ans = item #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
        if ans:
            messages.append({"role": "assistant", "content": AI_quesntions[i]},)
            messages.append({"role": "user", "content": ans})
        elif ans == "0":
            return None

    narration = f'''
        目標學系: {department}
        =====================================
        根據以上問答及提供的學系，幫我完成{support}
    '''
    messages.append({"role": "user", "content": narration})


    print("===========================================================================================")
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model = "gpt-4-1106-preview",
        messages = messages,
        max_tokens = 1000,
    )
    end_time = time.time() 
    print(f"程式執行時間: {end_time - start_time} 秒")
    
    return response['choices'][0]['message']['content']


if __name__=="__main__":
    app.run(debug=True)