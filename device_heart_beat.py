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