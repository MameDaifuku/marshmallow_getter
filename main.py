# -*- coding: utf-8 -*-

import config
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
	temp["id"] = marshmallow_id
	
	return temp
###

def output_array_marshmallow(array_marshmallow):
	marshmallow_answer_id = array_marshmallow["id"]
	print("marshmallow_answer_id = " + str(marshmallow_answer_id)) #検証用
	file_path = f"{dir_path_user}/{marshmallow_answer_id}.json"
	if not os.path.exists(file_path) : 
		with open(file_path, mode="w", encoding="utf-8_sig") as f:
			f.write(json.dumps(array_marshmallow, default=default_method, ensure_ascii=False, indent=4))
			###
		###
	###
###

def get_and_output_marshmallow(url) :
	html = requests.get(url)
	json_marshmallow = ""
	try :
		json_marshmallow = json.loads(html.text)
	except Exception as e :
		print(html.text)
		raise e
	###
	
	for marshmallow in json_marshmallow :
		array_marshmallow = convert_fragment_to_array(marshmallow["id"], marshmallow["fragment"])
		output_array_marshmallow(array_marshmallow)
		next_param = array_marshmallow["data-updated-at"] #ループ終了時点で次のパラメータ指定値がここにセットされた状態になる
	###
	
	return next_param
###

def get_file_name_list(dir_path):
	result = []
	file_path_list = sorted(glob.glob(dir_path+"/*"))
	for file_path in file_path_list:
		file_name = os.path.basename(file_path)
		result.append(file_name)
	###
	result.sort()
	
	return result


####################################################
def run():
	next_param = "" #この変数は初回処理以降も使い回す

	# 初回処理
	next_param = get_and_output_marshmallow(base_url)
	
	# 2回目以降の処理
	for i in range(1000): #とりあえず1000回ループさせる
		#スリープを入れないとretry laterって怒られる。5回に1回の頻度で長めのスリープ。
		if (i % 5 == 0) : time.sleep(5) 
		else	: time.sleep(1) 

		next_url = f"{base_url}before={next_param}"
		next_param = get_and_output_marshmallow(next_url)
	###
###

def run_restart():
	# 途中から取り直しをし始める場合の処理
	file_name_list = get_file_name_list(dir_path_user)
	for file_name in file_name_list :
		filePath = f"{dir_path_user}/{file_name}"
		with open(filePath, mode="r", encoding="utf-8_sig") as file:
			json_file = json.loads(file.read())
			next_param = json_file["data-updated-at"]
			for i in range(1000): #とりあえず1000回ループさせる
				#スリープを入れないとretry laterって怒られる。5回に1回の頻度で長めのスリープ。
				if (i % 5 == 0) : time.sleep(5) 
				else	: time.sleep(1) 
				
				next_url = f"{base_url}before={next_param}"
				next_param = get_and_output_marshmallow(next_url)
			###			
		###
		break #TODO 暫定。最後のファイルを起点にして必ず処理できるんであれば相応の書き方に直す
	###
###

####################################################
user_id = config.user_id
base_url = f"https://marshmallow-qa.com/users/{user_id}/answers?"
dir_path_output = "./output"
if not os.path.exists(dir_path_output) : os.mkdir(dir_path_output)
dir_path_user = f"{dir_path_output}/{user_id}"
if not os.path.exists(dir_path_user) : os.mkdir(dir_path_user)

run() # 最新から順繰りに取得する
# run_restart() # 取得済みの中でdata-updated-atの日付が一番古いヤツを起点にして取得する