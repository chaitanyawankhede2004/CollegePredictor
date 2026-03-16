import mysql.connector as myc
from mysql.connector import Error

def get_connection():
    try:
        return myc.connect(
            host="localhost",
            user="root",
            password="password",
            database='ChintuProject',
            auth_plugin='mysql_native_password'
        )
    except Error as e:
        print(f"Connection Error: {e}")
        return None


def register_student():
    con = get_connection()
    cur = con.cursor()

    print("\n--- Student Registration ---")
    enr = int(input("Enrollment No: "))
    name = input("Name: ")
    password = input("Password: ")
    rank = int(input("JEE Rank: "))

    cur.execute(
        "INSERT INTO students VALUES(%s,%s,%s,%s)",
        (enr,name,password,rank)
    )

    con.commit()
    print("Registration Successful!")

    cur.close()
    con.close()


# ---------------- LOGIN ----------------

def login_student():
    con = get_connection()
    cur = con.cursor()

    enr = int(input("Enrollment No: "))
    password = input("Password: ")

    cur.execute(
        "SELECT name,rank FROM students WHERE enr_no=%s AND password=%s",
        (enr,password)
    )

    student = cur.fetchone()

    cur.close()
    con.close()

    if student:
        print(f"\nWelcome {student[0]}")
        student_menu(student[1])
    else:
        print("Invalid Login")


# ---------------- PREDICTOR ----------------

def predict_college(rank):
    con = get_connection()
    cur = con.cursor()

    query = """
    SELECT institute_name,course,opening_rank,closing_rank
    FROM colleges
    WHERE %s BETWEEN opening_rank AND closing_rank
    ORDER BY closing_rank
    LIMIT 10
    """

    cur.execute(query,(rank,))
    results = cur.fetchall()

    print("\nPossible Colleges:\n")

    for r in results:
        print(f"College : {r[0]}")
        print(f"Branch  : {r[1]}")
        print(f"Rank Range : {r[2]} - {r[3]}")
        print("-"*50)

    cur.close()
    con.close()


# ---------------- BRANCH LIST ----------------

def show_branches():
    con = get_connection()
    cur = con.cursor()

    cur.execute("SELECT DISTINCT course FROM colleges")

    print("\nAvailable Branches:\n")

    for r in cur:
        print(r[0])

    cur.close()
    con.close()


# ---------------- MERIT LIST ----------------

def merit_list():
    con = get_connection()
    cur = con.cursor()

    branch = input("Enter Branch Name: ")

    query = """
    SELECT s.name,s.rank,c.institute_name
    FROM students s
    JOIN colleges c
    ON s.rank BETWEEN c.opening_rank AND c.closing_rank
    WHERE c.course=%s
    ORDER BY s.rank
    """

    cur.execute(query,(branch,))
    results = cur.fetchall()

    print("\nMerit List\n")

    for r in results:
        print(f"Name : {r[0]}  Rank : {r[1]}  College : {r[2]}")

    cur.close()
    con.close()


# ---------------- STUDENT MENU ----------------

def student_menu(rank):

    while True:
        print("\n1 Predict College")
        print("2 Show Branches")
        print("3 Merit List")
        print("4 Logout")

        ch = input("Choice: ")

        if ch=="1":
            predict_college(rank)

        elif ch=="2":
            show_branches()

        elif ch=="3":
            merit_list()

        elif ch=="4":
            break


# ---------------- MAIN MENU ----------------

def menu():

    while True:

        print("\nENGINEERING ADMISSION PORTAL")
        print("1 Register")
        print("2 Login")
        print("3 Exit")

        ch=input("Choice: ")

        if ch=="1":
            register_student()

        elif ch=="2":
            login_student()

        elif ch=="3":
            break


menu()
