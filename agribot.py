import RPi.GPIO as GPIO
import blynklib
import time

import Adafruit_DHT

##import spidev
import os
import cv2
import smtplib
import os.path
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders
from Adafruit_IO import Client, Feed, RequestError



m11=2
m12=3
m21=4
m22=17
dt=14
moisture=15
seeder=21
weeder=23
pump=16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.setup(seeder, GPIO.OUT)
GPIO.setup(weeder, GPIO.OUT)
GPIO.setup(pump, GPIO.OUT)

GPIO.setup(dt, GPIO.IN)
GPIO.setup(moisture, GPIO.IN)





sensor=Adafruit_DHT.DHT11

GPIO.output(m11 , 0)
GPIO.output(m12 , 0)
GPIO.output(m21, 0)
GPIO.output(m22, 0)
GPIO.output(seeder , 0)
GPIO.output(weeder, 0)
GPIO.output(pump, 0)



ADAFRUIT_IO_KEY = 'aio_bohI78iTvfntTKHng1YekAWEs6n4'
ADAFRUIT_IO_USERNAME = 's8897576332'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)# Create an instance of the REST client.


# Set up Adafruit IO Feeds.
temperature_feed = aio.feeds('temperature')
humidity_feed = aio.feeds('humidityy')
moisture_feed = aio.feeds('soil')


email = 's8897576332@gmail.com'
password = 'surya8897'
send_to_email = 's8897576332@gmail.com'
subject = 'msg from agribot'
message = 'location image received'
file_location = '/home/pi/firstside0.png'
msg = MIMEMultipart()#Create the container (outer) email message.
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject
'''as.string() 
|
+------------MIMEMultipart 
              |                                                |---content-type 
              |                                   +---header---+---content disposition 
              +----.attach()-----+----MIMEBase----| 
                                 |                +---payload (to be encoded in Base64)
                                 +----MIMEText'''
msg.attach(MIMEText(message, 'plain'))#attach new  message by using the Message.attach

auth_token = 'w553_l9AXt0rSvDSkcH4ssNm9rcs4SaS'

# Initialize Blynk

blynk = blynklib.Blynk(auth_token)

@blynk.handle_event('write V0')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        print ("left")
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 0)
        GPIO.output(m11 , 1)
        GPIO.output(m12 , 0)
    else:
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 0)
    
@blynk.handle_event('write V1')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        print ("right")
        GPIO.output(m21 , 1)
        GPIO.output(m22 , 0)
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
    else:
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 0)
        

        
@blynk.handle_event('write V2')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        print ("STOP")
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 0)

        
@blynk.handle_event('write V3')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        print ("for")
        GPIO.output(m21 , 1)
        GPIO.output(m22 , 0)
        GPIO.output(m11 , 1)
        GPIO.output(m12 , 0)

@blynk.handle_event('write V4')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        print ("BACK")
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 1)
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 1)
@blynk.handle_event('write V5')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        humidity, temperature = Adafruit_DHT.read_retry(sensor,dt )
        water=GPIO.input(moisture)
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
            
        # Send humidity and temperature feeds to Adafruit IO
        temperature = '%.2f'%(temperature)
        humidity = '%.2f'%(humidity)
        aio.send(temperature_feed.key, str(temperature))
        aio.send(humidity_feed.key, str(humidity))
        print("dht11 uploaded")
        
        print(water)
        if(water == 0):
            print("wet")
            aio.send(moisture_feed.key, str('wet'))
            print("sent")

        else:
            print("dry")
            aio.send(moisture_feed.key, str('dry'))
            print("sent")

@blynk.handle_event('write V6')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        print ("IMAGE UPLOADING")
        print("with in cemara")
        camera = cv2.VideoCapture(0)
        for i in range(10):
            return_value, image = camera.read()
            cv2.imwrite('AGRI'+str(i)+'.png', image)
            print('AGRI IMG captured')
            time.sleep(2)
            break
        del(camera)
        
        
        filename = os.path.basename(file_location)#function returns the tail of the path
        attachment = open(file_location, "rb") #“rb” (read binary)
        part = MIMEBase('application', 'octet-stream')#Content-Type: application/octet-stream , image/png, application/pdf
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)#Content-Disposition: attachment; filename="takeoff.png"
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)# Send the message via local SMTP server.
        print("with in msg")
        server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        print("mail sended")
        server.quit()
@blynk.handle_event('write V7')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        print ("pump")
        GPIO.output(pump , 1)
    else:
        GPIO.output(pump , 0)
        

@blynk.handle_event('write V8')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        print ("WEEDER on")
        GPIO.output(weeder, 1)
    else:
        print ("WEEDER on")
        GPIO.output(weeder, 0)
        

@blynk.handle_event('write V9')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        print ("seder")
        GPIO.output(seeder , 1)
    else:
        GPIO.output(seeder , 0)


try:
    while True:
        blynk.run()

        
                    



except KeyboardInterrupt:
    print("Quit")

# Reset GPIO settings
GPIO.cleanup()



URL :  http://embagribot.dbandroid.online/

Credentials : 

email        : admin@gmail.com
password : agri@123

API : http://embagribot.dbandroid.online/save_values.php?tmp=&humidity=&soil=&id=
