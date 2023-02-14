import time
import paho.mqtt.client as mqtt
import pymysql.cursors
from datetime import datetime
import ping3
import logging

logging.basicConfig(filename="/home/azureiotuser/server_reset.log",format='%(asctime)s %(message)s',filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
	print("Data arrived")
	print('\n')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("20.205.208.135", 1883, 60)
logger.info("Connected to MQTT")

connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
while True:
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("20.205.208.135", 1883, 60)
	time.sleep(4)
	with connection.cursor() as cursor:
		sql = "Select keonjhar_school_device.device_id,keonjhar_school_device.school_id,keonjhar_school.school_name from keonjhar_school_device join keonjhar_school on keonjhar_school_device.school_id = keonjhar_school.school_id where device_status = 1 and device_reset_status=0"
		cursor.execute(sql)
		result = cursor.fetchall()
		print("Data fetching...")
		connection.commit()
		logger.info("Data fetched from database")
		if result == ():
			print("No Device needs reset")
			logger.info("No data found from request")
		else:
			logger.info("Data Found, intiating reset request")
			print("Data Found, intiating reset request")
			#print(result)
			reset_device_id = result[0]["device_id"]
			reset_school_id = result[0]["school_id"]
			reset_school_name = result[0]["school_name"]
			for i in range(0,len(result)):
				print(result)
				topic_topic = str(reset_device_id)+"/"+str(reset_school_id)+"/"+str(reset_school_name)+"/"+"Reset_POST"
				print("Sending Reset to {}".format(topic_topic))

				client.publish(topic_topic,"reset_0")

				with connection.cursor() as cursor:
					sql33 = "select device_id,school_id from keonjhar_school_device where school_id=%s and device_type=%s"
					cursor.execute(sql33,(reset_school_id,"Alarm"))
					result4 = cursor.fetchone()
					alarm_device_id = result4['device_id']
					alarm_school_id = result4['school_id']
					sql66 = "Select school_name from keonjhar_school where school_id=%s"
					cursor.execute(sql66,(int(alarm_school_id)))
					result78 = cursor.fetchone()
					connection.commit()
					alarm_school_name = result78['school_name']
					topic2 = str(alarm_device_id)+"/"+str(alarm_school_id)+"/"+str(alarm_school_name)+ "/" + "Set_Alert"
					print("Sending Alarm data: {}".format(topic2))
					client.publish(topic2,"theft/alarm_off")
					print("Reset Send")
				with connection.cursor() as cursor:
					sql = "update keonjhar_school_device set device_status = 0, device_reset_status =0 where device_id=%s and school_id = %s;"
					cursor.execute(sql,(reset_device_id,reset_school_id))
					result = cursor.fetchall()
					connection.commit()
					print("Device has been reset {}".format(device_id))
	#client.reconnect()
		# with connection.cursor() as cursor:
		# 	sql = "select school_id from keonjhar_school_device where device_value>=50 group by school_id having count(device_value)>=2;"
		# 	cursor.execute(sql)
		# 	result = cursor.fetchall()
		# 	connection.commit()
		# 	print("Second data")
		# 	#print(result[0]["school_id"])
		# 	#print(result[1]["school_id"])
		# 	for i in range(0,len(result)):
		# 		data = result[i]["school_id"]
		# 		print(data)
		# 		with connection.cursor() as cursor:
		# 			sql ="Select keonjhar_school_device.device_id, keonjhar_school.school_name from keonjhar_school_device join keonjhar_school on keonjhar_school_device.school_id = keonjhar_school.school_id where keonjhar_school_device.school_id=%s;"
		# 			cursor.execute(sql,(data))
		# 			result=cursor.fetchall()
		# 			connection.commit()
		# 			print(result)






