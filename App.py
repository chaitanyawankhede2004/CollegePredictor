import mysql.connector as myc
from mysql.connector import Error

# ─────────────────────────────────────────
#  DB CONNECTION
# ─────────────────────────────────────────
def get_connection():
    try:
        return myc.connect(
            host="localhost",
            user="root",
            password="password",
            database="ChintuProject",
            auth_plugin="mysql_native_password"
        )
    except Error as e:
        print(f"❌ Connection Error: {e}")
        return None

# ─────────────────────────────────────────
#  REGISTER
# ─────────────────────────────────────────
def register_student():
    con = get_connection()
    if not con:
        return
    cur = con.cursor()
    print("\n" + "="*50)
    print("        STUDENT REGISTRATION")
    print("="*50)
    try:
        enr      = int(input("  Enrollment No : "))
        name     = input("  Full Name      : ").strip()
        password = input("  Password       : ").strip()
        rank     = int(input("  JEE Rank       : "))

        # Check duplicate enrollment
        cur.execute("SELECT enr FROM students WHERE enr=%s", (enr,))
        if cur.fetchone():
            print("⚠️  Enrollment number already registered!")
            return

        cur.execute(
            "INSERT INTO students (enr, name, password, stdrank) VALUES (%s,%s,%s,%s)",
            (enr, name, password, rank)
        )
        con.commit()
        print(f"\n  ✅ Registration successful! Welcome, {name}.")
    except ValueError:
        print("❌ Invalid input. Enrollment No and Rank must be numbers.")
    except Error as e:
        print(f"❌ DB Error: {e}")
    finally:
        cur.close()
        con.close()

# ─────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────
def login_student():
    con = get_connection()
    if not con:
        return
    cur = con.cursor()
    print("\n" + "="*50)
    print("             STUDENT LOGIN")
    print("="*50)
    try:
        enr      = int(input("  Enrollment No : "))
        password = input("  Password       : ").strip()

        # Fixed: column names are enr, password, name, stdrank
        cur.execute(
            "SELECT name, stdrank FROM students WHERE enr=%s AND password=%s",
            (enr, password)
        )
        student = cur.fetchone()
    except ValueError:
        print("❌ Enrollment No must be a number.")
        return
    finally:
        cur.close()
        con.close()

    if student:
        name, rank = student
        print(f"\n  ✅ Login successful! Welcome, {name}  (JEE Rank: {rank})")
        student_menu(name, rank)
    else:
        print("  ❌ Invalid enrollment number or password.")

# ─────────────────────────────────────────
#  COLLEGE PREDICTOR
# ─────────────────────────────────────────
def predict_college(rank):
    con = get_connection()
    if not con:
        return
    cur = con.cursor()
    print("\n" + "="*60)
    print(f"   🎓 COLLEGE PREDICTOR  —  Your JEE Rank: {rank}")
    print("="*60)

    # Show colleges where the student's rank falls within range
    query = """
        SELECT institute_name, course, opening_rank, closing_rank
        FROM colleges
        WHERE %s BETWEEN opening_rank AND closing_rank
        ORDER BY closing_rank
        LIMIT 15
    """
    cur.execute(query, (rank,))
    results = cur.fetchall()
    cur.close()
    con.close()

    if not results:
        print("  ⚠️  No colleges found for your rank range.")
        print("  Tip: Your rank may be outside the available data range.")
        return

    print(f"  Found {len(results)} possible college(s):\n")
    for i, r in enumerate(results, 1):
        print(f"  [{i:02}] 🏫 {r[0]}")
        print(f"       📚 Branch     : {r[1]}")
        print(f"       📊 Rank Range : {r[2]} — {r[3]}")
        print("       " + "-"*50)

