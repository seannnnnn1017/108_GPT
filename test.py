from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.test 

test=db.test
a=test.find()

    
test.insert_one({'_id': '123123123','username' : 'Sean'})

for i in a:

    print(i['_id'])

    