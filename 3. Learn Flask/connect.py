import psycopg2

# Connect to the PostgreSQL database
mydb = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='010202',
    dbname='market'  # Specify the database name
)

# Create a cursor object
my_cursor = mydb.cursor()

# SQL command to insert data
sql_command = "INSERT INTO Item (name, price, barcode, description) VALUES (%s, %s, %s, %s)"
values = ("IPhone15", 500, "878224756", "with A99 Bionic Chipset")

# Execute the SQL command
my_cursor.execute(sql_command, values)

# Commit the transaction
mydb.commit()

# Close the cursor and connection
my_cursor.close()
mydb.close()
