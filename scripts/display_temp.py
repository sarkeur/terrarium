#!/usr/bin/env python
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import os

wss =[]
class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print 'New user is connected.\n' 
    if self not in wss:
      wss.append(self)
  def on_close(self):
    print 'connection closed\n'
    if self in wss:
      wss.remove(self)

application = tornado.web.Application([(r'/ws', WSHandler),])

if __name__ == "__main__":
  os.system('modprobe w1-gpio')
  os.system('modprobe w1-therm')
  interval_msec = 2000

  def wsSend(message):
    for ws in wss:
      if not ws.ws_connection.stream.socket:
        print "Web socket does not exist anymore!!!"
        wss.remove(ws)
      else:
        ws.write_message(message)

  def read_temp():
    try:
      #replace xxxxxxxxxxxx with code of your DS18B20
      file = open('/sys/bus/w1/devices/28-0115921b25ff/w1_slave', 'r')
      lines = file.readlines()
      if lines[0].find("YES"):
        pok = lines[1].find('=')
        temp = str(float(lines[1][pok+1:pok+6])/1000)
      file.close()

      #read temp. onboard sensor    
      file = open('/sys/bus/w1/devices/28-0115921c81ff/w1_slave','r')
      lines = file.readlines()
      if lines[0].find("YES"):
        pok = lines[1].find('=')
        temp = str(float(lines[1][pok+1:pok+6])/1000)
      file.close()
      wsSend(temp)
    except:
      wsSend("-;-")

  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
    
  main_loop = tornado.ioloop.IOLoop.instance()
  sched_temp = tornado.ioloop.PeriodicCallback(read_temp, interval_msec,   io_loop = main_loop)

  sched_temp.start()
  main_loop.start()
