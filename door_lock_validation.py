import time
import paho.mqtt.client as mqtt
import pymysql.cursors

global data
global username
global password
global crc

connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
def execute_sql(data):
	with connection.cursor() as cursor:
		global password
		sql = data
		cursor.execute(sql,(password))
		result = cursor.fetchone()
		#print("SQL Data {}".format(result))
		if result == None:
			client.publish("get/data","Wrong password")
		else:
			print(result)
		#return result['user_password']
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Sent/Data/Server/keonjhar")

def on_message(client, userdata, msg):
	global password
	print("Data arrived {}".format(str(msg.payload)))
	print('\n')
	data = msg.payload.decode(encoding='utf-8')
	data2 = data.split('/')
	print(data2)
	print('\n')
	print("Data's Metadata {}".format(str(msg.topic)))
	#let's assume the data is "School1/username/password_payload"
	username = str(data2[1])
	password = str(data2[2])
	execute_sql("Select * from okcl_school_user WHERE user_password =%s")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("20.205.208.135", 1883, 60)
client.loop_forever()