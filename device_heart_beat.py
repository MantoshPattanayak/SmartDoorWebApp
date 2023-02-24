import time
import paho.mqtt.client as mqtt
import pymysql.cursors
from datetime import datetime
from datetime import date
import ping3
import logging
import pytz

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
	UTC = pytz.utc
	IST = pytz.timezone('Asia/Kolkata')
	today = date.today()
	current_time = datetime.now(IST)
	current_time =current_time.strftime('%H:%M:%S')
	current_date = today.strftime("%d/%m/%Y")

	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("20.205.208.135", 1883, 60)
	time.sleep(4)
	with connection.cursor() as cursor:
		sql = "Select device_id,device_heart_beat_time,school_id from keonjhar_school_device where device_heart_beat_time is NOT NULL"
		cursor.execute(sql)
		result = cursor.fetchall()
		connection.commit()
		device_id = result[0]['device_id']
		school_id = result[1]['school_id']
		for i in result:
			print(i)
			school_time = i['device_heart_beat_time']
			t1 = datetime.strptime(school_time,"%H:%M:%S")
			t2 = datetime.strptime(current_time, "%H:%M:%S")
			delta = t2-t1
			print("Time diff {}".format(delta.total_seconds()))
			if delta.total_seconds() <= 30.0:
				with connection.cursor() as cursor:
					sql11 = "Insert into keonjhar_log (log_type,log_school_id,log_device_id,log_description,log_time,log_date,log_alert_status) values(%s,%s,%s,%s,%s,%s,%s);"
					sql33 = "update keonjhar_school_device set device_heartbeat_status = %s where device_id=%s and school_id=%s"
					cursor.execute(sql33,("Online",int(device_id),int(school_id)))
					cursor.execute(sql11,("device_online",int(school_id),int(device_id),"device Online",str(current_time),str(current_date),"0"))
					result = cursor.fetchall()
					connection.commit()
					print("Offline")
			else:
				with connection.cursor() as cursor:
					sql11 = "Insert into keonjhar_log (log_type,log_school_id,log_device_id,log_description,log_time,log_date,log_alert_status) values(%s,%s,%s,%s,%s,%s,%s);"
					sql22 = "update keonjhar_school_device set device_heartbeat_status = %s where device_id=%s and school_id=%s"
					cursor.execute(sql22,("Offline",int(device_id),int(school_id)))
					cursor.execute(sql11,("device_offline",int(school_id),int(device_id),"device Offline",str(current_time),str(current_date),"0"))
					result = cursor.fetchall()
					connection.commit()
				print("Offline")
		