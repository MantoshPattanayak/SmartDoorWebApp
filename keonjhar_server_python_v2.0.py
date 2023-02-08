import time
import paho.mqtt.client as mqtt
import pymysql.cursors
from datetime import datetime
from datetime import date
import ping3
import logging
import pytz
logging.basicConfig(filename="/home/azureiotuser/server.log",format='%(asctime)s %(message)s',filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	logger.info("Started Connection and Connected with MQTT")
	with connection.cursor() as cursor:
		topic = []
		sql = "Select keonjhar_school_device.device_id,keonjhar_school_device.School_id,keonjhar_school.school_name from keonjhar_school_device join keonjhar_school on keonjhar_school_device.school_id = keonjhar_school.school_id"
		cursor.execute(sql)
		result = cursor.fetchall()
		connection.commit()
		logger.debug("Reterived Data from Database for subscribtion")
		for i in result:
			topic.append((str(i["device_id"])+"/"+str(i["School_id"])+"/"+str(i["school_name"]),0))
		try:
			for i in topic:
				print(i)
			client.subscribe(topic)
			logger.info("Subscribed to all the topics")
		except Exception as e:
			raise e
		else:
			print("")
			logger.warning("Unable to subcribe to school topic")
def door_validation(filtered_data,topic_data):
	UTC = pytz.utc
	IST = pytz.timezone('Asia/Kolkata')
	today = date.today()
	current_time = datetime.now(IST)
	current_time =current_time.strftime('%H:%M:%S')
	current_date = today.strftime("%d/%m/%Y")
	logger.info("Door Data Arrived")
	connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
	logger.info("Door_Sensor Data arrived")
	print("Validating data...")
	topic_data = topic_data
	data = filtered_data[3].split('@')
	emp_id = data[0]
	password = data[1]
	school_id = data[2]
	device_id = filtered_data[0]
	with connection.cursor() as cursor:
		sql = "Select emp_id,user_password,school_id from user_data where emp_id=%s and user_password=%s and school_id=%s"
		cursor.execute(sql,(emp_id,password,school_id))
		result = cursor.fetchall()
		connection.commit()
		print('\n')
		print("Executed Data")
		logger
		#insert into log#######################
		if result == ():
			print("Wrong data entered")
			logger.warning("Wrong username and password")
			topic_data = topic_data+"/POST"
			client.publish(topic_data,"incorrect")
			with connection.cursor() as cursor:
				sql11 = "Insert into keonjhar_log (log_type,log_school_id,log_device_id,log_description,log_time,log_date,log_alert_status) values(%s,%s,%s,%s,%s,%s,%s);"
				cursor.execute(sql11,("Door_Entry Denied",int(school_id),int(device_id),"Access Denised",str(current_time),str(current_date),"0"))
				result = cursor.fetchall()
				connection.commit()
				print("Door_Entry Denied",int(school_id),int(device_id),"Access Denised",str(current_time),str(current_date),"0")
			print(topic_data)
			#insert into log#######################
		else:
			if int(emp_id) == int(result[0]["emp_id"]) and password== result[0]["user_password"]:
				with connection.cursor() as cursor:
					sql11 = "Insert into keonjhar_log (log_type,log_school_id,log_device_id,log_description,log_time,log_date,log_alert_status) values(%s,%s,%s,%s,%s,%s,%s);"
					cursor.execute(sql11,("Door_Entry Granted",int(school_id),int(device_id),"Access Granted",str(current_time),str(current_date),"0"))
					result = cursor.fetchall()
					connection.commit()
					print("Door_Entry Granted",int(school_id),int(device_id),"Access Denised",str(current_time),str(current_date),"0")
				logger.info("Correct Data entered")
				topic_data = topic_data+"/POST"
				client.publish(topic_data,"correct")
				print(topic_data)
				print("Correct password")
				#insert into log#######################
			else:
				print("wrong password")
				#insert into log#######################
def regular_data_ping(filtered_data,topic_data):

	connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
	data = filtered_data[3].split('@')
	payload = data[0]
	school_id = data[2]
	device_id = data[1]
	school_name = topic_data.split("/")
	school_name = school_name[2]
	with connection.cursor() as cursor:
		sql = "Select * from keonjhar_school_device where device_id=%s and school_id=%s"
		cursor.execute(sql,(device_id,school_id))
		result = cursor.fetchall()
		connection.commit()
		if result == ():
			print("No such devices are registered")
			# insert into login
		else:
			print("Checking data")
			if int(result[0]["device_id"])==int(device_id) and int(result[0]["school_id"]) == int(school_id) and int(payload)==0:
				print("Correct Data of device and reset not required")
				# log in logger
			else:
				print("Incorret data of the device and payload for reseting")
				# log in logger
				connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
				with connection.cursor() as cursor:
					sql = "update keonjhar_school_device set device_reset_status = 1 where device_id=%s"
					cursor.execute(sql,(device_id))
					result = cursor.fetchall()
					sql66 = "select device_id from keonjhar_school_device where school_id=%s and device_type=%s"
					cursor.execute(sql66,(int(school_id),"Alarm"))
					result4 = cursor.fetchone()
					print(result4)
					device_id=result['device_id']
					topic_alarm = str(device_id)+'/'+str(school_id)+'/'+str(school_name)+'/'+"/Set_Alert"
					print(topic_alarm)
					client.publish(topic_alarm,"theft/alarm_on")
					connection.commit()
					print("Reset status has occured for device id {}".format(device_id))
				#topic_data = topic_data+"/Ping_POST"
				#client.publish(topic_data,"theft/alarm_on")
def device_status(filtered_data,topic_data):
	UTC = pytz.utc
	IST = pytz.timezone('Asia/Kolkata')
	today = date.today()
	current_time = datetime.now(IST)
	current_time =current_time.strftime('%H:%M:%S')
	current_date = today.strftime("%d/%m/%Y")
	connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
	topic_data = topic_data
	device_id = filtered_data[0]
	school_id = filtered_data[1]
	data = filtered_data[3]
	if data == "Open":
		with connection.cursor() as cursor:
			sql ="update keonjhar_school_device set connection_status = 'Open' where device_id = %s and school_id = %s"
			sql2 ="update keonjhar_school_device set status_date = %s where device_id = %s and school_id = %s"
			sql3 ="update keonjhar_school_device set status_time = %s where device_id = %s and school_id = %s"
			cursor.execute(sql,(device_id,school_id))
			cursor.execute(sql2,(current_date,device_id,school_id))
			cursor.execute(sql3,(current_time,device_id,school_id))
			result = cursor.fetchall()
			with connection.cursor() as cursor:
					sql11 = "Insert into keonjhar_log (log_type,log_school_id,log_device_id,log_description,log_time,log_date,log_alert_status) values(%s,%s,%s,%s,%s,%s,%s);"
					cursor.execute(sql11,("Door_Entry Opened",int(school_id),int(device_id),"Door Opened",str(current_time),str(current_date),"0"))
					result = cursor.fetchall()
					connection.commit()
					print("Door_Entry Opened",int(school_id),int(device_id),"Door is opened",str(current_time),str(current_date),"0")
			connection.commit()
			print("Door is Open: -> for device_id {} & school_id {}".format(device_id,school_id))
	elif data == "Closed":
		with connection.cursor() as cursor:
			sql ="update keonjhar_school_device set connection_status = 'Closed' where device_id = %s and school_id = %s"
			sql2 ="update keonjhar_school_device set status_date = %s where device_id = %s and school_id = %s"
			sql3 ="update keonjhar_school_device set status_time = %s where device_id = %s and school_id = %s"
			cursor.execute(sql,(device_id,school_id))
			cursor.execute(sql2,(current_date,device_id,school_id))
			cursor.execute(sql3,(current_time,device_id,school_id))
			result = cursor.fetchall()
			with connection.cursor() as cursor:
					sql11 = "Insert into keonjhar_log (log_type,log_school_id,log_device_id,log_description,log_time,log_date,log_alert_status) values(%s,%s,%s,%s,%s,%s,%s);"
					cursor.execute(sql11,("Door_Entry Closed",int(school_id),int(device_id),"Door Closed",str(current_time),str(current_date),"0"))
					result = cursor.fetchall()
					connection.commit()
					print("Door Closed",int(school_id),int(device_id),"Door Closed",str(current_time),str(current_date),"0")
			connection.commit()
			print("Door is closed: -> device_id {} & school_id {}".format(device_id,school_id))
	elif data == "Forced Entry":
		with connection.cursor() as cursor:
			sql ="update keonjhar_school_device set connection_status = 'Forced_Entry' where device_id = %s and school_id = %s"
			sql2 ="update keonjhar_school_device set status_date = %s where device_id = %s and school_id = %s"
			sql3 ="update keonjhar_school_device set status_time = %s where device_id = %s and school_id = %s"
			cursor.execute(sql,(device_id,school_id))
			cursor.execute(sql2,(current_date,device_id,school_id))
			cursor.execute(sql3,(current_time,device_id,school_id))
			topic_alarm = topic_data+"/Set_Alert"
			client.publish(topic_alarm,"theft/alarm_on")
			print(topic_alarm)
			result = cursor.fetchall()
			with connection.cursor() as cursor:
					sql11 = "Insert into keonjhar_log (log_type,log_school_id,log_device_id,log_description,log_time,log_date,log_alert_status) values(%s,%s,%s,%s,%s,%s,%s);"
					cursor.execute(sql11,("Forced Entry",int(school_id),int(device_id),"Door Break",str(current_time),str(current_date),"0"))
					result = cursor.fetchall()
					connection.commit()
					print("Door Break",int(school_id),int(device_id),"Door Break",str(current_time),str(current_date),"0")
			connection.commit()
			print("Forced_Entry has been set off for device_id {} & school_id {}".format(device_id,school_id))
	elif data == "Open from Inside":
		with connection.cursor() as cursor:
			sql ="update keonjhar_school_device set connection_status = 'Open_from_Inside' where device_id = %s and school_id = %s"
			sql2 ="update keonjhar_school_device set status_date = %s where device_id = %s and school_id = %s"
			sql3 ="update keonjhar_school_device set status_time = %s where device_id = %s and school_id = %s"
			cursor.execute(sql,(device_id,school_id))
			cursor.execute(sql2,(current_date,device_id,school_id))
			cursor.execute(sql3,(current_time,device_id,school_id))
			result = cursor.fetchall()
			with connection.cursor() as cursor:
					sql11 = "Insert into keonjhar_log (log_type,log_school_id,log_device_id,log_description,log_time,log_date,log_alert_status) values(%s,%s,%s,%s,%s,%s,%s);"
					cursor.execute(sql11,("Door Opened",int(school_id),int(device_id),"Door Opened from Inside",str(current_time),str(current_date),"0"))
					result = cursor.fetchall()
					connection.commit()
					print("Door Opened",int(school_id),int(device_id),"Door Opened from Inside",str(current_time),str(current_date),"0")
			connection.commit()
			print("Door is open: -> device_id {} & school_id {}".format(device_id,school_id))
	else:
		print("Wrong Data")
def door_info(filtered_data,topic_data):
	UTC = pytz.utc
	IST = pytz.timezone('Asia/Kolkata')
	today = date.today()
	current_time = datetime.now(IST)
	current_time =current_time.strftime('%H:%M:%S')
	current_date = today.strftime("%d/%m/%Y")
	topic_data = topic_data
	data = filtered_data[3].split('@')
	ip = data[0]
	mac = data[1]
	device_id = filtered_data[0]
	school_id = filtered_data[1]
	#print(ip,mac,device_id,school_id)
	connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		sql = "update keonjhar_school_device set device_ip=%s,device_mac=%s,device_heart_beat_time=%s,device_heart_beat_date=%s where device_id=%s and school_id=%s"
		cursor.execute(sql,(ip,mac,str(current_time),str(current_date),device_id,school_id))
		result = cursor.fetchall()
		connection.commit()
		print("Device Ip {} and Mac {} are update for {}:::{}".format(ip,mac,device_id,school_id))
def alarm_info(filtered_data,topic_data):
	UTC = pytz.utc
	IST = pytz.timezone('Asia/Kolkata')
	today = date.today()
	current_time = datetime.now(IST)
	current_time =current_time.strftime('%H:%M:%S')
	current_date = today.strftime("%d/%m/%Y")
	topic_data = topic_data
	data = filtered_data[3].split('@')
	ip = data[0]
	mac = data[1]
	device_id = filtered_data[0]
	school_id = filtered_data[1]
	#print(ip,mac,device_id,school_id)
	connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		sql = "update keonjhar_school_device set device_ip=%s,device_mac=%s,device_heart_beat_time=%s,device_heart_beat_date=%s where device_id=%s and school_id=%s"
		cursor.execute(sql,(ip,mac,str(current_time),str(current_date),device_id,school_id))
		result = cursor.fetchall()
		connection.commit()
		print("Device Ip {} and Mac {} are update for {}:::{}".format(ip,mac,device_id,school_id))
def sensor_info(filtered_data,topic_data):
	UTC = pytz.utc
	IST = pytz.timezone('Asia/Kolkata')
	today = date.today()
	current_time = datetime.now(IST)
	current_time =current_time.strftime('%H:%M:%S')
	current_date = today.strftime("%d/%m/%Y")
	topic_data = topic_data
	data = filtered_data[3].split('@')
	ip = data[0]
	mac = data[1]
	device_id = filtered_data[0]
	school_id = filtered_data[1]
	#print(ip,mac,device_id,school_id)
	connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		sql = "update keonjhar_school_device set device_ip=%s,device_mac=%s,device_heart_beat_time=%s,device_heart_beat_date=%s where device_id=%s and school_id=%s"
		cursor.execute(sql,(ip,mac,str(current_time),str(current_date),device_id,school_id))
		result = cursor.fetchall()
		connection.commit()
		print("Device Ip {} and Mac {} are update for {}:::{}".format(ip,mac,device_id,school_id))
def sensor_validation(filtered_data,topic_data):
	UTC = pytz.utc
	IST = pytz.timezone('Asia/Kolkata')
	today = date.today()
	current_time = datetime.now(IST)
	current_time =current_time.strftime('%H:%M:%S')
	current_date = today.strftime("%d/%m/%Y")
	connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
	topic_data = topic_data
	data = filtered_data[3].split("@")
	temp = data[0]
	hum = data[1]
	mq2 = data[2]
	print(data)
	print(temp)
	print(hum)
	print(mq2)
	device_id =  filtered_data[0]
	school_id = filtered_data[1]
	with connection.cursor() as cursor:
		sql = "update keonjhar_school_device set device_id=%s,device_temp=%s,device_hum=%s,device_mq2=%s,school_id=%s where device_id=%s"
		sql2 = "Insert into sensor_data_keonjhar(device_id,school_id,device_smoke_data,device_temperature,device_humidity,received_date,recevied_time) values(%s,%s,%s,%s,%s,%s,%s);"
		cursor.execute(sql,(int(device_id),float(temp),float(hum),float(mq2),int(school_id),int(device_id)))
		cursor.execute(sql2,(int(device_id),int(school_id),float(mq2),float(temp),float(hum),str(current_date),str(current_time)))
		result = cursor.fetchall()
		connection.commit()
		print("Done sensor upload")
def on_message(client, userdata, msg):
	print("Data arrived")
	print('\n')
	incoming_data = msg.payload.decode("utf-8")
	topic_data = msg.topic.encode('utf-8').decode('utf-8')
	filtered_data = incoming_data.split('/')
	print(filtered_data)
	print(len(filtered_data))
	if filtered_data[4] == "door":
		door_validation(filtered_data,topic_data)
	elif filtered_data[4] == "sensor":
		sensor_validation(filtered_data,topic_data)
	elif filtered_data[4] == "ping":
		regular_data_ping(filtered_data,topic_data)
	elif filtered_data[4] == "doorStat":
		device_status(filtered_data,topic_data)
	elif filtered_data[4] == "door_info":
		door_info(filtered_data, topic_data)
	elif filtered_data[4] == "Siren_Hbeat":
		alarm_info(filtered_data, topic_data)
	elif filtered_data[4] == "sensor_info":
		sensor_info(filtered_data, topic_data)
	else:
		print("incorrect data arrived")
		logger.warning("Incorrect Data has Arrived")

while True:
	try:
		connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
		client = mqtt.Client()
		client.on_connect = on_connect
		client.on_message = on_message
		client.connect("20.205.208.135", 1883, 60)		
	except Exception as e:
		raise e
	else:
		print("Restarting")
	client.loop_forever()