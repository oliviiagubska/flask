import sqlite3
con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute(""" INSERT INTO Employee (EmpID, EmpName, HireDate, Salary)
            VALUES (1122, 'Bloggs', '#1/1/2001#', 18000)
            """)
con.commit()
con.close()
