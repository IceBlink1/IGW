import sqlite3 as sql
s = input()
conn = sql.connect(s)
c = conn.cursor()
arr = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','eleventh','twelvth','thirteenth','fourteenth','fifteenth','sixteenth','eighteenth','nineteenth','twentieth','twentyfirst','twentysecond','twentythird','twentyfourth','twentyfifth','twentysixth','twentyseventh','twentyeighth','twentyninth','thirtieth','thirtyfirst','thirtysecond','thirtythird','thirtyfourth','thirtyfifth']
c.execute('''CREATE TABLE IF NOT EXISTS timetable(
            day text primary key, amount integer)''')
max = 0
for j in range(5):
    s = input()
    n = int(input())
    c.execute('''insert into timetable([day],[amount]) values(?,?)''',(s,n))
    for i in range(max,n):
        
        c.execute('''ALTER TABLE timetable ADD COLUMN '''+arr[i]+'''_lesson text''')
        c.execute('''ALTER TABLE timetable ADD COLUMN '''+arr[i]+'''_lesson_teacher text''')
    if n > max:
        max = n
    for i in range(n):
        s1 = input()
        s2 = input()
        c.execute('''update timetable set '''+arr[i]+'''_lesson = ? where day = ?''',(s1,s))
        c.execute('''update timetable set '''+arr[i]+'''_lesson_teacher = ? where day = ?''',(s2,s))
        
    print()
conn.commit()
conn.close()
