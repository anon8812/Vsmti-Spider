#!/usr/bin/python
# -*- coding: utf-8 -*-

import time, json, sys, ConfigParser
import sqlite3 as db

config = ConfigParser.ConfigParser()
config.read('config.ini')

class Log:
	def __init__(self):
		self.logfile = config.get('logging', 'logfile')
		
	def write(self, string):
		file = open(self.logfile, 'a')
		file.write('[' + time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime()) + '] ' + string + '\n')
		file.close()
		
log = Log()
import vsmti, facebook

class Manager:
	def __init__(self):
		self.fb = facebook.Facebook()
		self.vsm = vsmti.Vsmti('http://www.vsmti.hr')
		try:
			self.database = config.get('Database', 'database')
			self.connection = db.connect(self.database)
			self.dbc = self.connection.cursor()
			self.dbc.execute('CREATE TABLE IF NOT EXISTS stories (id INTEGER NOT NULL PRIMARY KEY, title VARCHAR(100), body VARCHAR(1024), has_link INTEGER, link VARCHAR(100))')
			self.dbdata = self.fetch_db(True)
			self.main_loop()
		except Exception, e:
			log.write(str(e))
			
	def fetch_db(self, check):
		self.dbc.execute('SELECT title, body, has_link, link FROM stories')
		dbdata = self.dbc.fetchall()
		dblenght = len(dbdata)
		if check == True:
			if dbdata == []:
				data = self.vsm.get_each()
				for item in data:
					log.write('Adding ' + item[0].encode('utf-8', 'replace'))
					self.dbc.execute('INSERT INTO stories (title, body, has_link, link) VALUES ("%s", "%s", %i, "%s")' % (item[0], item[1], item[2], item[3]))
					self.connection.commit()
					
			self.dbc.execute('SELECT title, body, has_link, link FROM stories')
			dbdata = self.dbc.fetchall()
			dblenght = len(dbdata)
			buff = []
			for item in dbdata:
				buff.append(list(item))
			return buff
		else:
			buff = []
			for item in dbdata:
				buff.append(list(item))
			return buff
			
	def check_new(self):
		data = self.vsm.get_each()
		datalength = len(data)
		log.write(str(datalength))
		dblength = len(self.fetch_db(False))
		if not datalength == dblength:
			log.write('New post! - ' + str(datalength-dblength))
			item = data[0]
			log.write('Adding ' + item[0] + ' to database')
			self.dbc.execute('INSERT INTO stories (title, body, has_link, link) VALUES ("%s", "%s", %i, "%s")' % (item[0], item[1], item[2], item[3]))
			self.connection.commit()
			if item[2] == 1:
				self.fb.publish_link(item)
			else:
				self.fb.publish(item)
		else:
			log.write('No change')
			
	def main_loop(self):
		while True:
			self.check_new()
			time.sleep(300)
			
if __name__ == '__main__':
	manager = Manager()
	
