import sqlite3
con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute(""" DELETE FROM Employee
                WHERE EmpID = "1122"
            """)
con.commit()
con.close()

