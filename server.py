#!/usr/bin/env python
import sqlite3
import json

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs

port_number = 80
conn = sqlite3.connect('./hdsa.db')
c = conn.cursor()

class S(BaseHTTPRequestHandler):

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    if self.path.startswith('/usage'):
      self._set_headers()
      global conn, c
      c.execute('SELECT * FROM usage ORDER BY time DESC LIMIT 10')
      rows = c.fetchall()
      self.wfile.write(json.dumps(rows))
      return
    elif self.path.startswith('/solar'):
      self._set_headers()
      global conn, c
      c.execute('SELECT * FROM solar ORDER BY time DESC LIMIT 10')
      rows = c.fetchall()
      self.wfile.write(json.dumps(rows))
      return
    elif self.path.startswith('/battery'):
      self._set_headers()
      global conn, c
      c.execute('SELECT * FROM battery ORDER BY time DESC LIMIT 10')
      rows = c.fetchall()
      self.wfile.write(json.dumps(rows))
      return
    elif self.path.startswith('/audio'):
      self.send_response(200)
      self.send_header('Content-type', 'audio/wav')
      self.end_headers()
      self.wfile.write(open("alarm_beep.wav", "r").read())
    else:
      self._set_headers()
      self.wfile.write(open("index.html", "r").read())

if __name__ == "__main__":
  try:
    server = HTTPServer(('', port_number), S)
    print('Started HTTP server on port', port_number)
    server.serve_forever()

  except KeyboardInterrupt:
    print('^C received, shutting down server')
    server.socket.close()
