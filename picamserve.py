#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json
import time
from datetime import datetime
from datetime import timezone
import threading
import queue
from pprint import pp
from pihq_camera import pihqCamera
from daynight import DayNight
from bottle import Bottle, ServerAdapter, request, route, run, template, HTTPResponse, static_file, TEMPLATE_PATH, error
from cheroot.wsgi import Server as WSGIServer
from cheroot.ssl.builtin import BuiltinSSLAdapter
from wsgiref.simple_server import make_server, WSGIRequestHandler

class WSGIRefServer(ServerAdapter):
    server = None # class variable, not instance
    quiet = True
    logger = None

    def set_logger(self, logger):
      self.logger = logger

    def log(self, msg):
      if self.logger:
        self.logger.append_log(f'[WSGIServer]\t{msg}')

    def run(self, handler):
      self.log(f'run WSGIServer: host:{self.host} port: {self.port}')

      if self.quiet:
        class QuietHandler(WSGIRequestHandler):
          def log_request(*args, **kw):
            if args[1] != '304' and args[1] != '200':
              self.log(f'server response: {args[1]} {kw}')
        self.options['handler_class'] = QuietHandler

      self.server = make_server(self.host, self.port, handler, **self.options)
      self.server.serve_forever()

    def stop(self):
      self.log(f'shutting down')
      # self.server.server_close() # <--- alternative but causes bad fd exception
      self.server.shutdown()


class Webserver:

  def __init__(self, logger=None, host="0.0.0.0", port="8080", verbose=True, debug=False, state_transition_callback=None):
    # super().__init__(logger=logger, module_name="Webserver")
    self.verbose = verbose
    self.debug = debug
    self.host = host
    self.port = port
    self.queue = None
    self.thread = None
    # self.data = empty_data
    # self.network_connection = NetworkConnections(logger=self.logger)
    self.status = {}
    self.state_transition_callback = state_transition_callback
    # self.camera = pihqCamera()
    self.daynight = DayNight(44.6509, -63.5923)

  def log(self, message):
    print(f"WEBSERVER: {message}")

  def start_server(self):
    self.log('starting webserver...')
    try:
      self.bottle = Bottle()
      base_path = os.path.abspath(os.path.dirname('.'))
      self.log(f'using base path: {base_path}')
      TEMPLATE_PATH.insert(0, base_path + '/views')
    except Exception as e:
      self.log(f'could not instantiate Bottle...{e}')
    self.log('Bottle instantiated')
   
    # current directory name in order to reference static file paths for Bottle templates

    # get our unit config data to pass into pages:
    base_path = os.path.abspath(os.path.dirname('.'))
    #network_list_json_file = base_path + '/config/config.json'
    #with open(network_list_json_file, 'r') as f:
    #  unitdata = json.load(f)

    @self.bottle.route('/static/<filename:re:.*\.*>')
    def static(filename):
      dirname = os.path.abspath(os.path.dirname(__file__))
      # self.log(f'static path requested: {dirname}/static/{filename}') # lots of log noise
      response = static_file(filename, root=dirname+'/static')
      response.set_header("Cache-Control", "public, max-age=0") # prevent any caching
      return response


    @self.bottle.route('/latest')
    def latest():
      metadata = "METADATA"
      hms_since_boot = "hms_since_boot"
      consecutive="could not read number of consecutive frames"
      with open("./metadata.txt", "r") as f:
        metadata =  json.load(f)
        metadata_parsed = json.dumps(metadata, indent=4)
      with open("./consecutive.txt", "r") as f:
        consecutive = f.read()

      try:
        ns_since_boot = int(metadata["SensorTimestamp"])
        seconds_since_boot = ns_since_boot/1000/1000/1000
        hours_since_boot = int(seconds_since_boot/3600)
        seconds_since_boot = seconds_since_boot - hours_since_boot*3600
        minutes_since_boot = int(seconds_since_boot/60)
        seconds_since_boot = seconds_since_boot - minutes_since_boot*60
        hms_since_boot = f"{hours_since_boot}:{minutes_since_boot}:{seconds_since_boot}"
      except Exception as e:
         hms_since_boot = f"hms_since_boot parse error: {e}"
      response = template('<body style="background:black;color:white;font-size:2em"><img width="100%" src="/hireslatestimage"><br/>images so far: {{consecutive}}<br/>time since camera sensor reboot: {{hms_since_boot}}<br/>METADATA:<br/><pre>{{metadata_parsed}}</pre></body>', consecutive=consecutive, hms_since_boot = hms_since_boot, metadata_parsed = metadata_parsed)
      return response

    @self.bottle.route('/hireslatestimage')
    def hireslatestimage():
      # self.log("capturing image...")
      # self.log(f"it is currently {'day' if self.daynight.is_day() else 'night'}")
      # try:
      #   self.camera.capture("capture.jpg")
      #   self.log("capture complete")

      # except Exception as e:
      #   self.log(f"ERROR: Capture: {e}")
      self.log("webserver route request: /latest...")
      base = os.path.abspath(os.path.dirname('.'))
      response = static_file('capture.jpg', root=base)
      response.set_header("Cache-Control", "public, max-age=0") # prevent any caching
      return response
    

    @self.bottle.route('/')
    def page_landing():
      self.log('route: /')
      return "<h1>Hullo MINIeye</h1>"

    @self.bottle.error(500)
    def error_handler_500(error):
      self.log(json.dumps({"status": "error", "message": str(error.exception)}))

    try:
      # self.server = WSGIRefServer(host=self.host, port=self.port)
      # HTTPServer.ssl_adapter = BuiltinSSLAdapter(
      #   certificate='config/cheroot.crt',
      #   private_key='cconfig/cheroot.key')
      self.server = WSGIServer( (self.host, int(self.port)), self.bottle)
      #self.server.ssl_adapter = BuiltinSSLAdapter("config/cheroot.pem", "config/cheroot.key") #if we want to use a Self signed cert to get https to get permission to use sensors
      self.server.safe_start()
    except Exception as e:
      self.log(f'could not instantiate WSGIRefServer...{e}')
    # self.server.set_logger(self.logger)

    self.bottle.run(host=self.host, port=self.port, debug=self.debug, server=self.server)

  def setup(self):
    self.log('setup: start_server()')
    time.sleep(1) # cannot start up bottle immediately, needs some wifi setup time
    self.start_server()
    data = {}

  def read(self):
    # in this case when we want to read changes in state of the interface
    #  feels like we may be shoehoming here, i.e. polling versus async/event driven
    return self.data

  def update_status(self, status):
    """
    This is called by main to inject overal Auroreye status object for use in the webserver interface display
    """
    self.status = status

  def start(self):
    self.log("start webserver for access point")
    self.queue = queue.Queue(maxsize=1)
    self.thread = threading.Thread(target=self.setup)
    self.thread.daemon = False
    self.thread.start()
    
  def stop(self):
    self.log("webserver for access point shutting down...")
    # self.server.stop()

if __name__ == "__main__":
  webserver = Webserver()
  webserver.start()
