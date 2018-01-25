import telebot
from telebot import types
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
cnt = 1
markup = types.ReplyKeyboardMarkup(True, False,row_width=1)
get_ht = types.KeyboardButton(text='Узнать домашнее задание')
add_ht = types.KeyboardButton(text='Добавить домашнее задание')
get_nt = types.KeyboardButton(text='Посмотреть заметку')
add_nt = types.KeyboardButton(text='Добавить заметку')
change_gr = types.KeyboardButton(text='Сбросить настройки аккаунта')
c_dev = types.KeyboardButton(text='Связаться с разработчиком')
markup.row(get_ht, add_ht)
markup.row(get_nt, add_nt)
markup.row(change_gr, c_dev)
bckbtn = types.KeyboardButton(text="Вернуться назад")
mark = types.ReplyKeyboardMarkup(True, False, row_width = 1)
mark.row(bckbtn)
lesson_id = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','eleventh','twelvth','thirteenth','fourteenth','fifteenth','sixteenth','eighteenth','nineteenth','twentieth','twentyfirst','twentysecond','twentythird','twentyfourth','twentyfifth','twentysixth','twentyseventh','twentyeighth','twentyninth','thirtieth','thirtyfirst','thirtysecond','thirtythird','thirtyfourth','thirtyfifth','thirtysixth','thirtyseventh','thirtyeighth','thirtyninth','fortyth','fortyfirst','fortysecond','fortythird','fortyfourth','fortyfifth','fortysixth','fortyseventh','fortyeighth','fortyninth','fiftyth']
def day_of_week(d):
    arr = ["Понедельник", "Вторник", "Среда","Четверг","Пятница","Суббота","Воскресенье"]
    return arr[d.weekday()]
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
 bot.reply_to(message, 'Приветствую, введите Вашу группу в формате 11МИ3')

@bot.message_handler(content_types = ['photo'])
def photo(message):
    global tmp
    global cnt
    if len(tmp) == 4:
            file_info = bot.get_file(message.photo[-1].file_id)
            down_file = bot.download_file(file_info.file_path)
            print(file_info)
            src = tmp[3]
            with open(src+".jpg","wb") as new_file:
                new_file.write(down_file)
@bot.message_handler(content_types = ['text'])
def text(message):
        global markup
        global tmp
        global mark
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
        elif message.text == "Вернуться назад":
            tmp = []
            bot.send_message(message.chat.id, "Чем могу помочь?", reply_markup = markup)
        elif len(tmp) == 1:
            arr = list(map(int,message.text.split(".")))
            arr.reverse()
            d = dt.date(arr[0],arr[1],arr[2])
            tmp.append(message.text)
            tmp.append(day_of_week(d))
            if tmp[2] == "Воскресенье" or tmp[2] == "Четверг":
                bot.send_message(message.chat.id, "В этот день нет пар", reply_markup = markup)
                tmp = []
            elif tmp[0] == "add_ht":
                s = "добавить"
                bot.send_message(message.chat.id, "Введите номер предмета, на который вы хотите " + s + " домашнее задание", reply_markup = mark)
            elif tmp[0] == "get_ht":
                s = "узнать"
                bot.send_message(message.chat.id, "Введите номер предмета, на который вы хотите " + s + " домашнее задание",reply_markup = mark)
            elif tmp[0] == "add_n":
                s = "добавить"
                bot.send_message(message.chat.id, "Введите номер предмета, на который вы хотите " + s + " заметку",reply_markup = mark)
            elif tmp[0] == "get_n":
                s = "узнать"
                bot.send_message(message.chat.id, "Введите номер предмета, на который вы хотите " + s + " заметку",reply_markup = mark)
        elif len(tmp) == 3:
            if tmp[0] == "get_ht":
                conn = sql.connect("user_info")
                c = conn.cursor()
                c.execute("select [gr] from users where [ids] = (?)", (str(message.chat.id),))
                g = c.fetchone()
                gr = g[0]
                s = gr+"_"+tmp[1]+"_"+message.text
                print(s)
                conn.close()
                ch = file_exists(s+".txt")
                chf = file_exists(s+".jpg")
                if not ch and not chf:
                    bot.send_message(message.chat.id, "На указанный урок нет домашнего задания", reply_markup = markup)
                if ch:
                    doc = open(s+".txt", 'r')
                    k = ""
                    for line in doc:
                        k += line
                    bot.send_message(message.chat.id, k,reply_markup = markup)
                if chf:
                    with open(s+'.jpg', 'rb') as f:
                        bot.send_photo(message.chat.id, f, reply_markup= markup)
                tmp = []
            elif tmp[0] == "add_ht":
                conn = sql.connect("user_info")
                c = conn.cursor()
                c.execute("select [gr] from users where [ids] = (?)", (str(message.chat.id),))
                g = c.fetchone()
                gr = g[0]
                s = gr+"_"+tmp[1]+"_"+message.text
                conn.close()
                tmp.append(s)
                bot.send_message(message.chat.id, "Введите текст домашнего задания",reply_markup = mark)
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
                    bot.send_message(message.chat.id, "На указанный урок нет заметки",reply_markup = markup)
                else:
                    doc = open(s, 'r')
                    s = ""
                    for line in doc:
                        s += line
                    bot.send_message(message.chat.id, s, reply_markup = markup)
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
                bot.send_message(message.chat.id, "Введите текст заметки",reply_markup = mark)
        elif len(tmp) == 4:
            s = tmp[3]
            doc = open(s+".txt", "a+")
            doc.write(message.chat.username+" добавил:\n" + message.text+"\n")
            if tmp[0] == "add_ht":
                bot.send_message(message.chat.id, "ДЗ успешно добавлено.",reply_markup = markup)
            else:
                bot.send_message(message.chat.id, "Заметка успешно добавлена.",reply_markup = markup)
            tmp = []
        elif message.text == "Добавить домашнее задание":
            tmp.append("add_ht")
            bot.send_message(message.chat.id, "Введите дату в формате 01.01.2018",reply_markup = mark)
        elif message.text == "Узнать домашнее задание":
            tmp.append("get_ht")
            bot.send_message(message.chat.id, "Введите дату в формате 01.01.2018",reply_markup = mark)
        elif message.text == "Добавить заметку":
            tmp.append("add_n")
            bot.send_message(message.chat.id, "Введите дату в формате 01.01.2018",reply_markup = mark)
        elif message.text == "Посмотреть заметку":
            tmp.append("get_n")
            bot.send_message(message.chat.id, "Введите дату в формате 01.01.2018",reply_markup = mark)
        elif message.text == 'Связаться с разработчиком':
            bot.send_message(message.chat.id, 'Связаться с разработчиком можно в Telegram @IceBlink1 либо по почте lyutiko.alex@gmail.com',reply_markup = markup)
        elif message.text == "Сбросить настройки аккаунта":
            del_lc(bot,message,conn,c)
        else:
            bot.send_message(message.chat.id,"Простите, я Вас не понимаю",reply_markup = markup)
def reg_lc(bot,message,conn,c):
        global markup
        c.execute("insert into users([ids]) values(?)", (message.chat.id,))
        c.execute("update users set [gr] = ? where [ids] = ?",(message.text,message.chat.id))
        bot.send_message(message.chat.id, "Вы успешно зарегистрировались", reply_markup = markup)
        conn.commit()
        conn.close()
        return None
def del_lc(bot, message, conn, c):
    c.execute("delete from users where [ids] = ?", (message.chat.id,))
    bot.send_message(message.chat.id, "Данные успешно удалены. Для повторной регистрации отправьте номер новой группы")
    conn.commit()
    conn.close()
    return None
bot.polling()

