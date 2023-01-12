import time
import paho.mqtt.client as mqtt
import pymysql.cursors
from datetime import datetime
import ping3
import logging

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

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
	print("Second data")
	#print(result[0]["school_id"])
	#print(result[1]["school_id"])
	for i in range(0,len(result)):
		data = result[i]["school_id"]
		print(data)
		with connection.cursor() as cursor:
			data
			sql ="Select keonjhar_school_device.device_id, keonjhar_school.school_name from keonjhar_school_device join keonjhar_school on keonjhar_school_device.school_id = keonjhar_school.school_id where keonjhar_school_device.school_id=%s;"
			cursor.execute(sql,(data))
			result=cursor.fetchall()
			connection.commit()
			print(result)
			school_id = result[0]["school_id"]
			device_id = result[0]["device_id"]
			school_name = result[0]["school_name"]
			topic = str(device_id)+"/"+str(school_id)+"/"+str(school_name)
			client.publish(topic,"on")
client.loop_forever()