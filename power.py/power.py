import json
import requests
import mysql.connector
#pip install mysql-connector-python
from datetime import datetime, date, timedelta

# MySQL connection configuration
mysql_config = {
    "user": "<username>",
    "password": "<password>",
    "host": "<ip addr>",
    "database": "<some db>"
}

# Function to create the tables if they don't exist
def create_tables():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # Check if counts table exists
        cursor.execute("SHOW TABLES LIKE 'counts'")
        result = cursor.fetchone()

        if not result:
            # Create counts table
            cursor.execute("""
                CREATE TABLE counts (
                    id INT PRIMARY KEY,
                    current_count FLOAT
                )
            """)

        # Check if daily_counts table exists
        cursor.execute("SHOW TABLES LIKE 'daily_counts'")
        result = cursor.fetchone()

        if not result:
            # Create daily_counts table
            cursor.execute("""
                CREATE TABLE daily_counts (
                    date DATE PRIMARY KEY,
                    count FLOAT
                )
            """)

        # Check if monthly_counts table exists
        cursor.execute("SHOW TABLES LIKE 'monthly_counts'")
        result = cursor.fetchone()

        if not result:
            # Create monthly_counts table
            cursor.execute("""
                CREATE TABLE monthly_counts (
                    month INT,
                    year INT,
                    count FLOAT,
                    PRIMARY KEY (month, year)
                )
            """)

        # Commit changes
        connection.commit()

    except mysql.connector.Error as error:
        print("Error creating tables:", error)

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to insert or update current count in MySQL
def update_current_count(count):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # Create tables if they don't exist
        create_tables()

        # Check if current count exists in the table
        cursor.execute("SELECT * FROM counts WHERE id = 1")
        result = cursor.fetchone()

        if result:
            # Update current count
            cursor.execute("UPDATE counts SET current_count = %s WHERE id = 1", (count,))
        else:
            # Insert current count
            cursor.execute("INSERT INTO counts (id, current_count) VALUES (1, %s)", (count,))

        # Commit changes
        connection.commit()

    except mysql.connector.Error as error:
        print("Error updating current count:", error)

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to update daily count in MySQL
def update_daily_count(count):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # Create tables if they don't exist
        create_tables()

        # Get today's date
        today = date.today()

        # Check if a record for today exists in the table
        cursor.execute("SELECT * FROM daily_counts WHERE date = %s", (today,))
        result = cursor.fetchone()

        if result:
            # Update daily count
            cursor.execute("UPDATE daily_counts SET count = count + %s WHERE date = %s", (count, today))
        else:
            # Insert daily count
            cursor.execute("INSERT INTO daily_counts (date, count) VALUES (%s, %s)", (today, count))

        # Check if the current date is different from the stored date in the table
        # If it's a new day, reset the count to the current value
        cursor.execute("SELECT date FROM daily_counts ORDER BY date DESC LIMIT 1")
        last_date = cursor.fetchone()

        if last_date and last_date[0] < today:
            #cursor.execute("UPDATE daily_counts SET count = %s WHERE date = %s", (count, today))
            cursor.execute("INSERT INTO daily_counts (date, count) VALUES (%s, %s)", (today, count))

        # Commit changes
        connection.commit()

    except mysql.connector.Error as error:
        print("Error updating daily count:", error)

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to update monthly count in MySQL
def update_monthly_count(count):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # Create tables if they don't exist
        create_tables()

        # Get the current month and year
        today = date.today()
        month = today.month
        year = today.year

        # Check if a record for the current month exists in the table
        cursor.execute("SELECT * FROM monthly_counts WHERE month = %s AND year = %s", (month, year))
        result = cursor.fetchone()

        if result:
            # Update monthly count
            cursor.execute("UPDATE monthly_counts SET count = count + %s WHERE month = %s AND year = %s", (count, month, year))
        else:
            # Insert monthly count
            cursor.execute("INSERT INTO monthly_counts (month, year, count) VALUES (%s, %s, %s)", (month, year, count))

        # Check if the current month is different from the stored month in the table
        # If it's a new month, reset the count to the current value
        cursor.execute("SELECT month, year FROM monthly_counts ORDER BY year DESC, month DESC LIMIT 1")
        last_month = cursor.fetchone()

        if last_month and (last_month[0], last_month[1]) < (month, year):
            cursor.execute("INSERT INTO monthly_counts (month, year, count) VALUES (%s, %s, %s)", (month, year, count))



        # Commit changes
        connection.commit()

    except mysql.connector.Error as error:
        print("Error updating monthly count:", error)

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()


# Call the API and update counts
def update_counts():
    try:
        url = "http://192.168.1.126/json"
        response = requests.get(url)

        # Parse the JSON data
        data = response.json()

        # Access the "Count" value
        count = data["Sensors"][1]["TaskValues"][0]["Value"]

        kwh = count / 1000
        print(kwh)

        # Update current count
        update_current_count(kwh)

        # Update daily count if it's a new day
        update_daily_count(kwh)

        # Update monthly count if it's a new month
        update_monthly_count(kwh)

    except requests.RequestException as error:
        print("Error calling the API:", error)

# Run the program
update_counts()