from NovaClient import NovaClient
from DatabaseManager import DatabaseManager


class ClusterInterface(object):
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.node_list = []
		self.protected_instance_list = []
		self.nova_client = NovaClient.getInstance()
		self.db = DatabaseManager()