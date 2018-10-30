# -*- coding: utf-8 -*-

from flask import jsonify
from flask import render_template
from flask import Flask, request
from flask import make_response
from module import const

app = Flask(__name__)

@app.route("/get_data", methods=['GET', ])
def get_data():
	with open(const.ITEM_LST_PATH, 'r') as f:
		data = f.read()
	return jsonify({'data': data})
