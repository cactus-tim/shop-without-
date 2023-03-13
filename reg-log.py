from tkinter import *
from tkinter import messagebox
from email_validator import validate_email, EmailNotValidError


def clicked():
    password = Pass1.get()
    double_check = Pass2.get()
    mail = Mail.get()
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
    else:
        f = open("Reg.txt", 'a')
        f.write('\n')
        f.write(mail)
        f.write(' ')
        f.write(password)
        f.close()




window = Tk()
window.title("Регистрация")
window.geometry('400x250')

lbl_mail = Label(window, text="Почта")
lbl_pass1 = Label(window, text="Пароль")
lbl_pass2 = Label(window, text="Подтвердите Пароль")
lbl_mail.grid(column=0, row=0)
lbl_pass1.grid(column=0, row=20)
lbl_pass2.grid(column=0, row=40)

Mail = Entry(window, width=40)
Mail.grid(column=1, row=0)
Pass1 = Entry(window, width=40)
Pass1.grid(column=1, row=20)
Pass2 = Entry(window, width=40)
Pass2.grid(column=1, row=40)

btn = Button(window, text="Зарегистрироваться", command=clicked)
btn.grid(column=1, row=60)

window.mainloop()
