from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

'''
KEY = "9932b264-c9dd-412f-9b4c-c4f030e19f26"
TOKEN = "knbFEckkVDrqLNIYoSGiI06CN8icECXsGGkmICP5DCfrFsiITj6agRjWycYQICGIZMEIFGxkElL44WPNJJRT4OOWQBusAAQ7gQqhbG66tWGlsVkwmYNvhS68tpYmIbqfvdevoU8Xq8s6IIvPZQ1ns5"
'''

KEY = 'f08efe56-ed9d-44f3-818e-78f16ecf6b45'
TOKEN = 'PjzEcZyAjsOgxQGe2a1DYvud2Bb9yahGm0OSXTSMPC9umc4LCCheGSnsEI2cNV404T2VKv0mQxGAXeOobmyHVW3NI7W4B0iAi8kCNBKwy84JUXT2VMxI8djIs4CwEwaZCG7masBFhH6JYq1ijHsb9h'

BASE_URL = 'https://api.us.cumul.io/0.1.0/'

CUSTOM_INTEGRATION = "fd1a18fa-a8f1-4ec9-9ecd-19669dc76ac3"

@app.route('/', methods=['GET'])
def index():
	return "Hello World"

@app.route('/api/v1/cumul/token', methods=['POST'])
def get_cumul_token():
	import pycurl
	from io import BytesIO

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()

	data = {
	    "action": "create",
	    "version": "0.1.0",
	    "key": KEY,
	    "token": TOKEN,  
	    "properties": {
	        "integration_id": CUSTOM_INTEGRATION,
	        "type": "sso",
	        "expiry": "24 hours",
	        "inactivity_interval": "10 minutes",
	        "username": "jesus.huazano@rankmi.com",
	        "name": "Jesus Huazano",
	        "email": "jesus.huazano@rankmi.com",
	        "suborganization": "Air Force",
	        "role": "viewer",
	    }
	}


	curl_object.setopt(curl_object.URL, BASE_URL + 'authorization')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_body = json.loads( bytes_object.getvalue().decode('utf8') )

	print(get_body)

	sso_id = get_body['id']
	sso_token = get_body['token']
	sso_user_id = get_body['user_id']


	bytes_object = BytesIO()
	curl_object = pycurl.Curl()

	data = {                                       
		"action": "get",
		"version": "0.1.0",  
	    "key": KEY,
	    "token": TOKEN, 
		"find": {
			"attributes": ["id", "name", "contents", "type"],
			"include": [],
			"type": "dashboard"
		}
	}

	curl_object.setopt(curl_object.URL, BASE_URL + 'securable')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_dashboards = json.loads( bytes_object.getvalue().decode('utf8') )

	return jsonify({
		"full": get_body,
		"sso_id": sso_id,
		"sso_token": sso_token,
		"sso_user_id": sso_user_id,
		"items": get_dashboards
	})

@app.route('/api/v1/cumul/create/integration', methods=['POST'])
def create_cumul_integration():
	import pycurl
	from io import BytesIO

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()

	post_data = request.get_json()

	data = {
		"action": "create",
		"key": KEY, #post_data['key'],
		"token": TOKEN, #post_data['token'],
		"version": "0.1.0",
		"properties": {
			"name": {
				"en": "Integration EN",
				"fr": "Integration FR"
			}
		}
	}

	curl_object.setopt(curl_object.URL, BASE_URL + 'integration')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_body = json.loads( bytes_object.getvalue().decode('utf8') )
	return jsonify(get_body)

@app.route('/api/v1/cumul/associate/integration/dataset', methods=['POST'])
def create_cumul_integration_associate_dataset():
	import pycurl
	from io import BytesIO

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()

	post_data = request.get_json()

	data = {
		"action": "associate",
		"key": KEY,
		"token": TOKEN,
		"version": "0.1.0",
		"id": post_data['integration_id'],
		"resource": {
			"role": "Securables",
			"id": post_data['dataset_id']
		},
		"properties": {
			"flagRead": True
		}
	}


	curl_object.setopt(curl_object.URL, BASE_URL + 'integration')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_body = json.loads( bytes_object.getvalue().decode('utf8') )
	return jsonify(get_body)

@app.route('/api/v1/cumul/associate/integration/dashboard', methods=['POST'])
def create_cumul_integration_associate_dashboard():
	import pycurl
	from io import BytesIO

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()

	post_data = request.get_json()

	data = {
		"action": "associate",
		"key": KEY,
		"token": TOKEN,
		"version": "0.1.0",
		"id": post_data['integration_id'],
		"resource": {
			"role": "Securables",
			"id": post_data['dashboard_id']
		},
		"properties": {
			"flagRead": True
		}
	}


	curl_object.setopt(curl_object.URL, BASE_URL + 'integration')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_body = json.loads( bytes_object.getvalue().decode('utf8') )
	return jsonify(get_body)



