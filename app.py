from flask import Flask, render_template, request, url_for, redirect,session,jsonify
from datetime import datetime, timedelta
import os
from pymongo import MongoClient
from sha512 import sha512
from datetime import timedelta
#send Email
import email.message
import smtplib


app = Flask(__name__)
client = MongoClient('mongodb+srv://op23756778:Sean23756778@cluster0.xqmycmu.mongodb.net/')

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

@app.route('/', methods=('GET', 'POST'))
def index():
    if session.get('username'):
        return redirect(url_for('main'))
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

@app.route('/main', methods=('GET', 'POST'))
def main():
    if session.get('username'):
        pass
    else:
        print('not login')
        return redirect(url_for('index'))
    return render_template('Member_login_system/demoMain.html', name=session.get('username'))

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
        return redirect(url_for('index'))
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
    session['username']=False
    return redirect(url_for('index'))



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
if __name__=="__main__":
    app.run()