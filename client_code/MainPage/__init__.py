from ._anvil_designer import MainPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class MainPage(MainPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.hostel_id_index_relation = [] # [INDEX/ID] 
    self.user_id_index_relation = []
    self.price_id_index_relation = []
    self.room_id_index_relation = []
    
    self.init_components(**properties)
    self.loading_data()
    # Any code you write here will run before the form opens.


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
    data_list = anvil.server.call('get_room',hostel_selected, price_selected)
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
          name.set_event_handler("click",self.del_btn)
          if text not in [component.text for component in self.user_to_add.get_components()]:
              self.user_to_add.add_component(name)  # Add the Link component if it's not already added
          else:
              print(f"{text} is already added.")  # Optionally, notify that the item is already added
          break 

  def del_btn(self,**k):
    print("clicked by :",k['sender'].text)
    k['sender'].remove_from_parent()




    


