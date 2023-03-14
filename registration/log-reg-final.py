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

def reg():
    window.destroy()

    global window_reg1
    window_reg1 = Tk()
    window_reg1.title("Регистрация")

    # Все надписи
    lbl_mail = Label(window_reg1, text="Почта")
    lbl_pass1 = Label(window_reg1, text="Пароль")
    lbl_pass2 = Label(window_reg1, text="Подтвердите Пароль")
    lbl_cap = Label(window_reg1, text="Введите капчу")
    lbl_mail.grid(column=0, row=0)
    lbl_pass1.grid(column=0, row=20)
    lbl_pass2.grid(column=0, row=40)
    lbl_cap.grid(column=0, row=60)

    # Все поля для ввода
    global txt_mail
    txt_mail = Entry(window_reg1, width=40)
    txt_mail.grid(column=1, row=0)
    global txt_pass1
    txt_pass1 = Entry(window_reg1, width=40)
    txt_pass1.grid(column=1, row=20)
    global txt_pass2
    txt_pass2 = Entry(window_reg1, width=40)
    txt_pass2.grid(column=1, row=40)
    global txt_captcha
    txt_captcha = Entry(window_reg1, width=40)
    txt_captcha.grid(column=1, row=60)

    # Создание капчи
    global captcha_text
    with open("for_captcha.txt", "r") as file:
        allText = file.read()
        words = list(map(str, allText.split()))
        captcha_text = random.choice(words)

    image = ImageCaptcha(width=280, height=90)
    image.write(captcha_text, 'CAPTCHA.jpg')
    canvas = tkinter.Canvas(window_reg1, height=100, width=700)
    path = "CAPTCHA.jpg"
    img = ImageTk.PhotoImage(Image.open(path))
    result = canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.grid(row=100, column=100)

    # Кнопка
    btn = Button(window_reg1, text="Зарегистрироваться", command=attemption_to_reg)
    btn.grid(column=1, row=80)

    window_reg1.mainloop()

    if flag:  # Проверяем, что первый этап регистрации пройден успешно
        global window_reg2
        window_reg2 = Tk()
        window_reg2.title("Регистрация")
        window_reg2.geometry('1000x500')
        lbl_name = Label(window_reg2, text="Имя")
        lbl_sec_name = Label(window_reg2, text="Фамилия")
        lbl_date = Label(window_reg2, text="Дата рождения")
        lbl_name.grid(column=0, row=0)
        lbl_sec_name.grid(column=0, row=20)
        lbl_date.grid(column=0, row=40)
        global txt_name
        txt_name = Entry(window_reg2, width=40)
        txt_name.grid(column=1, row=0)
        global txt_sec_name
        txt_sec_name = Entry(window_reg2, width=40)
        txt_sec_name.grid(column=1, row=20)

        # кнопка
        btn2 = Button(window_reg2, text="Подтвердить", command=attemption_to_reg2)
        btn2.grid(column=1, row=120)

        # Списки с числами для даты
        day = ['1', '2', '3']
        days = [str(i + 1) for i in range(31)]
        months = [str(i + 1) for i in range(12)]
        years = [str(i + 1) for i in range(2024, 1950, -1)]

        # Выбор даты рождения
        global combobox1
        combobox1 = ttk.Combobox(values=days)
        combobox1.grid(column=1, row=40)
        global combobox2
        combobox2 = ttk.Combobox(values=months)
        combobox2.grid(column=2, row=40)
        global combobox3
        combobox3 = ttk.Combobox(values=years)
        combobox3.grid(column=3, row=40)

        window_reg2.mainloop()

        # lbl_name = Label(window_reg2, text="Имя")
        # lbl_name.grid(column=0, row=0)
        # global txt_name
        # txt_name = Entry(window_reg2, width=40)
        # txt_name.grid(column=1, row=0)

        global window_reg3
        window_reg3 = Tk()
        window_reg3.title("Регистрация")
        window_reg3.geometry('1000x500')

        lbl_link = Label(window_reg3, text="Ссылка на вашу фотографию")
        lbl_link.grid(column=0, row=0)
        global txt_link_face
        txt_link_face = Entry(window_reg3, width=40)
        txt_link_face.grid(column=1, row=20)

        # кнопка
        btn = Button(window_reg3, text="Подтвердить", command=attemption_to_reg3)
        btn.grid(column=1, row=120)

        window_reg3.mainloop()

