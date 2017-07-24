import pyrebase
config = {
  "apiKey": "AIzaSyBxUR7lyOPiPoGKL4ATZztXkK-N7UK9Sck",
  "authDomain": "testing-6a8f2.firebaseapp.com",
  "databaseURL": "https://testing-6a8f2.firebaseio.com",
  "storageBucket": "testing-6a8f2.appspot.com",
  "serviceAccount": "C:/Users/Lauren/smartshoe/testing-6a8f2-firebase-adminsdk-50kup-bfa1979cae.json"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
#authenticate a user
user = auth.sign_in_with_email_and_password("lauren9y@gmail.com", "123456")
# user = auth.refresh(user['refreshToken'])
idToken = user['idToken']
# print (idToken)
db = firebase.database()

data1 = {"sensor1": "example value", "sensor2": "example value", "sensor3": "example value", "sensor4": "example value"}
db.child("datetime").child("Pad1").set(data1, idToken)

data2 = {"sensor1": "example value", "sensor2": "example value", "sensor3": "example value", "sensor4": "example value"}
db.child("datetime").child("Pad1").set(data2, idToken)

data3 = {"sensor1": "example value", "sensor2": "example value", "sensor3": "example value", "sensor4": "example value"}
db.child("datetime").child("Pad1").set(data3, idToken)

data4 = {"sensor1": "example value", "sensor2": "example value", "sensor3": "example value", "sensor4": "example value"}
db.child("datetime").child("Pad1").set(data4, idToken)


# examples of commands
# archer = {"name": "Sterling Archer", "agency": "Figgis Agency"}
# db.child("agents").push(archer, user['idToken'])
#
# lana = {"name": "Lana Kane", "agency": "Figgis Agency"}
# db.child("agents").child("Lana").set(lana, user['idToken'])
#
# #read
# all_agents = db.child("agents").get(user['idToken']).val()
# print(all_agents)
#
# lana_data = db.child("agents").child("Lana").get(user['idToken']).val()
# print(lana_data)
#
# #update
# db.child("agents").child("Lana").update({"name": "Lana Anthony Kane"}, user['idToken'])
#
# #delete
# db.child("agents").remove(user['idToken'])
