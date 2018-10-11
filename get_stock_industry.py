#encoding=utf-8

def get_content_list(input_file):
	p_input = open(input_file,'r')
	out_list = p_input.readlines()
	p_input.close()

	return out_list

def get_industryID_dict(content_list):
	out_dict = dict()
	g_industry_id=2000000
	for item in content_list:

		if "code" in item:
			continue

		tmp_list = item.strip().split(',')
		industry = tmp_list[3]
		if industry not in out_dict:
			out_dict[industry]=str(g_industry_id)
			g_industry_id +=1
	return out_dict

def create_industry_csv(industryID_dict):
	industry = open('industry.csv','w')
	industry.write("industryID:ID,industry_name,:LABEL\n")
	
	for key in industryID_dict:
		industryID = industryID_dict[key]
		industry.write(str(industryID)+","+key+",INDUSTRY\n")
	industry.close()

def create_stockindustry(content_list,industryID_dict):
	stock_industry   = open('stock_industry.csv','w')
	stock_industry.write(":START_ID,:END_ID,:TYPE\n")
	for item in content_list:

		if "code" in item:
			continue

		tmp_list = item.strip().split(',')
		code = tmp_list[1]
		industry = tmp_list[3]
		industryID = industryID_dict[industry]

		stock_industry.write(code+","+str(industryID)+",BELONGS_INDUSTRY\n")

	stock_industry.close()

def create_industry__stockindustry():

	content_list = get_content_list('stock_industry_prep.csv')
	industryID_dict =get_industryID_dict(content_list)

	create_industry_csv(industryID_dict)
	create_stockindustry(content_list,industryID_dict)

if __name__ == "__main__":
	create_industry__stockindustry()