from flask_table import Table, Col

class ItemTable(Table):
	name = Col('ucReport')
	description = Col('Requirements for each campus.')
	
class Item(object):
	def __init__(self, name, description):
		self.name = name
		self.description = description
	
items = [Item('Name 1', 'description 1'),
		 Item('Name 2', 'description 2'),
		 Item('Name 3', 'description 3')]
		 
table = ItemTable(items)