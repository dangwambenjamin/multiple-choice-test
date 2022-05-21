from tkinter import *
from tkinter import messagebox
from questionsList import *
from csv import *

root = Tk()
root.geometry('600x250')
root.title('Objective Test')

# left menu section
menu = LabelFrame(root, text='MENU')
menu.grid(row=0, column=0, padx=(50, 0), pady=30)

# right content section
content = LabelFrame(root, text='')
content.grid(row=0, column=1, pady=30, padx=(2, 10))

# bottom navigation panel
nav = LabelFrame(content)
nav.grid(row=1, column=0, columnspan=5)

global username_box
global password_box
global index


def login():
    global username_box
    global password_box

    username_label = Label(menu, text='USERNAME')
    username_label.grid(row=2, column=0, padx=(10, 10), pady=(5, 5))
    password_label = Label(menu, text='PASSWORD')
    password_label.grid(row=3, column=0, padx=(10, 10), pady=(5, 5))

    username_box = Entry(menu, width=50)
    password_box = Entry(menu, width=50)
    username_box.grid(row=2, column=1, padx=(10, 50), pady=(5, 5))
    password_box.grid(row=3, column=1, padx=(10, 50), pady=(5, 10))

    send = Button(menu, text='SEND', fg='green', font=('', 10, 'bold'), command=validate)
    send.grid(row=4, column=0, columnspan=2, pady=(5, 50), ipadx=100)
    messagebox.askokcancel('NOTICE', 'USE USERNAME "admin", AND PASSWORD "password" TO LOGIN AS ADMIN\n OR PRESS "SEND" TO TAKE TEST')


def validate():
    global index

    if username_box.get() in Admin.admins and Admin.admins[username_box.get()] == password_box.get():
        # convert dictionary with usernames and password to list to get index
        convert = list(Admin.admins)
        index = convert.index(username_box.get())
        # use index to get corresponding instance in Admin all list
        Admin.callMethods(Admin.all[index])
    else:
        key = messagebox.askquestion('CONFIRM', 'Are You Ready For The Test??')
        if key == 'yes':
            test(currentTest)


q_num = 0
total = len(currentTest)
response = {}

global quest
global alpha
global beta
global gamma
global delta
global label
global prev_btn
global next_btn
global questions_page
global submit_page
global space
global r
global var
global pr2


def buttons(digit, data):
    global q_num
    q_index = total - 1
    response[var] = data

    if digit == 1 and q_num != 0:
        if q_num == q_num:
            submit_page.destroy()
        q_num -= 1
        clean()
        test(currentTest)
    elif digit == 2 and q_num < q_index:
        q_num += 1
        clean()
        test(currentTest)
    elif digit == 2 and q_num == q_index:
        q_num += 1
        submit()


def test(questions):
    root.geometry('1200x300')

    global questions_page
    global quest
    global alpha
    global beta
    global gamma
    global delta
    global space
    global label
    global prev_btn
    global next_btn
    global nav
    global r
    global var

    questions_page = LabelFrame(content)
    questions_page.grid(row=0, column=0, columnspan=5)

    r = StringVar()
    var = questions[q_num].num
    if var in response:
        r.set(response[var])
    else:
        r.set('aa')

    quest = Label(questions_page, text=questions[q_num].prompt, font=('Times New Roman', 18))
    quest.pack(anchor=W, padx=5)
    alpha = Radiobutton(questions_page, text=questions[q_num].alpha, variable=r, value='a', font=('Default', 13))
    alpha.pack(anchor=W, padx=5)
    beta = Radiobutton(questions_page, text=questions[q_num].beta, variable=r, value='b', font=('Default', 13))
    beta.pack(anchor=W, padx=5)
    gamma = Radiobutton(questions_page, text=questions[q_num].gamma, variable=r, value='c', font=('Default', 13))
    gamma.pack(anchor=W, padx=5)
    delta = Radiobutton(questions_page, text=questions[q_num].delta, variable=r, value='d', font=('Default', 13))
    delta.pack(anchor=W, padx=5)
    space = Label(questions_page, text='')
    space.pack(padx=300)

    prev_btn = Button(nav, text='PREV', command=lambda: buttons(1, r.get()))
    next_btn = Button(nav, text='NEXT', command=lambda: buttons(2, r.get()))
    label = Label(nav, text=f'Question {q_num + 1}/{total}')

    prev_btn.grid(row=2, column=0, pady=5, padx=(27, 200))
    label.grid(row=2, column=2, pady=5)
    next_btn.grid(row=2, column=4, pady=5, padx=(200, 27))


def clean():
    quest.destroy()
    alpha.destroy()
    beta.destroy()
    gamma.destroy()
    delta.destroy()
    label.destroy()
    space.destroy()
    prev_btn.destroy()
    label.destroy()
    next_btn.destroy()


