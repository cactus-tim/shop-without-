import tkinter
from tkinter import *
from tkinter import messagebox
from email_validator import validate_email, EmailNotValidError
from captcha.image import ImageCaptcha
from PIL import ImageTk, Image
from tkinter import ttk
import sqlite3 as sql
import random

flag = False
mail = str()
password = str()


def reg_or_log():
    global cond
    

def attemption_to_reg():
    global mail
    mail = txt_mail.get()
    global password
    password = txt_pass1.get()
    double_check = txt_pass2.get()
    captcha = txt_captcha.get()
    try:
        validation = validate_email(mail, check_deliverability=True)
    except EmailNotValidError as e:
        messagebox.showinfo('Attention', 'Email is incorrect')
        return
    res = cur.execute("SELECT Email FROM users WHERE Email = {mail}")
    if res.fetchall() is []:
        data['email'] = mail
        data['pass'] = password
    else:
        # Дополнительная проверка, по идее можно и без нее
        res = cur.execute("SELECT Email FROM users WHERE Email = {mail}")
        if res.fetchone()[0] == mail:
            messagebox.showinfo('Attention', 'Email is already registered')
            return
    if password != double_check:
        messagebox.showinfo('Attention', 'Passwords are not equal')
    elif len(password) < 8:
        messagebox.showinfo('Attention', 'Password must contain at least 8 characters')
    elif captcha != captcha_text:
        messagebox.showinfo('Attention', 'Captcha is incorrect')
    else:
        global flag
        flag = True
        window.destroy()


def attemption_to_reg2():
    name = txt_name.get()
    surname = txt_sec_name.get()
    dob = str(combobox1.get()) + '.' + str(combobox2.get()) + '.' + str(combobox3.get())
    if len(name) == 0 or len(surname) == 0 or len(combobox1.get()) == 0 or len(combobox2.get()) == 0 or len(
            combobox3.get()) == 0:
        messagebox.showinfo('Attention', 'Some field is empty')
    else:
        data['name'] = name
        data['surname'] = surname
        data['dob'] = dob
        messagebox.showinfo('sheeeeesh', 'вы успешно балдежнули')
        window2.destroy()

def attemption_to_reg2():
    # добавление фото (Киря)
    pass

def data_to_DB():
    res = cur.execute("SELECT ID FROM users ORDER BY ID DESC LIMIT 1")
    prev_user_id = res.fetchall()
    if prev_user_id is not []: # check first user
        res = cur.execute("SELECT ID FROM users ORDER BY ID DESC LIMIT 1")
        prev_user_id = res.fetchone()[0]
        user_id = prev_user_id + 1
        query = f"INSERT INTO users VALUES ('{user_id}', '{data['name']}', '{data['surname']}', '{data['email']}', '{data['pass']}', '{data['dob']}', '{data['face']}', {0})"
        cur.execute(query)
    else:
        user_id = 1
        query = f"INSERT INTO users VALUES ('{user_id}', '{data['name']}', '{data['surname']}', '{data['email']}', '{data['pass']}', '{data['dob']}', '{data['face']}', {0})"
        cur.execute(query)



# Окно
window = Tk()
window.title("Регистрация")
window.geometry('1000x500')

# DB
con = sql.connect('second.db')
cur = con.cursor()
global data
data = {'name': '', 'surname': '', 'email': '', 'pass': '', 'dob': '', 'face': ''}

# Все надписи
lbl_mail = Label(window, text="Почта")
lbl_pass1 = Label(window, text="Пароль")
lbl_pass2 = Label(window, text="Подтвердите Пароль")
lbl_cap = Label(window, text="Введите капчу")
lbl_mail.grid(column=0, row=0)
lbl_pass1.grid(column=0, row=20)
lbl_pass2.grid(column=0, row=40)
lbl_cap.grid(column=0, row=60)

# Все поля для ввода
txt_mail = Entry(window, width=40)
txt_mail.grid(column=1, row=0)
txt_pass1 = Entry(window, width=40)
txt_pass1.grid(column=1, row=20)
txt_pass2 = Entry(window, width=40)
txt_pass2.grid(column=1, row=40)
txt_captcha = Entry(window, width=40)
txt_captcha.grid(column=1, row=60)

# Создание капчи
with open("for_captcha.txt", "r") as file:
    allText = file.read()
    words = list(map(str, allText.split()))
    captcha_text = random.choice(words)

image = ImageCaptcha(width=280, height=90)
image.write(captcha_text, 'CAPTCHA.jpg')
canvas = tkinter.Canvas(window, height=100, width=700)
path = "CAPTCHA.jpg"
img = ImageTk.PhotoImage(Image.open(path))
result = canvas.create_image(0, 0, anchor='nw', image=img)
canvas.grid(row=100, column=100)

# Кнопка
btn = Button(window, text="Зарегистрироваться", command=attemption_to_reg)
btn.grid(column=1, row=80)

window.mainloop()

if flag:  # Проверяем, что первый этап регистрации пройден успешно
    window2 = Tk()
    window2.title("Регистрация")
    window2.geometry('1000x500')
    lbl_name = Label(window2, text="Имя")
    lbl_sec_name = Label(window2, text="Фамилия")
    lbl_date = Label(window2, text="Дата рождения")
    lbl_name.grid(column=0, row=0)
    lbl_sec_name.grid(column=0, row=20)
    lbl_date.grid(column=0, row=40)
    txt_name = Entry(window2, width=40)
    txt_name.grid(column=1, row=0)
    txt_sec_name = Entry(window2, width=40)
    txt_sec_name.grid(column=1, row=20)
    btn2 = Button(window2, text="Подтвердить", command=attemption_to_reg2)
    btn2.grid(column=1, row=120)

    # Списки с числами для даты
    day = ['1', '2', '3']
    days = [str(i + 1) for i in range(31)]
    months = [str(i + 1) for i in range(12)]
    years = [str(i + 1) for i in range(2024, 1950, -1)]

    # Выбор даты рождения
    combobox1 = ttk.Combobox(values=days)
    combobox1.grid(column=1, row=40)
    combobox2 = ttk.Combobox(values=months)
    combobox2.grid(column=2, row=40)
    combobox3 = ttk.Combobox(values=years)
    combobox3.grid(column=3, row=40)

    window2.mainloop()

    # close DB
    con.commit()
    con.close()
