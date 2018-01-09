#todo adding and getting notes, getting timetable, checking groups, buttons 
import telebot
import datetime as dt
import sqlite3 as sql
def file_exists(s):
    try:
        file = open(s,'r')
    except IOError as e:
        return False
    file.close()
    return True
bot = telebot.TeleBot("TOKEN")
tmp = []
lesson_id = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','eleventh','twelvth','thirteenth','fourteenth','fifteenth','sixteenth','eighteenth','nineteenth','twentieth','twentyfirst','twentysecond','twentythird','twentyfourth','twentyfifth','twentysixth','twentyseventh','twentyeighth','twentyninth','thirtieth','thirtyfirst','thirtysecond','thirtythird','thirtyfourth','thirtyfifth']
def day_of_week(d):
    arr = ["Понедельник", "Вторник", "Среда","Четверг","Пятница","Суббота","Воскресенье"]
    return arr[d.weekday()]
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
 bot.reply_to(message, 'Приветствую, введите Вашу группу в формате 11МИ3')
@bot.message_handler(content_types = ['text'])
def all(message):
        global tmp
        conn = sql.connect("user_info")
        c = conn.cursor()
        ch = False
        c.execute('''CREATE TABLE IF NOT EXISTS users(
                ids text primary key, gr text)''')
        print(message.chat.id)
        for i in c.execute("select ids from users"):
            for j in range(len(i)):
                if int(i[0]) == message.chat.id:
                    ch = True
        if not ch:
            reg_lc(bot,message,conn,c)
        elif len(tmp) == 1:
            arr = list(map(int,message.text.split(".")))
            arr.reverse()
            d = dt.date(arr[0],arr[1],arr[2])
            tmp.append(message.text)
            tmp.append(day_of_week(d))
            if tmp[0] == "add":
                s = "добавить"
            else:
                s = "узнать"
            bot.send_message(message.chat.id, "Введите номер предмета, на который вы хотите " + s + " домашнее задание")
        elif len(tmp) == 3:
            if tmp[0] == "get_ht":
                conn = sql.connect("user_info")
                c = conn.cursor()
                c.execute("select [gr] from users where [ids] = (?)", (str(message.chat.id),))
                g = c.fetchone()
                gr = g[0]
                s = gr+"_"+tmp[1]+"_"+message.text+".txt"
                print(s)
                conn.close()
                ch = file_exists(s)
                if not ch:
                    bot.send_message(message.chat.id, "На указанный урок нет домашнего задания")
                else:
                    doc = open(s, 'r')
                    s = ""
                    for line in doc:
                        s += line
                    bot.send_message(message.chat.id, s)
                tmp = []
            elif tmp[0] == "add_ht":
                conn = sql.connect("user_info")
                c = conn.cursor()
                c.execute("select [gr] from users where [ids] = (?)", (str(message.chat.id),))
                g = c.fetchone()
                gr = g[0]
                s = gr+"_"+tmp[1]+"_"+message.text+".txt"
                conn.close()
                tmp.append(s)
                bot.send_message(message.chat.id, "Введите текст домашнего задания")
            elif tmp[0] == "get_n":
                conn = sql.connect("user_info")
                c = conn.cursor()
                c.execute("select [gr] from users where [ids] = (?)", (str(message.chat.id),))
                g = c.fetchone()
                gr = g[0]
                s = gr+"_"+tmp[1]+"_"+message.text+"_note.txt"
                print(s)
                conn.close()
                ch = file_exists(s)
                if not ch:
                    bot.send_message(message.chat.id, "На указанный урок нет заметки")
                else:
                    doc = open(s, 'r')
                    s = ""
                    for line in doc:
                        s += line
                    bot.send_message(message.chat.id, s)
                tmp = []
            elif tmp[0] == "add_n":
                conn = sql.connect("user_info")
                c = conn.cursor()
                c.execute("select [gr] from users where [ids] = (?)", (str(message.chat.id),))
                g = c.fetchone()
                gr = g[0]
                s = gr+"_"+tmp[1]+"_"+message.text+"_note.txt"
                conn.close()
                tmp.append(s)
                bot.send_message(message.chat.id, "Введите текст заметки")
        elif len(tmp) == 4:
            s = tmp[3]
            doc = open(s, "a+")
            doc.write(message.chat.username+" добавил:\n" + message.text+"\n")
            if tmp[0] == "add_ht":
                bot.send_message(message.chat.id, "ДЗ успешно добавлено.")
            else:
                bot.send_message(message.chat.id, "Заметка успешно добавлена.")
            tmp = []
        elif message.text == "Добавить домашнее задание":
            tmp.append("add_ht")
            bot.send_message(message.chat.id, "Введите дату в формате 01.01.2018")
        elif message.text == "Узнать домашнее задание":
            tmp.append("get_ht")
            bot.send_message(message.chat.id, "Введите дату в формате 01.01.2018")
        elif message.text == "Добавить заметку":
            tmp.append("add_n")
            bot.send_message(message.chat.id, "Введите дату в формате 01.01.2018")
        elif message.text == "Просмотреть заматеку":
            tmp.append("get_n")
            bot.send_message(message.chat.id, "Введите дату в формате 01.01.2018")
        else:
            bot.send_message(message.chat.id,"Простите, я Вас не понимаю")
def reg_lc(bot,message,conn,c):
        c.execute("insert into users([ids]) values(?)", (message.chat.id,))
        c.execute("update users set [gr] = ? where [ids] = ?",(message.text,message.chat.id))
        bot.send_message(message.chat.id, "Вы успешно зарегистрировались")
        conn.commit()
        conn.close()
        return None
bot.polling()
