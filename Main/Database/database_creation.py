import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@0833"
    )

# Define the database name
db_name = 'chatbot_db'

# Connect to MySQL
conn = connect_to_database()
cursor = conn.cursor()

# Create the database
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
cursor.execute(f"USE {db_name}")

# Create the 'businesses' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS businesses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255),
    description TEXT
)
''')

# Create the 'faqs' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS faqs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    business_id INT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
)
''')

# Create the 'interactions' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    business_id INT,
    query TEXT,
    response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
)
''')

# Create the 'learning_data' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS learning_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    business_id INT,
    query TEXT,
    answer TEXT,
    feedback TEXT,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
)
''')

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Database and tables created successfully.")
