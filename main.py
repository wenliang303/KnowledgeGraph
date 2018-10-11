#encoding=utf-8
import tushare as ts
import os,time,re,time,json
import urllib.request,requests
from bs4 import  BeautifulSoup
from urllib import parse

def get_pre_of_industry_concept():
	# get info
	df = ts.get_industry_classified() 
	df.to_csv("stock_industry_prep.csv")

	df = ts.get_concept_classified()
	df.to_csv("stock_concept_prep.csv")

def get_age(age_list, sex):
	age = "0"
	if len(age_list) > 1:
		if sex == "None":
			age_group= re.match(r"\d+",age_list[0])
		else:
			age_group= re.match(r"\d+",age_list[1])
		
		if age_group != None :
			age = age_group.group(0)
	return age

def get_name(name):
	name = name.strip().replace(",","")
	if ' ' in name:
		name ="\""+name+"\""
	name = name.replace('\u4dae',"龚")
	return name

def create_executive_executive_stock():

	target_dir = os.path.join(os.path.abspath("."),'exe_member',"target")
	file_list = os.listdir(target_dir)
	executive=open('executive.csv','w')
	executive.write("persionID:ID,person_name,age:int,sex,:LABEL\n")

	executive_stock=open('executive_stock.csv','w')
	executive_stock.write(":START_ID,:END_ID,:TYPE\n")

	person_id= 1
	for f in file_list:
		file = os.path.join(target_dir,f)
		if not f.endswith("html"):
			continue
			 
		htmlfile = open(file, 'r')

		htmlhandle = htmlfile.read()
		soup = BeautifulSoup(htmlhandle, "html.parser")

		#code = soup.find("a",{"posid":"r1c2"}).get("title").strip().split(' ')[1]
		code = f.strip().replace('.html','')

		tb_BODs= soup.find_all("table",{"class":"m_table managelist m_hl"})
		if len(tb_BODs) > 0:
			tb_BOD = tb_BODs[0]
		else:
			print(file)
			continue

		tbs = tb_BOD.find_all(("table",{"class":"m_table ggintro"}))
		for tb  in tbs:
			trs = tb.find_all("tr")
			tds = trs[0].find_all('td')

			name = get_name(tds[0].get_text())
			duty = tds[1].get_text().strip()

			sex_age = trs[1].find('td').get_text().strip().replace("  "," ").replace("  "," ")
			tmp_list = sex_age.split(" ")
			sex = tmp_list[0]

			if sex !='男' and sex != '女':
				sex="None"

			age = get_age(tmp_list, sex)
			executive.write(str(person_id)+","+name+","+age+","+sex+",person\n")
			#print(name, age, code, duty)
			if "," in duty:
				duty_list = duty.split(',')
				for dt in duty_list:
					executive_stock.write(str(person_id)+","+code+","+dt.strip()+"\n")
			else:
				executive_stock.write(str(person_id)+","+code+","+duty+"\n")
			person_id +=1

	executive.close()
	executive_stock.close()

if __name__ == "__main__":
	get_pre_of_industry_concept()
	create_executive_executive_stock()

