import telebot
import time
from telebot import types
import datetime as dt
import sqlite3 as sql
def file_exists(s):
    s.encode('utf-8')
    try:
        file = open(s,'r')
    except IOError as e:
        print(e)
        return False
    file.close()
    return True
def sm(bot,chat,s,markup):
    try:
        bot.send_message(chat,s,reply_markup = markup)
    except Exception as e:
        print(e)
bot = telebot.TeleBot("TOKEN")
cnt = 1
markup = types.ReplyKeyboardMarkup(True, False,row_width=1)
get_ht = types.KeyboardButton(text='Узнать домашнее задание')
add_ht = types.KeyboardButton(text='Добавить домашнее задание')
get_nt = types.KeyboardButton(text='Посмотреть заметку')
add_nt = types.KeyboardButton(text='Добавить заметку')
change_gr = types.KeyboardButton(text='Сбросить настройки аккаунта')
c_dev = types.KeyboardButton(text='Связаться с разработчиком')
get_tt = types.KeyboardButton(text = 'Узнать расписание')
markup.row(get_ht, add_ht)
markup.row(get_nt, add_nt)
markup.row(get_tt)
markup.row(change_gr, c_dev)
bckbtn = types.KeyboardButton(text="Вернуться назад")
mark = types.ReplyKeyboardMarkup(True, False, row_width = 1)
mark.row(bckbtn)
gr_arr = ["10В1","10В2","10Г1","10Г2","10Г3","10Г4","10Г5","10Д1","10Д2","10МИ1","10МИ2","10МИ3","10МИ4","10МИ5","10МЭ1","10МЭ2","10МЭ3","10МЭ4","10МЭ5","10МЭ6","10П1","10П2","10СЭ1","10СЭ2","10СЭ3","10СЭ4","10СЭ5","10Ю1","10Ю2","11В1","11В2","11Г1","11Г2","11Г3","11Г4","11Г5","11Г6","11Д1","11Д2","11МИ1","11МИ2","11МИ3","11МЭ1","11МЭ2","11МЭ3","11МЭ4","11МЭ5","11МЭ6", "11П1","11П2","11СЭ1","11СЭ2","11СЭ3","11СЭ4","11СЭ5","11СЭ6","11СЭ7","11Ю1","11Ю2"]
lesson_id = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','eleventh','twelvth','thirteenth','fourteenth','fifteenth','sixteenth','eighteenth','nineteenth','twentieth','twentyfirst','twentysecond','twentythird','twentyfourth','twentyfifth','twentysixth','twentyseventh','twentyeighth','twentyninth','thirtieth','thirtyfirst','thirtysecond','thirtythird','thirtyfourth','thirtyfifth','thirtysixth','thirtyseventh','thirtyeighth','thirtyninth','fortyth','fortyfirst','fortysecond','fortythird','fortyfourth','fortyfifth','fortysixth','fortyseventh','fortyeighth','fortyninth','fiftyth']
def day_of_week(d):
    arr = ["Понедельник", "Вторник", "Среда","Четверг","Пятница","Суббота","Воскресенье"]
    return arr[d.weekday()]
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
     sm(bot,message.chat.id,'Приветствую, введите Вашу группу в формате 11МИ3',markup)

@bot.message_handler(content_types = ['photo'])
def photo(message):
    global markup
    tmp = []
    f = open(str(message.chat.id)+"_tmp.txt","r")
    for line in f:
            if line != "" or line != "\n":
                tmp.append(line[:-1])
                print(line)
    f.close()
    if len(tmp) == 4:
            file_info = bot.get_file(message.photo[-1].file_id)
            down_file = bot.download_file(file_info.file_path)
            print(file_info)
            src = tmp[3]
            with open(src+".jpg","wb") as new_file:
                new_file.write(down_file)
    f = open(str(message.chat.id)+"_tmp.txt","w")
    f.write("")
    f.close()
    bot.send_message(message.chat.id, "Фотография успешно добавлена", reply_markup = markup)