@app.route('/api/v1/cumul/token/multitenancy', methods=['POST'])
def get_cumul_token_multitenancy():
	import pycurl
	from io import BytesIO

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()

	data = {
	    "action": "create",
	    "version": "0.1.0",
	    "key": KEY,
	    "token": TOKEN,  
	    "properties": {
	        "integration_id": CUSTOM_INTEGRATION,
	        "type": "sso",
	        "expiry": "24 hours",
	        "inactivity_interval": "10 minutes",
	        "username": "jesus.huazano@rankmi.com",
	        "name": "Jesus Huazano",
	        "email": "jesus.huazano@rankmi.com",
	        "suborganization": "Air Force",
	        "role": "viewer",
			"account_overrides": { 
				"2de71311-daed-475e-81c5-9444ac95a15e" : {
					"host": "cumul2.cetlhze6fmhm.us-east-2.rds.amazonaws.com",
					"port": "5432",
					"user": "postgres",
					"password": "sw123456",
					"database": "sip",
					"schema": "catalogos",
					"table": "pais"
				},
				"0c3711d6-0dcd-462f-8da2-e9cc38b61841": {
					"host": "cumul1.cetlhze6fmhm.us-east-2.rds.amazonaws.com",
					"port": "5432",
					"user": "postgres",
					"password": "sw123456",
					"database": "sip2",
					"schema": "catalogos",
					"table": "estado"
				},
				"32ac3cee-1a6f-46f0-8ef9-4be122a6bd7d":{
					"host": "cumul1.cetlhze6fmhm.us-east-2.rds.amazonaws.com",
					"port": "5432",
					"user": "postgres",
					"password": "sw123456",
					"database": "sip2",
					"schema": "catalogos",
					"table": "municipio"
				}
			}
	    }
	}


	curl_object.setopt(curl_object.URL, BASE_URL + 'authorization')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_body = json.loads( bytes_object.getvalue().decode('utf8') )

	sso_id = get_body['id']
	sso_token = get_body['token']
	sso_user_id = get_body['user_id']

	return jsonify({
		"full": get_body,
		"sso_id": sso_id,
		"sso_token": sso_token,
		"sso_user_id": sso_user_id,
	})


@app.route('/api/v1/cumul/token/multitenancy/user1', methods=['POST'])
def get_cumul_token_multitenancy_user1():
	import pycurl
	from io import BytesIO

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()
	post_data = request.get_json()

	data = {
	    "action": "create",
	    "version": "0.1.0",
	    "key": KEY,
	    "token": TOKEN,  
	    "properties": {
	        "integration_id": "fd1a18fa-a8f1-4ec9-9ecd-19669dc76ac3",
	        "type": "sso",
	        "expiry": "24 hours",
	        "inactivity_interval": "10 minutes",
	        "username": "jesus.huazano@rankmi.com",
	        "name": "Jesus Huazano",
	        "email": "jesus.huazano@rankmi.com",
	        "suborganization": "Air Force",
	        "role": "viewer",
			"account_overrides": { 
				"2de71311-daed-475e-81c5-9444ac95a15e" : {
					"datasets": {
						"d43d8d98-ae55-4358-819d-7587d2df34c3" : {
							"schema": "<schema>",
							"table": "<table>"

						}
					}
				}
			}
	    }
	}


	curl_object.setopt(curl_object.URL, BASE_URL + 'authorization')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_body = json.loads( bytes_object.getvalue().decode('utf8') )

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()

	data = {                                       
		"action": "get",
		"version": "0.1.0",
	    "key": KEY,
	    "token": TOKEN,  
		"find": {
		"where": {
			"id": "d43d8d98-ae55-4358-819d-7587d2df34c3",
			"type": "dataset"
		},
		"include":[{
			"model": "Column",
			"attributes": ["name", "type"]
		}],
		"attributes": ["name", "rows", "created_at"]
		}
	}


	curl_object.setopt(curl_object.URL, BASE_URL + 'securable')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_columns = json.loads( bytes_object.getvalue().decode('utf8') )

	sso_id = get_body['id']
	sso_token = get_body['token']
	sso_user_id = get_body['user_id']

	return jsonify({
		"columns": get_columns,
		"full": get_body,
		"sso_id": sso_id,
		"sso_token": sso_token,
		"sso_user_id": sso_user_id,
	})



