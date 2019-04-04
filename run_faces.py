import find_faces
import cv2
import sys
import sqlite3
import csv
import json
import pandas as pd  
from sklearn import svm
from sklearn.externals import joblib
from PIL import Image,ImageDraw,ImageFont
import time
from identify_face_video import face_video
from identify_face_image import face_image
	
def convert_date(string):
	if string.find("-")!=-1:
	 	temp = string.split('-')
	 	x = str(temp[2])+"_"+str(temp[1])+"_"+str(temp[0])
	 	return x
	return string

def take_attendence(date, filename, course):
	threshold = 0.6
	conn = sqlite3.connect('student.db')
	print('opened succesfully')
	json_file = "Data/dictionary_reverse.json"
	json_rev_file = "Data/dictionary.json"
	with open (json_file) as data_file:
		dictionary = json.load(data_file)

	with open (json_rev_file) as data_file:
		dictionary_rev = json.load(data_file)

	table_name = "attendence"+course
	cursor = conn.execute("select id,name from %s"%(table_name))
	ids = []
	names = {}
	for row in cursor:
		ids.append(row[0])
		names[row[0]] = row[1]
	#Call function from identify_face_video.py
	found_ids = face_video(filename)
	print("i found array: ",found_ids)
	date = "\""+date+"\""
	print(found_ids)
	conn.execute("alter table %s\
		add %s INT default 0" %(table_name, date))

	conn.commit()

	for x in found_ids:
		conn.execute("update %s set total_attendence = total_attendence+1 where id=%d"%(table_name,int(x)))
		conn.execute("update %s set %s = 1 where id=%d"%(table_name,date,int(x)))

	conn.commit()

	df = pd.read_sql_query("select * from %s"%(table_name),conn)
	df1 = df.pop('total_attendence')
	df['total_attendence'] = df1
	head = df.columns

	new_head = []
	for x in head:
		new_head.append(convert_date(x))

	df.columns = new_head
	
	csv_file = "CSV/"+table_name+".csv"
	df.to_csv(csv_file, index=False)

	json_file = "Data/"+table_name+".json"
	with open (json_file) as data_file:
		data = json.load(data_file)
	cursor = conn.execute("select id, total_attendence from %s"%(table_name))
	dictionary = {}
	for row in cursor:
		dictionary[row[0]]=row[1]
	for (i,x) in enumerate(data['students']):
		if x['id'] in dictionary:
			data['students'][i]['attendence']=dictionary[x['id']]
			del(dictionary[x['id']])
	for x in dictionary:
		temp={}
		temp['id']=x
		temp['attendence']=dictionary[x]
		data['students'].append(temp)

	with open(json_file, 'w') as outfile:
		json.dump(data, outfile)

	conn.close()
	return found_ids

def take_attendence_image(date, filename, course):
	threshold = 0.6
	conn = sqlite3.connect('student.db')
	print('opened succesfully')
	json_file = "Data/dictionary_reverse.json"
	json_rev_file = "Data/dictionary.json"
	with open (json_file) as data_file:
		dictionary = json.load(data_file)

	with open (json_rev_file) as data_file:
		dictionary_rev = json.load(data_file)

	table_name = "attendence"+course
	cursor = conn.execute("select id,name from %s"%(table_name))
	ids = []
	names = {}
	for row in cursor:
		ids.append(row[0])
		names[row[0]] = row[1]
	#Call function from identify_face_image.py
	found_ids = face_image(filename)
	print("i found array: ",found_ids)
	date = "\""+date+"\""
	print(found_ids)
	conn.execute("alter table %s\
		add %s INT default 0" %(table_name, date))

	conn.commit()

	for x in found_ids:
		conn.execute("update %s set total_attendence = total_attendence+1 where id=%d"%(table_name,int(x)))
		conn.execute("update %s set %s = 1 where id=%d"%(table_name,date,int(x)))

	conn.commit()

	df = pd.read_sql_query("select * from %s"%(table_name),conn)
	df1 = df.pop('total_attendence')
	df['total_attendence'] = df1
	head = df.columns

	new_head = []
	for x in head:
		new_head.append(convert_date(x))

	df.columns = new_head
	
	csv_file = "CSV/"+table_name+".csv"
	df.to_csv(csv_file, index=False)

	json_file = "Data/"+table_name+".json"
	with open (json_file) as data_file:
		data = json.load(data_file)
	cursor = conn.execute("select id, total_attendence from %s"%(table_name))
	dictionary = {}
	for row in cursor:
		dictionary[row[0]]=row[1]
	for (i,x) in enumerate(data['students']):
		if x['id'] in dictionary:
			data['students'][i]['attendence']=dictionary[x['id']]
			del(dictionary[x['id']])
	for x in dictionary:
		temp={}
		temp['id']=x
		temp['attendence']=dictionary[x]
		data['students'].append(temp)

	with open(json_file, 'w') as outfile:
		json.dump(data, outfile)

	conn.close()
	return found_ids