def submit():
    global submit_page
    global q_num
    global pr2
    global questions_page

    next_btn.destroy()
    label.destroy()
    questions_page.destroy()

    submit_page = LabelFrame(content)
    submit_page.grid(row=0, column=0, columnspan=5)

    submit_btn = Button(submit_page, text='SUBMIT', bg='green', fg='white', font=('', 18, 'bold'),
                        command=lambda: results(currentTest))
    submit_btn.pack(anchor=CENTER, pady=52)
    Label(submit_page, text='').pack(padx=300)
    prev_btn.grid(row=2, column=0, pady=5, padx=(27, 540))


def results(questions):
    nav.destroy()
    questions_page.destroy()
    submit_page.destroy()
    result_page = LabelFrame(content)
    result_page.grid(row=0, column=0, columnspan=5)

    scheme = {}
    score = 0
    for question in questions:
        scheme[question.num] = question.ans
    for key in response:
        if response[key] == scheme[key]:
            score += 1
    percent = (score / total) * 100
    percent = round(percent, 1)
    result = Label(result_page, text=f'Score:: {percent}%', font=('Default', 20))
    result.pack(anchor=CENTER, padx=222, pady=65)
    if percent < 50:
        Label(result_page, text='YOU FAILED', font=('Default', 25), fg='red').pack(anchor=CENTER)
    else:
        Label(result_page, text='YOU PASSED', font=('Default', 25), fg='green').pack(anchor=CENTER)