@app.route('/api/v1/cumul/token/multitenancy/user2', methods=['POST'])
def get_cumul_token_multitenancy_user2():
	import pycurl
	from io import BytesIO

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()
	post_data = request.get_json()

	data = {
	    "action": "create",
	    "version": "0.1.0",
	    "key": KEY,
	    "token": TOKEN,  
	    "properties": {
	        "integration_id": "fd1a18fa-a8f1-4ec9-9ecd-19669dc76ac3",
	        "type": "sso",
	        "expiry": "24 hours",
	        "inactivity_interval": "10 minutes",
	        "username": "jesus.huazano2@rankmi.com",
	        "name": "Jesus Huazano 2",
	        "email": "jesus.huazano2@rankmi.com",
	        "suborganization": "Air Force",
	        "role": "viewer",
			"account_overrides": { 
				"2de71311-daed-475e-81c5-9444ac95a15e" : {
					"datasets": {
						"d43d8d98-ae55-4358-819d-7587d2df34c3" : {
							"schema": "<schema>",
							"table": "<table>"

						}
					}
				}
			}
	    }
	}


	curl_object.setopt(curl_object.URL, BASE_URL + 'authorization')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_body = json.loads( bytes_object.getvalue().decode('utf8') )

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()

	data = {                                       
		"action": "get",
		"version": "0.1.0",
	    "key": KEY,
	    "token": TOKEN,  
		"find": {
		"where": {
			"id": "d43d8d98-ae55-4358-819d-7587d2df34c3",
			"type": "dataset"
		},
		"include":[{
			"model": "Column",
			"attributes": ["name", "type"]
		}],
		"attributes": ["name", "rows", "created_at"]
		}
	}


	curl_object.setopt(curl_object.URL, BASE_URL + 'securable')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_columns = json.loads( bytes_object.getvalue().decode('utf8') )

	sso_id = get_body['id']
	sso_token = get_body['token']
	sso_user_id = get_body['user_id']

	return jsonify({
		"columns": get_columns,
		"full": get_body,
		"sso_id": sso_id,
		"sso_token": sso_token,
		"sso_user_id": sso_user_id,
	})



@app.route('/api/v1/cumul/token/multitenancy/user3', methods=['POST'])
def get_cumul_token_multitenancy_user3():
	import pycurl
	from io import BytesIO

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()
	post_data = request.get_json()

	data = {
	    "action": "create",
	    "version": "0.1.0",
	    "key": KEY,
	    "token": TOKEN,  
	    "properties": {
	        "integration_id": "fd1a18fa-a8f1-4ec9-9ecd-19669dc76ac3",
	        "type": "sso",
	        "expiry": "24 hours",
	        "inactivity_interval": "10 minutes",
	        "username": "jesus.huazano3@rankmi.com",
	        "name": "Jesus Huazano 3",
	        "email": "jesus.huazano3@rankmi.com",
	        "suborganization": "Air Force",
	        "role": "viewer",
			"account_overrides": { 
				"2de71311-daed-475e-81c5-9444ac95a15e" : {
					"host": "<host>",
					"port": "5432",
					"user": "postgres",
					"password": "123456",
					"database": "<db<",
					"schema": "<schema>",
					"table": "<table>"
				}
			}
	    }
	}


	curl_object.setopt(curl_object.URL, BASE_URL + 'authorization')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_body = json.loads( bytes_object.getvalue().decode('utf8') )

	bytes_object = BytesIO()
	curl_object = pycurl.Curl()

	data = {                                       
		"action": "get",
		"version": "0.1.0",
	    "key": KEY,
	    "token": TOKEN,  
		"find": {
		"where": {
			"id": "d43d8d98-ae55-4358-819d-7587d2df34c3",
			"type": "dataset"
		},
		"include":[{
			"model": "Column",
			"attributes": ["name", "type"]
		}],
		"attributes": ["name", "rows", "created_at"]
		}
	}


	curl_object.setopt(curl_object.URL, BASE_URL + 'securable')
	curl_object.setopt(curl_object.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
	curl_object.setopt(curl_object.POSTFIELDS, json.dumps(data).encode('utf-8'))
	curl_object.setopt(curl_object.WRITEDATA, bytes_object)
	curl_object.perform() 
	curl_object.close()

	get_columns = json.loads( bytes_object.getvalue().decode('utf8') )

	sso_id = get_body['id']
	sso_token = get_body['token']
	sso_user_id = get_body['user_id']

	return jsonify({
		"columns": get_columns,
		"full": get_body,
		"sso_id": sso_id,
		"sso_token": sso_token,
		"sso_user_id": sso_user_id,
	})



if __name__=='__main__':
	app.run(debug=True)