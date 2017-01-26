import redis

def getRedisInstance():
	redisConnection = redis.StrictRedis(host='localhost', port=6379, db=0)	
	return redisConnection