@bot.message_handler(content_types = ['text'])
def text(message):
        global markup
        global mark
        tmp = []
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
            return False
        f = open(str(message.chat.id)+"_tmp.txt","r")
        for line in f:
            if line != "" or line != "\n":
                tmp.append(line[:-1])
                print(line)
        f.close()
        if message.text == "Вернуться назад":
            f = open(str(message.chat.id)+"_tmp.txt","w")
            f.write("")
            f.close()
            sm(bot,message.chat.id, "Чем могу помочь?", markup)
        elif len(tmp) == 1:
            try:
                arr = list(map(int,message.text.split(".")))
                arr.reverse()
                d = dt.date(arr[0],arr[1],arr[2])
                tmp.append(message.text)
                tmp.append(day_of_week(d))
                if tmp[2] == "Воскресенье" or tmp[2] == "Четверг":
                    sm(bot, message.chat.id, "В этот день нет пар", markup)
                    tmp = []
                elif tmp[0] == "add_ht":
                    s = "добавить"
                    sm(bot, message.chat.id, "Введите id предмета, на который вы хотите " + s + " домашнее задание", mark)
                elif tmp[0] == "get_ht":
                    s = "узнать"
                    sm(bot, message.chat.id, "Введите id предмета, на который вы хотите " + s + " домашнее задание", mark)
                elif tmp[0] == "add_n":
                    s = "добавить"
                    sm(bot,message.chat.id, "Введите id предмета, на который вы хотите " + s + " заметку", mark)
                elif tmp[0] == "get_n":
                    s = "узнать"
                    sm(bot,message.chat.id, "Введите id, на который вы хотите " + s + " заметку", mark)
                f = open(str(message.chat.id)+"_tmp.txt", "a+")
                f.write(tmp[1]+"\n")
                f.write(tmp[2]+"\n")
                f.close()
                return None
            except Exception as e:
                print(e)
                sm(bot,message.chat.id, "Некорректный формат данных, попробуйте снова", mark)
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
                    sm(bot,message.chat.id, "На указанный урок нет домашнего задания", markup)
                if ch:
                    doc = open(s+".txt", 'r')
                    k = ""
                    for line in doc:
                        k += line
                    sm(bot,message.chat.id, k,markup)
                if chf:
                    with open(s+'.jpg', 'rb') as f:
                        bot.send_photo(message.chat.id, f, reply_markup= markup)
                f = open(str(message.chat.id)+"_tmp.txt","w")
                f.write("")
                f.close()
            elif tmp[0] == "add_ht":
                conn = sql.connect("user_info")
                c = conn.cursor()
                c.execute("select [gr] from users where [ids] = (?)", (str(message.chat.id),))
                g = c.fetchone()
                gr = g[0]
                s = gr+"_"+tmp[1]+"_"+message.text
                conn.close()
                tmp.append(s)
                sm(bot,message.chat.id, "Введите текст домашнего задания, либо отправьте фотографию. Обращаю внимание на факт, что фотография может быть только одна к каждому уроку, новые фотографии перезаписывают старые.",mark)
                f = open(str(message.chat.id)+"_tmp.txt","a+")
                f.write(tmp[3]+"\n")
                f.close()
            elif tmp[0] == "get_n":
                conn = sql.connect("user_info")
                c = conn.cursor()
                c.execute("select [gr] from users where [ids] = (?)", (str(message.chat.id),))
                g = c.fetchone()
                gr = g[0]
                s = gr+"_"+tmp[1]+"_"+message.text+"_note"
                print(s)
                conn.close()
                ch = file_exists(s+".txt")
                if not ch:
                    sm(bot,message.chat.id, "На указанный урок нет заметки", markup)
                else:
                    doc = open(s+".txt", 'r')
                    s = ""
                    for line in doc:
                        s += line
                    sm(bot,message.chat.id, s, markup)
                f = open(str(message.chat.id)+"_tmp.txt","w")
                f.write("")
                f.close()
            elif tmp[0] == "add_n":
                conn = sql.connect("user_info")
                c = conn.cursor()
                c.execute("select [gr] from users where [ids] = (?)", (str(message.chat.id),))
                g = c.fetchone()
                gr = g[0]
                s = gr+"_"+tmp[1]+"_"+message.text+"_note"
                conn.close()
                tmp.append(s)
                f = open(str(message.chat.id)+"_tmp.txt","a+")
                f.write(tmp[3]+"\n")
                f.close()
                sm(bot,message.chat.id, "Введите текст заметки", mark)
        elif len(tmp) == 4:
            s = tmp[3]
            doc = open(s+".txt", "a+")
            try:
                doc.write(message.chat.username+" добавил:\n" + message.text+"\n")
            except Exception as e:
                print(e)
                doc.write("Пользователь " + str(message.chat.id)+" добавил:\n" + message.text+"\n")        
            if tmp[0] == "add_ht":
                sm(bot,message.chat.id, "ДЗ успешно добавлено.",markup)
            else:
                sm(bot,message.chat.id, "Заметка успешно добавлена.", markup)
            f = open(str(message.chat.id)+"_tmp.txt","w")
            f.write("")
            f.close()
        elif message.text == "Добавить домашнее задание":
            tmp.append("add_ht")
            f = open(str(message.chat.id)+"_tmp.txt","a+")
            f.write(tmp[0]+"\n")
            f.close()
            sm(bot,message.chat.id, "Введите дату в формате 01.01.2018", mark)
        elif message.text == "Узнать домашнее задание":
            tmp.append("get_ht")
            f = open(str(message.chat.id)+"_tmp.txt","a+")
            f.write(tmp[0]+"\n")
            f.close()
            sm(bot,message.chat.id, "Введите дату в формате 01.01.2018", mark)
        elif message.text == "Добавить заметку":
            tmp.append("add_n")
            f = open(str(message.chat.id)+"_tmp.txt","a+")
            f.write(tmp[0]+"\n")
            f.close()
            sm(bot,message.chat.id, "Введите дату в формате 01.01.2018", mark)
        elif message.text == "Посмотреть заметку":
            tmp.append("get_n")
            f = open(str(message.chat.id)+"_tmp.txt","a+")
            f.write(tmp[0]+"\n")
            f.close()
            sm(bot,message.chat.id, "Введите дату в формате 01.01.2018", mark)
        elif message.text == 'Связаться с разработчиком':
            sm(bot,message.chat.id, 'Связаться с разработчиком можно в Telegram @IceBlink1 либо по почте lyutiko.alex@gmail.com', markup)
        elif message.text == "Сбросить настройки аккаунта":
            del_lc(bot,message,conn,c)
        elif message.text == "Узнать расписание":
            conn = sql.connect("user_info")
            c = conn.cursor()
            c.execute("select [gr] from users where [ids] = (?)", (str(message.chat.id),))
            g = c.fetchone()
            gr = g[0]
            s = g[0]+".txt"
            ch = file_exists(s)
            if not ch:
                sm(bot,message.chat.id, "Нет данных", markup)
            else:
                doc = open(s, 'r')
                k = ""
                cnt = 1
                arr = ["Вторник", "Среда", "Пятница", "Суббота"]
                for line in doc:
                    try:
                        line = int(line)
                    except Exception as e:
                        for i in arr:
                            if i+"\n" == line and line != "Понедельник\n":
                                cnt = 1
                                sm(bot,message.chat.id,k,markup)
                                k = line
                        if line == "Понедельник\n":
                           k+=line
                        elif line[0].isalpha():
                            pass
                        elif line == g[0]+'\n':
                            k+=line
                        elif line == "\n":
                            pass
                        else:
                            k +=  line[0:-1]+" id = " + str(cnt) + " \n"
                            cnt+=1
                    print(line)
                try:
                    bot.send_message(message.chat.id, k, reply_markup = markup)
                except Exception as o:
                    print(o)
                    sm(bot,message.chat.id, "Бот перегружен, попробуйте позже", markup)
        else:
            sm(bot,message.chat.id,"Простите, я Вас не понимаю", markup)
def reg_lc(bot,message,conn,c):
        global markup
        global gr_arr
        if message.text in gr_arr:
            c.execute("insert into users([ids]) values(?)", (message.chat.id,))
            c.execute("update users set [gr] = ? where [ids] = ?",(message.text,message.chat.id))
            sm(bot,message.chat.id, "Вы успешно зарегистрировались", markup)
            conn.commit()
            conn.close()
            f = open(str(message.chat.id)+"_tmp.txt","w+")
            f.close()
        else:
            bot.send_message(message.chat.id, "Нет данных о такой группе, попробуйте еще раз или свяжитесь с разработчиком")
        return None
def del_lc(bot, message, conn, c):
    c.execute("delete from users where [ids] = ?", (message.chat.id,))
    sm(bot,message.chat.id, "Данные успешно удалены. Для повторной регистрации отправьте номер новой группы",markup)
    conn.commit()
    conn.close()
    return None
while True:
    try:
        bot.polling(none_stop = True)
    except Exception as e:
        time.sleep(15)
