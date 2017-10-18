from ClusterInterface import ClusterInterface
#from DetectionManager import DetectionManager
from Node import Node
from Instance import  Instance
import uuid
import logging
import ConfigParser

class Cluster(ClusterInterface):
	def __init__(self, id , name):
		super(Cluster, self).__init__(id, name)

	def addNode(self, node_name_list):
		# create node list
		try:
			#message=""
			#result=None
			for node_name in node_name_list:
				if  not self._nodeIsIllegal(node_name) :
					#id = str(uuid.uuid4())
					#ipmi_status = self._getIPMIStatus(node_name)
					node = Node(name = node_name , cluster_id = self.id)
					self.node_list.append(node)
					#node.startDetection()
					message = "The node %s is added to cluster." % self.getAllNodeStr()
					result = {"code": "0", "clusterId": self.id, "message": message}
			logging.info(message)
			return result

		except:
			message = "Cluster add node fail , some node maybe overlapping or not in compute pool please check again! The node list is %s." % (self.getAllNodeStr())
			logging.error(message)
			result = {"code": "1", "clusterId": self.id, "message": message}
			return result

	def deleteNode(self , node_name):
		node = self.getNodeByName(node_name)
		if not node:
			raise Exception("Delete node -- Not found the node %s" % node_name)
		#node.deleteDetectionThread()
		self.node_list.remove(node)

	def getAllNodeInfo(self):
		ret = []
		for node in self.node_list:
			ret.append(node.getInfo())
		return ret

	def addInstance(self , instance_id):
		self.host = None
		if self.isProtected(instance_id): # check instance is already being protected
			raise Exception("this instance is already being protected!")
		elif not self.checkInstancePowerOn(instance_id):
			raise Exception("this instance is power off!")
		else:
			#Live migration VM to cluster node
			self.host = self.nova_client.getInstanceHost(instance_id)
			instance = Instance(id=instance_id,name=self.nova_client.getInstanceNameById(instance_id),host=self.host)
			self.instance_list.append(instance)
			print self.instance_list

	def deleteInstance(self , instance_id):
		if not self.isProtected(instance_id):
			raise Exception("this instance is not being protected")
		for instance in self.instance_list:
			if instance.id == instance_id:
				self.instance_list.remove(instance)
				#break
		return True

	#cluster.addInstance
	def findNodeByInstance(self, instance_id):
		for node in self.node_list:
			if node.containsInstance(instance_id):
				return node
		return None

	'''
	def _isNodeDuplicate(self , unchecked_node_name):
		for node in self.node_list:
			if node.name == unchecked_node_name:
				return True
		return False
		
	#addNode call
	def _getIPMIStatus(self, node_name):
		config = ConfigParser.RawConfigParser()
		config.read('hass.conf')
		ip_dict = dict(config._sections['ipmi'])
		return node_name in ip_dict
		
	'''

	def _isInComputePool(self, unchecked_node_name):
		return unchecked_node_name in self.nova_client.getComputePool()

	def _nodeIsIllegal(self , unchecked_node_name):
		if not self._isInComputePool(unchecked_node_name):
			return True
		#if self._isNodeDuplicate(unchecked_node_name):
			#return True
		return False

	#be DB called
	def getNodeList(self):
		return self.node_list

	#be deleteNode called
	def getNodeByName(self, name):
		#node_list = self.getNodeList()
		for node in self.node_list:
			if node.name == name:
				return node
		return None

	#addNode message
	def getAllNodeStr(self):
		ret = ""
		for node in self.node_list:
			ret += node.name
		return ret

	#clustermanager.deletecluster call
	def deleteAllNode(self):
		for node in self.node_list:
			self.deleteNode(node.id)
		if self.node_list ==[]:
			return True
	'''
	def getProtectedInstanceList(self):
		return self.instance_list
	'''

	#list Instance
	def getAllInstanceInfo(self):
		ret = []
		#instance_list = self.getProtectedInstanceList()
		for instance in self.instance_list:
			ret.append(instance.getInfo())
		return ret

	def checkInstanceGetVolume(self,instance_id):
		if not self.nova_client.isInstanceGetVolume(instance_id):
			message = "this instance not having volume! Instance id is %s " %instance_id
			logging.error("this instance not having volume! Instance id is %s " %instance_id)
			return False
		return True

	def checkInstancePowerOn(self,instance_id):
		if not self.nova_client.isInstancePowerOn(instance_id):
			message = "this instance is not running! Instance id is %s " % instance_id
			logging.error("this instance not having volume! Instance id is %s " % instance_id)
			return False
		return True

	#clusterManager.
	def checkInstanceExist(self, instance_id):
		#node_list = self.getNodeList()
		print "node list of cluster:",self.node_list
		for node in self.node_list:
			if node.containsInstance(instance_id):
				return True
		message = "this instance not exist. Instance id is %s. " % instance_id
		logging.error(message)
		return False

	def isProtected(self, instance_id):
		for instance in self.instance_list:
			if instance.id == instance_id:
				return True
		return False

