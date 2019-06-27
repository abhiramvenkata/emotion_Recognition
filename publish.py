from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
import serial
ser = serial.Serial('/dev/ttyACM0',9600)
ser.baudrate=9600
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss456")
myMQTTClient.configureEndpoint("a27pb8hmkx5vf5.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/cert/CA.pem", "/home/pi/cert/d96a287d20-private.pem.key", "/home/pi/cert/d96a287d20-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("thing01/info", "connected", 0)
 
#loop and publish sensor reading
while 1:
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    read_serial=ser.readline()
    
    payload = '{ "timestamp": "' + now_str + '", ' + str(read_serial) + '}'
    print payload
    myMQTTClient.publish("thing01/data", payload, 0)
    sleep(2)
    