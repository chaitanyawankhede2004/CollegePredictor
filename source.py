import mysql.connector
from mysql.connector import Error
import csv
import os

def setup_database():
    con = None
    try:
        # Check CSV file
        if not os.path.exists("CollegeData.csv"):
            print("❌ CSV file not found! Make sure 'CollegeData.csv' is in the same folder.")
            return

        # Connect to MySQL (no DB selected yet)
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            auth_plugin="mysql_native_password"
        )
        cur = con.cursor()

        # Create and select database
        cur.execute("CREATE DATABASE IF NOT EXISTS ChintuProject")
        cur.execute("USE ChintuProject")
        print("✅ Database 'ChintuProject' ready.")

        # Create colleges table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS colleges (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                institute_name  VARCHAR(255),
                course          VARCHAR(255),
                opening_rank    INT,
                closing_rank    INT
            )
        """)

        # Create students table  (fixed: IF NOT EXISTS, correct column names)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                enr       INT PRIMARY KEY,
                name      VARCHAR(255),
                password  VARCHAR(255),
                stdrank   INT
            )
        """)
        print("✅ Tables created (colleges + students).")

        # Clear old college data before re-importing
        cur.execute("DELETE FROM colleges")

        # Read CSV  — NOTE: header in your file is "Cource" (typo), match it exactly
        with open("CollegeData.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            # Strip whitespace from header names
            csv_reader.fieldnames = [h.strip() for h in csv_reader.fieldnames]
            print("📋 CSV Headers detected:", csv_reader.fieldnames)

            data = []
            skipped = 0
            for row in csv_reader:
                try:
                    # Strip whitespace from every value
                    row = {k.strip(): v.strip() for k, v in row.items()}
                    data.append((
                        row["Name of institute"],
                        row["Cource"],          # matches your CSV typo exactly
                        int(row["Opening Rank"]),
                        int(row["Closing Rank"])
                    ))
                except Exception as e:
                    skipped += 1
                    print(f"  ⚠️  Skipping row: {row} | Reason: {e}")

        # Bulk insert
        query = """
            INSERT INTO colleges (institute_name, course, opening_rank, closing_rank)
            VALUES (%s, %s, %s, %s)
        """
        cur.executemany(query, data)
        con.commit()

        print(f"\n✅ {len(data)} records inserted successfully!")
        if skipped:
            print(f"⚠️  {skipped} rows were skipped due to errors.")

    except Error as e:
        print(f"❌ Database Error: {e}")
    finally:
        if con and con.is_connected():
            con.close()
            print("🔒 Connection closed.")

if __name__ == "__main__":
    setup_database()
