# -*- coding: utf-8 -*-

import glob
import time
import os
import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup

def default_method(item):
	if isinstance(item, object) and hasattr(item, '__dict__'):
		return item.__dict__
	else:
		raise TypeError
	###
###


def convert_fragment_to_array(marshmallow_id, fragment) :
	soup = BeautifulSoup(fragment, "html.parser")
	temp = {}
	temp["question"] = soup.find("div", {"data-target" : "obscene-word.content"}).get_text()
	temp["answer"] = soup.find("div", {"class" : "answer-content pre-wrap text-dark"}).get_text()
	temp["data-updated-at"] = soup.find("li", {"class" : "answer card mb-4 fade-in"})["data-updated-at"]
	temp["user_id"] = soup.find("a", {"class" : "d-flex align-items-end mb-1 no-decoration"})["href"]
	temp["user_name"] = soup.find("img", {"class" : "rounded-circle mr-2 d-flex icon-mini"})["alt"]
	temp["user_number"] = marshmallow_id
	
	return temp
###

def output_array_marshmallow(dir_path_user, array_marshmallow):
	marshmallow_answer_id = array_marshmallow["user_number"]
	print("marshmallow_answer_id = " + str(marshmallow_answer_id)) #検証用
	file_path = f"{dir_path_user}/{marshmallow_answer_id}.json"
	if not os.path.exists(file_path) : 
		with open(file_path, mode="w", encoding="utf-8_sig") as f:
			f.write(json.dumps(array_marshmallow, default=default_method, ensure_ascii=False, indent=4))
			###
		###
	###
###


def get_and_output_marshmallow(user_number) :
	print("user_number = " + user_number)
	url = f"https://marshmallow-qa.com/users/{user_number}/answers?"
	html = requests.get(url)
	
	if (html.text == "") : return # マシュマロ回答が存在しないuser_number
		
	dir_path_user = f"{dir_path_output}/{user_number}"
	if os.path.exists(dir_path_user) : return
	else : os.mkdir(dir_path_user)
	
	json_marshmallow = ""
	next_param = ""
	json_marshmallow = json.loads(html.text)
	for marshmallow in json_marshmallow :
		array_marshmallow = convert_fragment_to_array(marshmallow["id"], marshmallow["fragment"])
		output_array_marshmallow(dir_path_user, array_marshmallow)
		next_param = array_marshmallow["data-updated-at"] #ループ終了時点で次のパラメータ指定値がここにセットされた状態になる
	###
	
	return next_param
###

####################################################
def run():
	start_number = 100000
	
	for num in range(50) :
		if (num % 5 == 0) : time.sleep(5) 
		else	: time.sleep(1) 
# 		time.sleep(1) 
		
		get_and_output_marshmallow(str(start_number + num))
# 		break
	###
###

####################################################
dir_path_output = "./output"
if not os.path.exists(dir_path_output) : os.mkdir(dir_path_output)

run()