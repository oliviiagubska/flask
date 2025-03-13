import sqlite3
con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute(""" UPDATE Employee
            SET Salary = Salary * 1.1
            WHERE EmpID = 1122
            """)
con.commit()
con.close()

