#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# $ cat companys.txt | awk '{print $1}' > rootdomains.txt
# $ python subDomainsBrute.py -l rootdomains.txt -t 100 -i

import requests
import re

def getPagesCount():
	url = "http://butian.360.cn/company/lists"
	resp = requests.get(url)
	resp.encoding = resp.apparent_encoding
	return int(re.search(u'(\d+)">末页</a>', resp.text).group(1))

def getRootDoamin(domain):
	ret = re.search(r'([a-zA-Z0-9-]+?)\.(com\.cn|edu\.cn|gov\.cn|org\.cn|net\.cn|gq|hk|im|info|la|mobi|so|tech|biz|co|tv|me|cc|org|net|cn|com)$', domain)
	if ret ==None:
		return None
	return ret.group(0)

def getCompanyUrlList(companys):
	companyurls = []
	for i in companys:
		companyurls.append(i["url"])
	return companyurls

def getCompanyByPage(page, companys):
	print "[*] 当前第%d页." % page
	url = "http://butian.360.cn/company/lists/page/%d" % page
	resp = requests.get(url)
	resp.encoding = resp.apparent_encoding
	company_list = re.findall(r'id/\d+?">(.*?)</a></td>.*?20px;">(.*?)</td>', resp.text, re.S)
	company_name = company_url = None
	for l in company_list:
		company_name =  l[0]
		company_url =  l[1]
		company_url = getRootDoamin(company_url)
		print "%-30s%s" % (company_url, company_name)
		if company_url == None:
			continue
		if company_url not in getCompanyUrlList(companys):
			companys.append({"name": company_name, "url": company_url})

if __name__ == '__main__':
	companys = []
	pages = getPagesCount()
	print "[*] 总共有%d页" % pages
	#pages = 2
	for page in range(1, pages+1):
		getCompanyByPage(page, companys)

	f = open("companys.txt", "w")
	for company in companys:
		f.write("%-30s%s\n" % (company["url"].encode("utf-8"), company["name"].encode("utf-8")))
	f.close()

