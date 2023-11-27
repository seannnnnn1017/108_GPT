# 108_GPT
This repository is used to test server websites.
---
# Database: MongoBD
Cloud server:
https://cloud.mongodb.com/v2/654f2da80f6b846755a32768?fbclid=IwAR3r03puZPSpphYJ7y_u-zvbxstT5A8aXsWpbIw9wa_JjJb0p0cwcjq6QwY#/overview
#  Database structure:
# 1 demo 
      
## 1.1 account 
This document is used to store user account information.

    {
    "_id": {
      "$oid": "6550ae94832821c48dcb0d11"
    },
    "email": user@gmail.com,
    "username": username,
    "password": User passwords are securely stored using the SHA-512 hashing algorithm.,
    "check number": The username is combined with the first 10 characters of the SHA-512 hash of the email, and the first 10 characters of the SHA-512 hash of the password.
  }
## 1.2 check
This document is used to temporarily store sign-up requests from users for 1 day.
## 1.3 Reset_ask
This document is used to temporarily store change-password requests from users for 1 day.


---
# 1.0 Member Login System
  1.1 Register 
    
  1.2 Login 
    
  1.3 Forget password 
    
  1.4 Logout 

---
