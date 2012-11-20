#! /usr/bin/env python
#
# ServerSide Component of a browser based switch 
#
# Sam Machin - theLab Nov 2012
#

import cherrypy
import urllib
import urllib2
import json
import memcache
import os


mc = memcache.Client(['127.0.0.1:11211'], debug=0)
STATIC_DIR = os.path.join(os.path.abspath("."), u"static")



class start(object):
	def index(self):
		return open(os.path.join(STATIC_DIR, u'index.html'))
	def state(self, var=None, **params):
		switch = str(urllib.unquote(cherrypy.request.params['switch']))
		state = mc.get(switch)
		data = {}
		data['switch'] = []
		data['switch'].append(state)
		return json.dumps(data)
	def on(self, var=None, **params):
		switch = str(urllib.unquote(cherrypy.request.params['switch']))
		mc.set(switch, "on")
		return "ok"
	def off(self, var=None, **params):	
		switch = str(urllib.unquote(cherrypy.request.params['switch']))
		mc.set(switch, "off")
		return "ok"
	index.exposed = True
	state.exposed = True
	on.exposed = True
	off.exposed = True

cherrypy.config.update(os.path.join(os.path.abspath("."), u"app.cfg"))
app = cherrypy.tree.mount(start(), '/', os.path.join(os.path.abspath("."), u"app.cfg"))
cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 9010})

if hasattr(cherrypy.engine, "signal_handler"):
    cherrypy.engine.signal_handler.subscribe()
if hasattr(cherrypy.engine, "console_control_handler"):
    cherrypy.engine.console_control_handler.subscribe()
cherrypy.engine.start()
cherrypy.engine.block()