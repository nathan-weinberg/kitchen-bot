import psycopg2

DATABASE_URL = 'YOUR DATABASE URL'
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# Create nicknames table
cur.execute('''
	CREATE TABLE nicknames (
		name varchar PRIMARY KEY,
		nickname varchar UNIQUE NOT NULL
	);
''')

# Populate nicknames table
cur.execute('''
	INSERT INTO nicknames (name, nickname) VALUES
		('EXAMPLE1', 'Example 1'),
		('EXAMPLE2', 'Example 2'),
		('EXAMPLE3', 'Example 3')
''')

# Create user_ids table
cur.execute('''
	CREATE TABLE user_ids (
		name varchar REFERENCES nicknames(name),
		id int UNIQUE NOT NULL
	);
''')

# Populate user_ids table
cur.execute('''
	INSERT INTO user_ids (name, id) VALUES
		('EXAMPLE1', 1),
		('EXAMPLE2', 2),
		('EXAMPLE3', 3)
	;
''')

# Create kitchen_boy table
cur.execute('''
	CREATE TABLE kitchen_boy (
		name varchar REFERENCES nicknames(name),
		isBoy boolean NOT NULL,
		nextBoy varchar REFERENCES nicknames(name),
		dayNum int NOT NULL
	);
''')

# Populate kitchen_boy table
cur.execute('''
	INSERT INTO kitchen_boy (name, isBoy, nextBoy, dayNum) VALUES
		('EXAMPLE1', true, 'EXAMPLE2', 1),
		('EXAMPLE2', false, 'EXAMPLE3', 1),
		('EXAMPLE3', false, 'EXAMPLE1', 1)
	;	
''')

# Create meta table
cur.execute('''
	CREATE TABLE meta (
		status varchar NOT NULL
	);
''')

# Populate meta table
cur.execute('''
	INSERT INTO meta (status) VALUES
		('ENABLED')
	;
''')

conn.commit()
conn.close()
print("Database Filled")
