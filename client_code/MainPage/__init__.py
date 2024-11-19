from ._anvil_designer import MainPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

# Favorite Preiskat im dropdown selected

class MainPage(MainPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.hostel_id_index_relation = [] # [INDEX/ID] 
    self.user_id_index_relation = []
    self.price_id_index_relation = []
    self.room_id_index_relation = []
    self.extra_user_index = []
    self.init_components(**properties)
    self.loading_data()


  # PROBLEM 
  # DATUM IN DER DB
  # DOPPELBUCHUNG !!!! am GLEICHEN TAG
  


  # Loading
  def data_modify(self, data):
    data_list = []
    relation = []
    count = 0
    for i in data:
      data_list.append([i[0],count]) # i[0] the Name  COUNT is the index in the dropdown
      relation.append([count, i[1]]) # i [1] the ID  COUNT is the index in the dropdown
      count +=1
    return [data_list, relation]

  def transform_index_to_id(self, data, index):
    for i in data:
      if index == i[0]:
        return i[1]
 
  def loading_data(self):
    self.load_hostel()
    self.load_user(self.user_dropdown)
    self.load_user(self.extra_user_dropdown)
    self.load_price()
    self.load_room()
    self.display_booking()

  def load_hostel(self):
    data_list = anvil.server.call('get_hostel')
    data_modify = self.data_modify(data_list)
    self.hostel_id_index_relation = data_modify[1]
    self.hostel_dropdown.items = data_modify[0]

  def load_user(self, dropdown):
    data_list = anvil.server.call('get_user')
    data_modify = self.data_modify(data_list)
    self.user_id_index_relation = data_modify[1]
    dropdown.items = data_modify[0]

  def load_price(self):
    data_list = anvil.server.call('get_price')
    data_modify = self.data_modify(data_list)
    self.price_id_index_relation = data_modify[1]
    self.price_dropdown.items = data_modify[0]

  def load_room(self):
    hostel_selected = self.transform_index_to_id(self.hostel_id_index_relation, self.hostel_dropdown.selected_value)
    price_selected = self.transform_index_to_id(self.price_id_index_relation, self.price_dropdown.selected_value)
    data_list = anvil.server.call('get_room', hostel_selected, price_selected)
    data_modify = self.data_modify(data_list)
    self.room_id_index_relation = data_modify[1]
    self.room_dropdown.items = data_modify[0]  
  
  def hostel_dropdown_change(self, **event_args):
    self.load_room()

  def price_dropdown_change(self, **event_args):
    self.load_room()

  def add_user_click(self, **event_args):
    value = self.extra_user_dropdown.selected_value
    for text, i in self.extra_user_dropdown.items:
      if i == value:
          print(text) 
          name = Link( text=str(text))
          name.icon="fa:times"
          name.icon_align="left"
          name.background="#eee"
          name.role="lozenge"
          name.border="1px solid #888"
        
          name.set_event_handler("click", lambda **k: self.del_btn(k, value))
        
          if text not in [component.text for component in self.user_to_add.get_components()]:
              self.extra_user_index.append(value)
              self.user_to_add.add_component(name)  # Add the Link component if it's not already added
          else:
              print(f"{text} is already added.")  # Optionally, notify that the item is already added
          break 

  def del_btn(self, k, value):
    print("clicked by:", k['sender'].text)
    k['sender'].remove_from_parent()  # Remove the link from the UI
    if value in self.extra_user_index:
        self.extra_user_index.remove(value)  # Remove the value from the list
        print(f"{value} removed from extra_user_index.")
    else:
        print(f"{value} not found in extra_user_index.")

  def booking_btn_click(self, **event_args):
    self.get_booking_data()
    self.display_booking()


  def get_booking_data(self):
    main_BeID = self.transform_index_to_id(self.user_id_index_relation, self.user_dropdown.selected_value)
    users = self.get_extra_user_id(main_BeID)
    if self.check_date(self.start_date.date, self.end_Date.date, "%Y-%m-%d" ):
      start_date = str(self.start_date.date)
      end_date = str(self.end_Date.date)
      zid = self.transform_index_to_id(self.room_id_index_relation, self.room_dropdown.selected_value)
      print(zid)
      print(users)
      anvil.server.call('booking',users,start_date,end_date,zid)
      self.booking_comback.text = "Buchung ist erfolgreich."
    else:
      self.booking_comback.text = "Datum ist nicht möglich"
      


  def check_date(self,start_date, end_date, date_format):
    # Define the date format
   
    
    # Convert strings to datetime objects
    d1 = datetime.strptime(str(start_date), date_format)
    d2 = datetime.strptime(str(end_date), date_format)
    
    return d1 < d2
      
  
  def get_extra_user_id(self, main_ID):
    users_id = []
    for i in self.extra_user_index:
      users_id.append(self.transform_index_to_id(self.user_id_index_relation,i))
    if main_ID in users_id:
      pass
    else:
      users_id.append(main_ID)
      
    return users_id
    
  def display_booking(self):
    self.repeating_panel_1.items = None
    data = anvil.server.call('get_data')

    add_list = []
    for i in data:
      add_list.append({'column_1': i[0], 'column_2': i[1], 'column_3': i[2], 'column_4': i[3], 'column_5': i[4], 'column_6': i[5], })

    self.repeating_panel_1.items = add_list


    