def log():
    window.destroy()

    global window_log
    window_log = Tk()
    window_log.title("Ввойти в аккаунт")

    # Все надписи
    lbl_mail = Label(window_log, text="Почта")
    lbl_pass1 = Label(window_log, text="Пароль")
    lbl_cap = Label(window_log, text="Введите капчу")
    lbl_mail.grid(column=0, row=0)
    lbl_pass1.grid(column=0, row=20)
    lbl_cap.grid(column=0, row=60)

    # Все поля для ввода
    global txt_mail_log
    txt_mail_log = Entry(window_log, width=40)
    txt_mail_log.grid(column=1, row=0)
    global txt_pass_log
    txt_pass_log = Entry(window_log, width=40)
    txt_pass_log.grid(column=1, row=20)
    global txt_captcha_log
    txt_captcha_log = Entry(window_log, width=40)
    txt_captcha_log.grid(column=1, row=60)

    # Создание капчи
    global captcha_text_log
    with open("for_captcha.txt", "r") as file:
        allText = file.read()
        words = list(map(str, allText.split()))
        captcha_text_log = random.choice(words)

    image = ImageCaptcha(width=280, height=90)
    image.write(captcha_text_log, 'CAPTCHA.jpg')
    canvas = tkinter.Canvas(window_log, height=100, width=700)
    path = "CAPTCHA.jpg"
    img = ImageTk.PhotoImage(Image.open(path))
    result = canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.grid(row=100, column=100)

    # Кнопка
    btn = Button(window_log, text="Ввойти в аккаунт", command=attemption_to_log)
    btn.grid(column=1, row=80)

    window_log.mainloop()

def attemption_to_log():
    mail = txt_mail_log.get()
    password = txt_pass_log.get()
    captcha = txt_captcha_log.get()
    # try:
    #     validation = validate_email(mail, check_deliverability=True)
    # except EmailNotValidError as e:
    #     messagebox.showinfo('Attention', 'Email is incorrect')
    #     return
    query = f"SELECT Email FROM users WHERE Email = '{mail}'"
    res = cur.execute(query)
    if not res.fetchall():
        messagebox.showinfo('Attention', 'Email is incorrect')
        return
    query = f"SELECT Password FROM users WHERE Email = '{mail}'"
    res = cur.execute(query)
    true_password = res.fetchone()[0]
    if password != str(true_password):
        messagebox.showinfo('Attention', 'Password is incorrect')
    elif captcha != captcha_text_log:
        messagebox.showinfo('Attention', 'Captcha is incorrect')
    else:
        messagebox.showinfo('sheeeeesh', 'вы успешно балдежнули')
        window_log.destroy()

def attemption_to_reg():
    mail = txt_mail.get()
    password = txt_pass1.get()
    double_check = txt_pass2.get()
    captcha = txt_captcha.get()
    # try:
    #     validation = validate_email(mail, check_deliverability=True)
    # except EmailNotValidError as e:
    #     messagebox.showinfo('Attention', 'Email is incorrect')
    #     return
    query = f"SELECT Email FROM users WHERE Email = '{mail}'"
    res = cur.execute(query)
    if not res.fetchall():
        data['email'] = mail
        data['pass'] = password
    else:
        # Дополнительная проверка, по идее можно и без нее
        res = cur.execute(query)
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
        window_reg1.destroy()


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
        window_reg2.destroy()

def attemption_to_reg3():
    link = txt_link_face.get()
    data['face'] = link
    messagebox.showinfo('sheeeeesh', 'вы успешно балдежнули')
    data_to_DB()
    window_reg3.destroy()

def data_to_DB():
    res = cur.execute("SELECT ID FROM users ORDER BY ID DESC LIMIT 1")
    user_id = 1
    query = f"INSERT INTO users VALUES ('{user_id}', '{data['name']}', '{data['surname']}', '{data['email']}', '{data['pass']}', '{data['dob']}', '{data['face']}', {0})"
    if not res.fetchall(): # check first user
        cur.execute(query)
    else:
        res = cur.execute("SELECT ID FROM users ORDER BY ID DESC LIMIT 1")
        prev_user_id = res.fetchone()[0]
        user_id += prev_user_id
        cur.execute(query)
    con.commit()


# DB
con = sql.connect('second.db')
cur = con.cursor()
global data
data = {'name': '', 'surname': '', 'email': '', 'pass': '', 'dob': '', 'face': ''}

# Окно
window = Tk()
window.geometry('1000x500')

# Регестраци или капча
btn = Button(window, text="Регистрация", command=reg)
btn.grid(column=1, row=0)
btn1 = Button(window, text="Войти в аккаунт", command=log)
btn1.grid(column=1, row=40)

window.mainloop()



# close DB
con.close()

# 182 214