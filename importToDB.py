#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import re
import MySQLdb
db = MySQLdb.connect("localhost","secevery","secevery","domains" )
cursor = db.cursor()

path = "./output/"
files = os.listdir(path)
for f in files:
	domains = open(path + f).readlines()
	for i in domains:
		line = i.strip()
		ret = re.match(r'(\S*)\s.*?([0-9.]+)', line)
		domain = ret.group(1)
		ip = ret.group(2)
		print "%-30s%s" %(domain, ip)
		sql = "INSERT INTO domains (domain , ip) VALUES	('%s', '%s')" % (domain, ip)
		#print sql
		try:
			cursor.execute(sql)
			db.commit()
		except:
			db.rollback()
			pass

db.close()
