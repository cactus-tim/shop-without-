import tkinter
from tkinter import *
from tkinter import messagebox
from email_validator import validate_email, EmailNotValidError
from captcha.image import ImageCaptcha
from PIL import ImageTk, Image
import random


def attemption_to_reg():
    password = txt_pass1.get()
    double_check = txt_pass2.get()
    mail = txt_mail.get()
    captcha = txt_captcha.get()
    try:
        validation = validate_email(mail, check_deliverability=True)
    except EmailNotValidError as e:
        messagebox.showinfo('Attention', 'Email is incorrect')
        return
    f = open("Reg.txt", 'r')
    for i in f:
        pr = i.find(' ')
        if i[:pr] == mail:
            messagebox.showinfo('Attention', 'Email is already registered')
            return
    f.close()
    if password != double_check:
        messagebox.showinfo('Attention', 'Passwords are not equal')
    elif len(password) < 8:
        messagebox.showinfo('Attention', 'Password must contain at least 8 characters')
    elif captcha != captcha_text:
        messagebox.showinfo('Attention', 'Captcha is incorrect')
    else:
        f = open("Reg.txt", 'a')
        f.write('\n')
        f.write(mail)
        f.write(' ')
        f.write(password)
        f.close()
        window.destroy()


window = Tk()
window.title("Регистрация")
window.geometry('1000x500')

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
