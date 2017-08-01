import sys
import time
import sqlite3

from datetime import datetime
from vebus_client import *
from client_functions import *
from pymodbus.client.sync import ModbusTcpClient

modbus_client = ModbusTcpClient(sys.argv[1])
hub = VebusClient(modbus_client)
conn = sqlite3.connect('./hdsa.db')

def store(date, v):
  query = 'INSERT INTO usage VALUES (\"' + date + '\",' + str(v[0]) + ',' + str(v[1]) + ',' + str(v[2]) + ');'
  global conn
  c = conn.cursor()
  c.execute(query)
  conn.commit()

while True:
  vals = hub.get_output_power()
  print(vals)
  store(str(datetime.now()), vals)
  time.sleep(1)

#val = hub.get_battery_voltage()
#print(val)


