# -*- coding: utf-8 -*-

from gevent import monkey
from gevent import pywsgi
from module import view

def main():
	monkey.patch_all()
	server = pywsgi.WSGIServer(('127.0.0.1', 8080), view.app)
	server.serve_forever()

if __name__ == '__main__':
	main()
