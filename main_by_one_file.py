#encoding=utf-8
import tushare as ts
import os,time,re,time,json
import urllib.request,requests
from bs4 import  BeautifulSoup
from urllib import parse


target_dir = os.path.join(os.path.abspath("."),'exe_member',"target")
file_list = os.listdir(target_dir)
out_file=open('executive_prep.csv','w')
out_file.write("高管姓名,性别,年龄,股票代码,职位\n")



file=os.path.join(os.path.abspath("."),'exe_member',"target",'601999.html')
print(file)

htmlfile = open(file, 'r')
htmlhandle = htmlfile.read()
soup = BeautifulSoup(htmlhandle, "html.parser")

#code = soup.find("a",{"posid":"r1c2"}).get("title").strip().split(' ')[1]
code = file.strip().replace('.html','')

tb_BODs= soup.find_all("table",{"class":"m_table managelist m_hl"})
if len(tb_BODs) > 0:
	tb_BOD = tb_BODs[0]


tbs = tb_BOD.find_all(("table",{"class":"m_table ggintro"}))
for tb  in tbs:
	trs = tb.find_all("tr")
	tds = trs[0].find_all('td')


	name = tds[0].get_text().strip()
	duty = tds[1].get_text().strip()

	sex_age = trs[1].find('td').get_text().strip().replace("  "," ").replace("  "," ")
	tmp_list = sex_age.split(" ")
	sex = tmp_list[0]
	age = "None"
	if len(tmp_list) > 1:

		age_group= re.match(r"\d+",tmp_list[1])
		if age_group != None :
			age = age_group.group(0)
	print(name.replace('\u4dae',"龚"))

	print( age, code, duty)
	#out_file.write(name+","+sex+","+age+","+code+","+duty+"\n")

out_file.close()
#print(len(tbs))

