class DatabasePool:
	pool = []

	def __init__(self, session_manager, count):
		
		for i in range(0, count):
			self.pool.append(session_manager())

	def get_connection(self):
		connection = self.pool[0]
		del self.pool[0]

	def return_connection(self, connection):
		self.pool.append(connection)


pool = DatabasePool()