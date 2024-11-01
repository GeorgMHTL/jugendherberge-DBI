import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3 

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#


@anvil.server.callable
def get_hostel():
  con = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
  cursor = con.cursor()
  data = list(cursor.execute("SELECT name, JID FROM jugendherbergen"))
  con.commit()
  con.close()
  return data

@anvil.server.callable
def get_user():
  con = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
  cursor = con.cursor()
  data = list(cursor.execute("SELECT vorname, BeID FROM benutzer;"))
  con.commit()
  con.close()
  return data

@anvil.server.callable 
def get_price():
  con = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
  cursor = con.cursor()
  data = list(cursor.execute("SELECT name || ' ' || preis || '€' AS NamePreis, PID FROM preiskategorie;"))
  con.commit()
  con.close()
  return data
  
@anvil.server.callable
def get_room(hostel_id, price_id):
  con = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
  cursor = con.cursor()
  data = list(cursor.execute(f"SELECT 'NR:' || ZID || ' BETTEN: ' ||bettenZahl AS NummerBettZahl, ZID FROM zimmer WHERE JID={hostel_id} AND PID = {price_id};"))
  con.commit()
  con.close()
  return data