class Admin:
    all = []
    admins = {}
    methods = ['make questions', 'delete all questions', 'make new questions file', 'create new admin', 'log out']
    fileList = ['testQuestions.csv']
    n = 0
    i = 0
    r2 = IntVar()
    call = IntVar()

    def __init__(self, username, password):
        self.username = username
        self.password = password

        Admin.all.append(self)
        Admin.admins[self.username] = password

    @staticmethod
    def callMethods(self):
        for widget in menu.winfo_children():
            widget.destroy()

        Label(menu, text=f"{self.username.upper()}", fg='blue', font=('', 10, 'italic')).pack(pady=(2, 8), anchor=W)

        if len(Admin.fileList) > 1:
            Label(menu, text='Select file to work with', font=('', 15)).pack(pady=(2, 8), anchor=W, padx=10)
            for j in Admin.fileList:
                Radiobutton(menu, text=j, variable=Admin.r2, value=Admin.i, font=('', 13)).pack(anchor=W, padx=20)
                Admin.i += 1

        # print("Below are a list of admin functions!")
        Label(menu, text='Below are a list of admin functions', font=('', 15)).pack(anchor=W, pady=(2, 8))
        ind = 1
        root.geometry('600x350')
        for i in Admin.methods:
            Radiobutton(menu, text=i, variable=Admin.call, value=ind, font=('', 13)).pack(anchor=W, padx=20)
            ind += 1
        Label(menu, text='').pack(padx=225)
        Button(menu, text='SUBMIT', fg='green', font=('', 13, 'bold'), command=lambda: send()).pack(ipadx=100, pady=10)

        def send():
            Admin.n = Admin.r2.get()
            if Admin.call.get() == 1:
                self.__makeQuestion()
            elif Admin.call.get() == 2:
                self.__clear()
            elif Admin.call.get() == 3:
                self.__newfile()
            elif Admin.call.get() == 4:
                self.__makeAdmin()
            elif Admin.call.get() == 5:
                self.logout()

    @staticmethod
    def __makeAdmin():
        for widget in menu.winfo_children():
            widget.destroy()

        Label(menu, text="Enter new admin username", font=('', 13)).pack(anchor=W)
        name = Entry(menu, width=30, font=('', 15))
        name.pack(anchor=W, padx=10, pady=5)
        Label(menu, text="Enter new admin password", font=('', 13)).pack(anchor=W)
        password = Entry(menu, width=30, font=('', 15))
        password.pack(anchor=W, padx=10, pady=5)

        Button(menu, text='SEND', fg='green', font=('', 15, 'bold'), command=lambda: send(name.get(), password.get())).pack(anchor=W, padx=10, pady=4, ipadx=53)
        Button(menu, text='CANCEL', fg='red', font=('', 15, 'bold'), command=lambda: Admin.callMethods(Admin.all[index])).pack(anchor=W, padx=10, ipadx=40)
        Label(menu, text='').pack(padx=225)

        def send(username, passcode):
            new = Admin(username, passcode)
            for widget1 in menu.winfo_children():
                widget1.destroy()
            Label(menu, text="Admin created successfully", font=('', 15), fg='green').pack(anchor=CENTER, pady=50,
                                                                                           padx=10)

            Admin.all.append(new)

    @staticmethod
    def __makeQuestion():
        for widget in menu.winfo_children():
            widget.destroy()
        root.geometry('700x350')

        Label(menu, text='question::', font=('', 14)).grid(row=0, column=0, padx=(5, 0), sticky='W')
        make = Entry(menu, width=50, font=('', 12))
        make.grid(row=0, column=1, padx=(10, 20), sticky='W')
        Label(menu, text='a::', font=('', 14)).grid(row=2, column=0, padx=(5, 0), sticky='W')
        a = Entry(menu, width=30, font=('', 12))
        a.grid(row=2, column=1, padx=(10, 20), sticky='W')
        Label(menu, text='b::', font=('', 14)).grid(row=3, column=0, padx=(5, 0), sticky='W')
        b = Entry(menu, width=30, font=('', 12))
        b.grid(row=3, column=1, padx=(10, 20), sticky='W')
        Label(menu, text='c::', font=('', 14)).grid(row=4, column=0, padx=(5, 0), sticky='W')
        c = Entry(menu, width=30, font=('', 12))
        c.grid(row=4, column=1, padx=(10, 20), sticky='W')
        Label(menu, text='d::', font=('', 14)).grid(row=5, column=0, padx=(5, 0), sticky='W')
        d = Entry(menu, width=30, font=('', 12))
        d.grid(row=5, column=1, padx=(10, 20), sticky='W')

        num = len(currentTest)
        num += 1
        number = f'v{num}'

        Label(menu, text='answer(a/b/c/d)', font=('', 14)).grid(row=6, column=0, padx=(5, 0), sticky='W')
        ans = Entry(menu, width=10, font=('', 12))
        ans.grid(row=6, column=1, padx=(10, 20), sticky='W')

        save = Button(menu, text='SAVE', fg='green', font=('', 12, 'bold'), command=lambda: save())
        save.grid(row=8, column=0, pady=10, padx=10, ipadx=100, columnspan=2, sticky='W')
        stop = Button(menu, text='STOP', fg='red', font=('', 12, 'bold'),
                      command=lambda: Admin.callMethods(Admin.all[index]))
        stop.grid(row=9, column=0, pady=10, padx=10, ipadx=100, columnspan=2, sticky='W')

        def save():
            # append new questions to csv file
            headers = ['numbers', 'questions', 'alpha', 'beta', 'gamma', 'delta', 'answer']
            diction = {'numbers': number, 'questions': str(f'\'{make.get()}?\''), 'alpha': a.get(), 'beta': b.get(),
                       'gamma': c.get(), 'delta': d.get(), 'answer': ans.get()}
            with open(f'{Admin.fileList[Admin.n]}', 'a') as file:
                assign = DictWriter(file, fieldnames=headers)
                assign.writerow(diction)
            make.delete(0, END)
            a.delete(0, END)
            b.delete(0, END)
            c.delete(0, END)
            d.delete(0, END)
            ans.delete(0, END)

    # function to create new questions file
    @staticmethod
    def __newfile():
        for widget in menu.winfo_children():
            widget.destroy()

        Label(menu, text="What would you like to name your file:: ", font=('', 13)).pack(anchor=W)
        name = Entry(menu, width=30, font=('', 15))
        name.pack(anchor=W, padx=10, pady=10)
        Button(menu, text='SEND', fg='green', font=('', 15, 'bold'), command=lambda: send(name.get())).pack(anchor=W, padx=10, pady=10, ipadx=52)
        Button(menu, text='CANCEL', fg='red', font=('', 15, 'bold'), command=lambda: Admin.callMethods(Admin.all[index])).pack(anchor=W, padx=10, ipadx=40)
        Label(menu, text='').pack(padx=225)

        def send(data):
            with open(f'{data}.csv', 'w') as new:
                new.write('')
                for widget1 in menu.winfo_children():
                    widget1.destroy()
                Label(menu, text="file created successfully", font=('', 15), fg='green').pack(anchor=CENTER,
                                                                                              pady=(50, 10), padx=10)
                Button(menu, text='BACK', command=lambda: Admin.callMethods(Admin.all[index])).pack(anchor=W, padx=5,
                                                                                                    pady=(20, 5))
            Admin.fileList.append(f'{data}.csv')

    # function to delete questions
    @staticmethod
    def __clear():
        for widget in menu.winfo_children():
            widget.destroy()

        Button(menu, text='DELETE', fg='red', font=('', 20, 'bold'), command=lambda: send()).pack(anchor=CENTER, ipadx=20, ipady=20)
        Label(menu, text='').pack(padx=225)
        Button(menu, text='CANCEL', fg='red', font=('', 15, 'bold'), command=lambda: Admin.callMethods(Admin.all[index])).pack(anchor=W, padx=10, pady=10, ipadx=40)

        def send():
            confirm = messagebox.askquestion('CONFIRM', "Do you want to clear the contents of this file??")
            if confirm == 'yes':
                with open(f'{Admin.fileList[Admin.n]}', 'w') as cls:
                    cls.write('')
            else:
                Admin.callMethods(Admin.all[index])

    @staticmethod
    def logout():
        for widget in menu.winfo_children():
            widget.destroy()
        login()


Admin('admin', 'password')
login()
root.mainloop()
