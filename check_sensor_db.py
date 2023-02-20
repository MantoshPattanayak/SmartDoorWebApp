import time
import paho.mqtt.client as mqtt
import pymysql.cursors
from datetime import datetime
import ping3
import logging

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("20.205.208.135", 1883, 60)


global data
connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
	global data
	sql = "select school_id from keonjhar_school_device where device_temp>=50 and device_mq2>=5000 and device_hum<=25 group by school_id having count(device_temp)>=2;"
	cursor.execute(sql)
	result = cursor.fetchall()
	connection.commit()
	print(result)
	
client.loop_forever()