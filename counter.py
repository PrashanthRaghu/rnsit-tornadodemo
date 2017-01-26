import redisFactory

class counter:
	redisConnection = redisFactory.getRedisInstance()
	count = 0

	def __init__(self):
		itemId = self.redisConnection.get("counter")

		if itemId != None:
			self.count = int(itemId)
		else:
			self.redisConnection.set("counter", 0)
			self.count = 0

	def incrCounter(self):
		self.redisConnection.incr("counter")
		self.count += 1


list_counter = counter()