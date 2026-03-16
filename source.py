import mysql.connector
from mysql.connector import Error
import csv

def setup_database():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            auth_plugin="mysql_native_password"
        )

        cur = con.cursor()

        # Create database
        cur.execute("CREATE DATABASE IF NOT EXISTS ChintuProject")
        cur.execute("USE ChintuProject")

        # Create table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS colleges (
                id INT AUTO_INCREMENT PRIMARY KEY,
                institute_name VARCHAR(255),
                course VARCHAR(255),
                opening_rank INT,
                closing_rank INT
            )
        """)

        # Read CSV file
        with open("CollegeData.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            data = []
            for row in csv_reader:
                data.append((
                    row["Name of institute"],
                    row["Cource"],
                    int(row["Opening Rank"]),
                    int(row["Closing Rank"])
                ))

        # Insert data
        query = """
            INSERT INTO colleges (institute_name, course, opening_rank, closing_rank)
            VALUES (%s, %s, %s, %s)
        """

        cur.executemany(query, data)

        con.commit()
        print("CSV Data Imported Successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        if con.is_connected():
            con.close()

if __name__ == "__main__":
    setup_database()
