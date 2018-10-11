#encoding=utf-8

def get_content_list(input_file):
	p_input = open(input_file,'r')
	out_list = p_input.readlines()
	p_input.close()

	return out_list

def get_conceptID_dict(content_list):
	out_dict = dict()
	g_concept_id=1000000
	for item in content_list:
		if "code" in item:
			continue

		tmp_list = item.strip().split(',')
		concept = tmp_list[3]
		if concept not in out_dict:
			out_dict[concept]=str(g_concept_id)
			g_concept_id +=1
	return out_dict

def create_stock_csv(concept_content_list):
	stock   = open('stock.csv','w')
	stock.write("stockID:ID,stock_name,:LABEL\n")
	
	industry_content_list = get_content_list('stock_industry_prep.csv')
	concept_content_list = get_content_list('stock_concept_prep.csv')

	# delete repeate
	stock_dict = dict()
	for item in industry_content_list:
		if "code" in item:
			continue

		tmp_list = item.strip().split(',')
		code = tmp_list[1]
		company_name = tmp_list[2]
		if code not in stock_dict:
			stock_dict[code]=company_name

	for item in concept_content_list:
		if "code" in item:
			continue

		tmp_list = item.strip().split(',')
		code = tmp_list[1]
		company_name = tmp_list[2]
		if code not in stock_dict:
			stock_dict[code]=company_name

	# write file
	for code in stock_dict:
		company_name = stock_dict[code]
		if "ST" in company_name:
			stock.write(code+","+company_name+",COMPANY;ST\n")
		else:
			stock.write(code+","+company_name+",COMPANY\n")

	stock.close()

def create_concept_csv(conceptID_dict):
	concept = open('concept.csv','w')
	concept.write("conceptID:ID,concept_name,:LABEL\n")
	
	for key in conceptID_dict:
		conceptID = conceptID_dict[key]
		concept.write(str(conceptID)+","+key+",CONCEPT\n")
	concept.close()

def create_stockconcept(content_list,conceptID_dict):
	stock_concept   = open('stock_concept.csv','w')
	stock_concept.write(":START_ID,:END_ID,:TYPE\n")
	for item in content_list:

		if "code" in item:
			continue

		tmp_list = item.strip().split(',')
		code = tmp_list[1]
		concept_name = tmp_list[3]
		conceptID = conceptID_dict[concept_name]

		stock_concept.write(code+","+str(conceptID)+",BELONGS_CONCEPT\n")

	stock_concept.close()

def create_stock_concept_stockconcept():

	content_list = get_content_list('stock_concept_prep.csv')
	conceptID_dict =get_conceptID_dict(content_list)

	create_stock_csv(content_list)
	create_concept_csv(conceptID_dict)
	create_stockconcept(content_list,conceptID_dict)

if __name__ == "__main__":

	create_stock_concept_stockconcept()