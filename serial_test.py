import serial
import pyrebase
from datetime import datetime, date, time
import time


#initializing pyrebase
config = {
  "apiKey": "AIzaSyBxUR7lyOPiPoGKL4ATZztXkK-N7UK9Sck",
  "authDomain": "testing-6a8f2.firebaseapp.com",
  "databaseURL": "https://testing-6a8f2.firebaseio.com",
  "storageBucket": "testing-6a8f2.appspot.com",
  "serviceAccount": "C:/Users/Lauren/smartshoe/testing-6a8f2-firebase-adminsdk-50kup-7f487fa306.json"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
#authenticate a user
user = auth.sign_in_with_email_and_password("lauren9y@gmail.com", "123456")
# user = auth.refresh(user['refreshToken'])
idToken = user['idToken']
# print (idToken)
db = firebase.database()
past_datetime = datetime.now()

#initializing serial
ser = serial.Serial()
ser.baudrate = 921600
ser.port = 'COM5'
ser.open()
time.sleep(0.1)
#begin reading from COM port
ser.flush()
a = ser.read(ser.inWaiting())
# print(ser.inWaiting())
print (a)
a = a.decode()
a_array = a.split('\r\n')
print (a_array)
result = {}


for i in a_array:
    print("number of lines", len(a_array))
    pad_array = i.split(',')
    print ("sequence is", pad_array[0])

    if len(pad_array) < 20:
        pass
        print ("i am passing")
    else:
        current_datetime = datetime.now()
        c = current_datetime - past_datetime
        print("difference in time", c)
        past_datetime = current_datetime

        date_time = datetime.strftime(datetime.now(), "%d%m%y%H%M%S%f")
        pad1_sensor1 = str(pad_array[1])
        pad1_sensor2 = str(pad_array[2])
        pad1_sensor3 = str(pad_array[3])
        pad1_sensor4 = str(pad_array[4])
        # data1 = {"sensor1": pad1_sensor1, "sensor2": pad1_sensor2, "sensor3": pad1_sensor3, "sensor4": pad1_sensor4}
        # db.child(date_time).child("Pad1").set(data1, idToken)
        pad1 = {1: pad1_sensor1, 2: pad1_sensor2, 3: pad1_sensor3, 4: pad1_sensor4}

        pad2_sensor1 = str(pad_array[6])
        pad2_sensor2 = str(pad_array[7])
        pad2_sensor3 = str(pad_array[8])
        pad2_sensor4 = str(pad_array[9])
        # data2 = {"sensor1": pad2_sensor1, "sensor2": pad2_sensor2, "sensor3": pad2_sensor3, "sensor4": pad2_sensor4}
        # db.child(date_time).child("Pad2").set(data2, idToken)
        pad2 = {1: pad2_sensor1, 2: pad2_sensor2, 3: pad2_sensor3, 4: pad2_sensor4}

        pad3_sensor1 = str(pad_array[11])
        pad3_sensor2 = str(pad_array[12])
        pad3_sensor3 = str(pad_array[13])
        pad3_sensor4 = str(pad_array[14])
        # data3 = {"sensor1": pad3_sensor1, "sensor2": pad3_sensor2, "sensor3": pad3_sensor3, "sensor4": pad3_sensor4}
        # db.child(date_time).child("Pad3").set(data3, idToken)
        pad3 = {1: pad3_sensor1, 2: pad3_sensor2, 3: pad3_sensor3, 4: pad3_sensor4}

        pad4_sensor1 = str(pad_array[16])
        pad4_sensor2 = str(pad_array[17])
        pad4_sensor3 = str(pad_array[18])
        pad4_sensor4 = str(pad_array[19])
        # data4 = {"sensor1": pad4_sensor1, "sensor2": pad4_sensor2, "sensor3": pad4_sensor3, "sensor4": pad4_sensor4}
        # db.child(date_time).child("Pad4").set(data4, idToken)
        pad4 = {1: pad4_sensor1, 2: pad4_sensor2, 3: pad4_sensor3, 4: pad4_sensor4}

        result[date_time] = [pad1, pad2, pad3, pad4]

for key, value in result.items():

    pad1_sensor1 = value[0][1]
    pad1_sensor2 = value[0][2]
    pad1_sensor3 = value[0][3]
    pad1_sensor4 = value[0][4]
    data1 = {"sensor1": pad1_sensor1, "sensor2": pad1_sensor2, "sensor3": pad1_sensor3, "sensor4": pad1_sensor4}


    pad2_sensor1 = value[1][1]
    pad2_sensor2 = value[1][2]
    pad2_sensor3 = value[1][3]
    pad2_sensor4 = value[1][4]
    data2 = {"sensor1": pad2_sensor1, "sensor2": pad2_sensor2, "sensor3": pad2_sensor3, "sensor4": pad2_sensor4}


    pad3_sensor1 = value[2][1]
    pad3_sensor2 = value[2][2]
    pad3_sensor3 = value[2][3]
    pad3_sensor4 = value[2][4]
    data3 = {"sensor1": pad3_sensor1, "sensor2": pad3_sensor2, "sensor3": pad3_sensor3, "sensor4": pad3_sensor4}


    pad4_sensor1 = value[3][1]
    pad4_sensor2 = value[3][2]
    pad4_sensor3 = value[3][3]
    pad4_sensor4 = value[3][4]
    data4 = {"sensor1": pad4_sensor1, "sensor2": pad4_sensor2, "sensor3": pad4_sensor3, "sensor4": pad4_sensor4}

    db.child(key).child("Pad1").set(data1, idToken)
    db.child(key).child("Pad2").set(data2, idToken)
    db.child(key).child("Pad3").set(data3, idToken)
    db.child(key).child("Pad4").set(data4, idToken)




ser.close()
