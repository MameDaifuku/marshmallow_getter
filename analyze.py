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

def get_file_name_list(dir_path):
	result = []
	file_path_list = sorted(glob.glob(dir_path+"/*"))
	for file_path in file_path_list:
		file_name = os.path.basename(file_path)
		result.append(file_name)
	###
	result.sort(reverse=True)
	
	
	return result
###

####################################################
def run():
	result = {}

	for file_name in get_file_name_list(dir_path_user) :
		filePath = f"{dir_path_user}/{file_name}"
		with open(filePath, mode="r", encoding="utf-8_sig") as file:
			json_file = json.loads(file.read())
			if json_file["data-updated-at"][0:7] not in 	result : result[json_file["data-updated-at"][0:7]] = 0
			result[json_file["data-updated-at"][0:7]] += 1
		###
	###
	pprint(result)
###

####################################################
user_id = config.user_id
base_url = f"https://marshmallow-qa.com/users/{user_id}/answers?"
dir_path_output = "./output"
if not os.path.exists(dir_path_output) : os.mkdir(dir_path_output)
dir_path_user = f"{dir_path_output}/{user_id}"
if not os.path.exists(dir_path_user) : os.mkdir(dir_path_user)

run()