# ─────────────────────────────────────────
#  BRANCH-WISE PREDICTOR (bonus)
# ─────────────────────────────────────────
def predict_by_branch(rank):
    con = get_connection()
    if not con:
        return
    cur = con.cursor()

    # Show available branches first
    cur.execute("SELECT DISTINCT course FROM colleges ORDER BY course")
    branches = [r[0] for r in cur.fetchall()]
    print("\n  Available Branches:")
    for i, b in enumerate(branches, 1):
        print(f"    {i}. {b}")

    branch = input("\n  Enter branch name exactly as shown: ").strip()

    query = """
        SELECT institute_name, course, opening_rank, closing_rank
        FROM colleges
        WHERE %s BETWEEN opening_rank AND closing_rank
          AND course = %s
        ORDER BY closing_rank
    """
    cur.execute(query, (rank, branch))
    results = cur.fetchall()
    cur.close()
    con.close()

    print(f"\n  Results for '{branch}' with rank {rank}:\n")
    if not results:
        print("  ⚠️  No colleges found for this branch and rank.")
        return
    for i, r in enumerate(results, 1):
        print(f"  [{i:02}] 🏫 {r[0]}")
        print(f"       📊 Rank Range : {r[2]} — {r[3]}")
        print("       " + "-"*48)

# ─────────────────────────────────────────
#  SHOW ALL BRANCHES
# ─────────────────────────────────────────
def show_branches():
    con = get_connection()
    if not con:
        return
    cur = con.cursor()
    cur.execute("SELECT DISTINCT course FROM colleges ORDER BY course")
    rows = cur.fetchall()
    cur.close()
    con.close()

    print("\n" + "="*50)
    print("         AVAILABLE BRANCHES")
    print("="*50)
    for i, r in enumerate(rows, 1):
        print(f"  {i:2}. {r[0]}")

# ─────────────────────────────────────────
#  MERIT LIST
# ─────────────────────────────────────────
def merit_list():
    con = get_connection()
    if not con:
        return
    cur = con.cursor()

    branch = input("  Enter Branch Name: ").strip()
    query = """
        SELECT s.name, s.stdrank, c.institute_name
        FROM students s
        JOIN colleges c
          ON s.stdrank BETWEEN c.opening_rank AND c.closing_rank
        WHERE c.course = %s
        ORDER BY s.stdrank
    """
    cur.execute(query, (branch,))
    results = cur.fetchall()
    cur.close()
    con.close()

    print(f"\n{'='*60}")
    print(f"   MERIT LIST — {branch}")
    print(f"{'='*60}")
    if not results:
        print("  No students found for this branch.")
        return
    print(f"  {'Rank':<10} {'Name':<25} {'College'}")
    print("  " + "-"*58)
    for r in results:
        print(f"  {r[1]:<10} {r[0]:<25} {r[2]}")

# ─────────────────────────────────────────
#  STUDENT MENU
# ─────────────────────────────────────────
def student_menu(name, rank):
    while True:
        print(f"\n{'='*50}")
        print(f"  Welcome {name}  |  Your JEE Rank: {rank}")
        print(f"{'='*50}")
        print("  1. Predict Colleges (by your rank)")
        print("  2. Predict Colleges (filter by branch)")
        print("  3. Show All Branches")
        print("  4. Merit List")
        print("  5. Logout")
        print(f"{'='*50}")
        ch = input("  Your Choice: ").strip()

        if   ch == "1": predict_college(rank)
        elif ch == "2": predict_by_branch(rank)
        elif ch == "3": show_branches()
        elif ch == "4": merit_list()
        elif ch == "5":
            print(f"\n  👋 Logged out. Goodbye, {name}!")
            break
        else:
            print("  ⚠️  Invalid choice. Enter 1-5.")

# ─────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────
def menu():
    while True:
        print("\n" + "="*50)
        print("    🎓 ENGINEERING ADMISSION PORTAL")
        print("="*50)
        print("  1. Register")
        print("  2. Login")
        print("  3. Exit")
        print("="*50)
        ch = input("  Your Choice: ").strip()

        if   ch == "1": register_student()
        elif ch == "2": login_student()
        elif ch == "3":
            print("\n  👋 Thank you for using the portal. Goodbye!\n")
            break
        else:
            print("  ⚠️  Invalid choice. Enter 1, 2 or 3.")

if __name__ == "__main__":
    menu()
