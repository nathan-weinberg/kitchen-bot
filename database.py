# psycopg2 connection (conn) must be passed to all funcs for functionality

def getAll(conn):
	''' returns List of names of all boys
	'''
	cur = conn.cursor()
	cur.execute("SELECT name FROM kitchen_boy;")
	raw_boys = cur.fetchall()
	boys = [boy[0] for boy in raw_boys]
	cur.close()
	return boys

def getBoy(conn):
	''' returns String of name of current kitchen boy
	'''
	cur = conn.cursor()
	cur.execute("SELECT name FROM kitchen_boy WHERE isBoy;")
	boy = cur.fetchone()[0]
	cur.close()
	return boy

def getBoyNum(conn):
	''' returns Int of day number for current kitchen boy
	'''
	cur = conn.cursor()
	cur.execute("SELECT dayNum FROM kitchen_boy WHERE isBoy;")
	num = cur.fetchone()[0]
	cur.close()
	return num

def getSchedule(conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM kitchen_boy ORDER BY name;")
	schedule = cur.fetchall()
	cur.close()
	return schedule

def getNextBoy(conn):
	''' returns String of name of next boy
	'''
	cur = conn.cursor()
	cur.execute("SELECT nextboy FROM kitchen_boy WHERE isBoy;")
	nextBoy = cur.fetchone()[0]
	cur.close()
	return nextBoy

def getNickname(conn, user):
	''' returns String of nickname of nickname of user
	'''
	cur = conn.cursor()
	cur.execute("SELECT nickname FROM nicknames WHERE name LIKE (%s);",(user,))
	nickname = cur.fetchone()[0]
	cur.close()
	return nickname

def getUserID(conn, user):
	''' gets String of GroupMe ID of user
	'''
	cur = conn.cursor()
	cur.execute("SELECT id FROM user_ids WHERE name LIKE (%s);",(user,))
	user_id = cur.fetchone()[0]
	cur.close()
	return user_id

def changeDay(conn, user):
	''' changes dayNum attribute to 2 for given user
	'''
	cur = conn.cursor()

	# changes dayNum variable of currentBoy in kitchen_boy table to num
	cur.execute("UPDATE kitchen_boy SET dayNum = 2 WHERE name LIKE (%s);",(user,))

	# commit changes
	conn.commit()
	cur.close()

def updateBoy(conn, prevBoy, nextBoy):
	''' passes responsiblity of kitchen boy
	'''	
	cur = conn.cursor()

	# erase responsibility from previous boy
	cur.execute("UPDATE kitchen_boy SET isBoy = false WHERE name LIKE (%s);",(prevBoy,))
	# reset day number of previous boy
	cur.execute("UPDATE kitchen_boy SET dayNum = 1 WHERE name LIKE (%s);",(prevBoy,))
	# assign responsibility to next boy
	cur.execute("UPDATE kitchen_boy SET isBoy = true WHERE name LIKE (%s);",(nextBoy,))
	
	# commit changes
	conn.commit()
	cur.close()
