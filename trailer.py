import urllib2
import sys
import time
import sqlite3
import subprocess

from datetime import datetime
from vebus_client import *
from client_functions import *
from pymodbus.client.sync import ModbusTcpClient

modbus_client = ModbusTcpClient(sys.argv[1])
hub = VebusClient(modbus_client)
conn = sqlite3.connect('./hdsa.db')

def toggle_lamp(onoff):
  if onoff:
    urllib2.urlopen("http://diysmartlamp.local/on").read()
  else:
    urllib2.urlopen("http://diysmartlamp.local/off").read()

def store_usage(date, v):
  query = 'INSERT INTO usage VALUES (\"' + date + '\",' + str(v[0]) + ',' + str(v[1]) + ',' + str(v[2]) + ');'
  global conn
  c = conn.cursor()
  c.execute(query)
  conn.commit()

def store_solar(date, v):
  query = 'INSERT INTO solar VALUES (\"' + date + '\",' + str(v)  + ');'
  global conn
  c = conn.cursor()
  c.execute(query)
  conn.commit()

def store_battery(date, v):
  query = 'INSERT INTO battery VALUES (\"' + date + '\",' + str(v)  + ');'
  global conn
  c = conn.cursor()
  c.execute(query)
  conn.commit()

while True:
  vals = hub.get_output_power()
  print("Usage: " + str(vals[1]))
  store_usage(str(datetime.now()), vals)
  cmd_str = "ssh root@" + sys.argv[1] + " 'dbus -y com.victronenergy.system /Dc/Pv/Power GetValue'"
  val = float(subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE).stdout.read())
  print("Solar: " + str(val))
  store_solar(str(datetime.now()), val)
  toggle_lamp(val > 1000)

  val = hub.get_soc()
  print("Battery: " + str(val))
  store_battery(str(datetime.now()), val)

  time.sleep(10)

