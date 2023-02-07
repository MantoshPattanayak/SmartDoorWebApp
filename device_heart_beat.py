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
		sql = "Select device_id,device_heart_beat_time from keonjhar_school_device where device_heart_beat_time is NOT NULL"
		cursor.execute(sql)
		result = cursor.fetchall()
		connection.commit()
		print(type(result))
		print(result)
		with connection.cursor() as cursor:
			for i in range(0,len(result)):
				school_time = result[i]['device_heart_beat_time']
				sql = "Select Timestampdiff(minute,%s,%s)"
				cursor.execute(sql,(school_time,current_time))
				result = cursor.fetchone()
				print(result)
				if result > 1:
					print("Device {} offline".format(result[0]['device_id']))
				else:
					print("Device {} online".format(result[0]['device_id']))