import dbFactory

class DatabasePool:
	pool = []

	def __init__(self, session_manager, count):
		
		for i in range(0, count):
			self.pool.append(session_manager())

	def get_connection(self):
		connection = self.pool[0]
		self.pool = self.pool[1:-1]
		return connection

	def return_connection(self, connection):
		self.pool.append(connection)

session = dbFactory.initDbSession()
pool = DatabasePool(session, 10)