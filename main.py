import customtkinter as ct
from tkinter import *
import csv
from csv import *

# from questionsList import *

root = ct.CTk()


def login():
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry('300x300')
    root.title('LOGIN')

    frame = ct.CTkFrame(root)
    frame.pack(padx=5, pady=5, fill='both', expand=True)

    ct.CTkLabel(frame, text='LOGIN PAGE', font=('Times New Roman', 30, 'bold'), text_color='#2266bb').pack(pady=20)

    username_box = ct.CTkEntry(frame, placeholder_text='USERNAME', font=('', 15), text_color='#222222')
    password_box = ct.CTkEntry(frame, placeholder_text='PASSWORD', show='*', font=('', 15), text_color='#222222')
    check_box = ct.CTkCheckBox(frame, checkbox_width=17, checkbox_height=17, text='login as admin', border_color='#2266bb', checkmark_color='#2266ee')
    submit_btn = ct.CTkButton(frame, text='LOGIN', command=lambda: validate(username_box.get().upper(), check_box.get()),
                              font=('', 15), fg_color='#2266bb', hover_color='#2266ee')

    username_box.pack(anchor=W, padx=10, pady=10, ipadx=60)
    password_box.pack(anchor=W, padx=10, pady=10, ipadx=60)
    check_box.pack(anchor=W, padx=13)
    submit_btn.pack(anchor=W, padx=10, pady=10, ipadx=60)


def validate(nick, check):
    if nick == '':
        nick = 'DANGWAM BENJAMIN'
    if check == 0:
        Student(nick)
    else:
        Administrator(nick)


# ------------------------------------------------------------------------------------------------
# student dashboard
class Student:
    def __init__(self, nick):
        for widget in root.winfo_children():
            widget.destroy()
        super().__init__()

        width = 1100
        height = 500
        self.nick = nick
        self.q_num = 0
        self.response = {}

        root.geometry(f'{width}x{height}')
        root.title('TEST')
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(1, weight=1)

        self.side_frame = ct.CTkFrame(root, width=int(width * 0.3), corner_radius=0)
        self.side_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.title_frame = ct.CTkFrame(root, width=int(width * 0.7), height=80, corner_radius=0)
        self.title_frame.grid(row=0, column=1, sticky='nsew')
        self.main_frame = ct.CTkFrame(root, width=int(width * 0.7), fg_color='transparent')
        self.main_frame.grid(row=1, column=1, sticky='nsew')
        self.main_frame.columnconfigure(0, weight=1)

        # start sidebar
        name = ct.CTkLabel(self.side_frame, text=f'{self.nick}', font=('', 20, 'bold'))
        name.grid(row=0, column=0, padx=25, pady=(25, 0))
        ct.CTkLabel(self.side_frame, text='(Student)', font=('', 10)).grid(row=1, column=0, pady=(0, 50))

        profile_btn = ct.CTkButton(self.side_frame, text='Profile', font=('', 15), command=self.profile, fg_color='#2266bb', hover_color='#2266ee')
        profile_btn.grid(row=2, column=0, pady=5)
        test_btn = ct.CTkButton(self.side_frame, text='Test', font=('', 15), command=self.show_test, fg_color='#2266bb', hover_color='#2266ee')
        test_btn.grid(row=3, column=0, pady=5)
        self.side_frame.rowconfigure(4, weight=1)
        ct.CTkSwitch(self.side_frame, text='Toggle Appearance', font=('', 15, 'bold'), progress_color='#2266bb', command=change_mode).grid(row=5,
                                                                                                                                           column=0,
                                                                                                                                           pady=10,
                                                                                                                                           padx=20)
        logout_btn = ct.CTkButton(self.side_frame, text='Log Out', font=('', 15), command=login, fg_color='#bb2222', hover_color='#ee2222')
        logout_btn.grid(row=6, column=0, pady=(10, 35))
        # end sidebar

        # start title frame
        ct.CTkLabel(self.title_frame, text='STUDENT\'S PAGE', font=('', 35, 'bold'), text_color='#2266bb').pack(pady=15)
        # end title frame

        # initialisations
        self.question_frame = None
        self.options_frame = None
        self.nav_frame = None
        self.submit_frame = None
        self.var = None
        self.prev_btn = None
        self.next_btn = None
        self.label = None

    def profile(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

        self.main_frame.rowconfigure(1, weight=0)
        self.main_frame.rowconfigure(0, weight=1)

        profile_frame = ct.CTkFrame(self.main_frame)
        profile_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        ct.CTkLabel(profile_frame, text='UPDATE PROFILE', font=('', 35, 'bold')).pack(pady=100)

    def show_test(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

        self.main_frame.rowconfigure(1, weight=0)
        self.main_frame.rowconfigure(0, weight=1)

        test_frame = ct.CTkFrame(self.main_frame)
        test_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        ct.CTkButton(test_frame, text='TAKE TEST', font=('', 35, 'bold'), command=lambda: self.test(convert()), fg_color='#2266bb',
                     hover_color='#2266ee').pack(pady=100)

    def buttons(self, digit, data):
        q_index = total - 1
        self.response[self.var] = data

        if digit == 0 and self.q_num > 0:
            if self.q_num == total:
                self.submit_frame.destroy()
            self.q_num -= 1
            self.test(convert())
        elif digit == 1 and self.q_num < q_index:
            self.q_num += 1
            self.test(convert())
        elif digit == 1 and self.q_num == q_index:
            self.q_num += 1
            self.submit()

    def test(self, questions):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

        # make row 0 non-responsive and row 1 responsive
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

        # start main frame
        self.question_frame = ct.CTkFrame(self.main_frame)
        self.question_frame.grid(row=0, column=0, padx=5, pady=(5, 1), sticky='nsew')

        self.options_frame = ct.CTkFrame(self.main_frame)
        self.options_frame.grid(row=1, column=0, padx=5, pady=(1, 1), sticky='nsew')

        self.nav_frame = ct.CTkFrame(self.main_frame)
        self.nav_frame.grid(row=2, column=0, padx=5, pady=(1, 5), sticky='nsew')
        self.nav_frame.columnconfigure((0, 1, 2), weight=1)

        # if an option has been selected, shade the selected box else shade none
        r = StringVar()
        self.var = questions[self.q_num].num  # use the question numbers as the variable to store the selected choice
        if self.var in self.response:  # self.var saves the selected option within the response dictionary
            r.set(self.response[self.var])
        else:
            r.set('aa')  # (i.e since 'aa' is an invalid choice)

        # question
        quest = ct.CTkLabel(self.question_frame, text=questions[self.q_num].prompt, font=('Times New Roman', 30, 'bold'))
        quest.pack(pady=15)

        # options
        alpha = ct.CTkRadioButton(self.options_frame, text=questions[self.q_num].alpha, variable=r, value='a', font=('Default', 25), radiobutton_height=25,
                                  radiobutton_width=25,
                                  fg_color='#2266bb', border_width_checked=10)
        alpha.grid(row=0, column=0, padx=20, pady=(20, 10))
        beta = ct.CTkRadioButton(self.options_frame, text=questions[self.q_num].beta, variable=r, value='b', font=('Default', 25), radiobutton_height=25,
                                 radiobutton_width=25,
                                 fg_color='#2266bb', border_width_checked=10)
        beta.grid(row=1, column=0, padx=20, pady=10)
        gamma = ct.CTkRadioButton(self.options_frame, text=questions[self.q_num].gamma, variable=r, value='c', font=('Default', 25), radiobutton_height=25,
                                  radiobutton_width=25,
                                  fg_color='#2266bb', border_width_checked=10)
        gamma.grid(row=2, column=0, padx=20, pady=10)
        delta = ct.CTkRadioButton(self.options_frame, text=questions[self.q_num].delta, variable=r, value='d', font=('Default', 25), radiobutton_height=25,
                                  radiobutton_width=25,
                                  fg_color='#2266bb', border_width_checked=10)
        delta.grid(row=3, column=0, padx=20, pady=(10, 15))

        # buttons
        self.prev_btn = ct.CTkButton(self.nav_frame, text='PREV', fg_color='#2266bb', hover_color='#2266ee', command=lambda: self.buttons(0, r.get()))
        self.prev_btn.grid(row=1, column=0, pady=8)
        self.label = ct.CTkLabel(self.nav_frame, text=f'Question {self.q_num + 1}/{total}', font=('', 15, 'bold'))
        self.label.grid(row=1, column=1, pady=8)
        self.next_btn = ct.CTkButton(self.nav_frame, text='NEXT', fg_color='#2266bb', hover_color='#2266ee', command=lambda: self.buttons(1, r.get()))
        self.next_btn.grid(row=1, column=2, pady=8)

    def submit(self):
        self.question_frame.destroy()
        self.options_frame.destroy()
        self.next_btn.destroy()
        self.label.destroy()

        self.submit_frame = ct.CTkFrame(self.main_frame)
        self.submit_frame.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky='nsew')
        ct.CTkButton(self.submit_frame, text='SUBMIT TEST', font=('', 35, 'bold'), command=lambda: self.results(convert()), fg_color='#22bb22',
                     hover_color='#22ee22').pack(pady=100)

    def results(self, questions):
        self.submit_frame.destroy()
        self.nav_frame.destroy()

        result_frame = ct.CTkFrame(self.main_frame)
        result_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        scheme = {}
        score = 0
        for data in questions:
            scheme[data.num] = data.ans
        for key in self.response:
            if self.response[key] == scheme[key]:
                score += 1
        percent = (score / total) * 100
        percent = round(percent, 1)
        ct.CTkLabel(result_frame, text=f'Score:: {percent}%', font=('', 30)).grid(row=0, column=0, pady=65, sticky='nsew')
        if percent < 50:
            ct.CTkLabel(result_frame, text='YOU FAILED', font=('', 45, 'bold'), text_color='#dd4242').grid(row=1, column=0, pady=80, sticky='nsew')
        else:
            ct.CTkLabel(result_frame, text='YOU PASSED', font=('', 45, 'bold'), text_color='#42dd42').grid(row=1, column=0, pady=5, sticky='nsew')
        # end main frame

# ---------------------------------------------------------------------------------------------------------------
# end of student dashboard


# -----------------------------------------------------------------------------------------------------------------
# admin dashboard
class Administrator:
    def __init__(self, nick):
        super().__init__()
        for widget in root.winfo_children():
            widget.destroy()

        width = 1100
        height = 500
        self.nick = nick

        root.geometry(f'{width}x{height}')
        root.title('DASHBOARD')
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(1, weight=1)

        self.side_frame = ct.CTkFrame(root, width=int(width * 0.3), corner_radius=0)
        self.side_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.title_frame = ct.CTkFrame(root, width=int(width * 0.7), height=80, corner_radius=0)
        self.title_frame.grid(row=0, column=1, sticky='nsew')
        self.main_frame = ct.CTkFrame(root, width=int(width * 0.7), fg_color='transparent')
        self.main_frame.grid(row=1, column=1, sticky='nsew')
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # start sidebar
        name = ct.CTkLabel(self.side_frame, text=f'{self.nick}', font=('', 20, 'bold'))
        name.grid(row=0, column=0, padx=25, pady=(25, 0))
        ct.CTkLabel(self.side_frame, text='(Administrator)', font=('', 10)).grid(row=1, column=0, pady=(0, 50))

        profile2_btn = ct.CTkButton(self.side_frame, text='Profile', font=('', 15), command=self.profile, fg_color='#2266bb', hover_color='#2266ee')
        profile2_btn.grid(row=2, column=0, pady=5)
        question_btn = ct.CTkButton(self.side_frame, text='Set Questions', font=('', 15), command=self.set_questions, fg_color='#2266bb',
                                    hover_color='#2266ee')
        question_btn.grid(row=3, column=0, pady=5)
        result_btn = ct.CTkButton(self.side_frame, text='View Student Results', font=('', 15), command=self.view_results, fg_color='#2266bb',
                                  hover_color='#2266ee')
        result_btn.grid(row=4, column=0, pady=5)
        self.side_frame.rowconfigure(5, weight=1)
        ct.CTkSwitch(self.side_frame, text='Toggle Appearance', font=('', 15, 'bold'), progress_color='#2266bb', command=change_mode).grid(row=6,
                                                                                                                                           column=0,
                                                                                                                                           pady=10,
                                                                                                                                           padx=20)
        logout_btn = ct.CTkButton(self.side_frame, text='Log Out', font=('', 15), command=login, fg_color='#bb2222', hover_color='#ee2222')
        logout_btn.grid(row=7, column=0, pady=(10, 35))
        # end sidebar

        # start title frame
        ct.CTkLabel(self.title_frame, text='ADMINISTRATOR\'S PAGE', font=('', 35, 'bold'), text_color='#2266bb').pack(pady=15)
        # end title frame

        # initialisations
        self.question_frame = None
        self.question = None
        self.option_a = None
        self.option_b = None
        self.option_c = None
        self.option_d = None
        self.answer = None

    def profile(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

        profile_frame = ct.CTkFrame(self.main_frame)
        profile_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        ct.CTkLabel(profile_frame, text='UPDATE PROFILE', font=('', 35, 'bold')).pack(pady=100)

    def set_questions(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

        self.question_frame = ct.CTkFrame(self.main_frame)
        self.question_frame.grid(row=0, column=0, padx=5, pady=(5, 1), sticky='nsew')

        ct.CTkLabel(self.question_frame, text='QUESTION:', font=('', 25, 'bold')).grid(row=0, column=0, sticky='w', pady=10, padx=20)
        self.question = ct.CTkTextbox(self.question_frame, font=('Times New Roman', 25), height=80, width=630)
        self.question.grid(row=0, column=1, sticky='nsew', pady=10, padx=10, ipady=5)

        ct.CTkLabel(self.question_frame, text='OPTION A:', font=('', 25, 'bold')).grid(row=1, column=0, sticky='w', pady=7, padx=20)
        self.option_a = ct.CTkEntry(self.question_frame, font=('Times New Roman', 20), placeholder_text='a', border_width=0)
        self.option_a.grid(row=1, column=1, padx=10, pady=7, ipady=5, sticky='nsew')
        ct.CTkLabel(self.question_frame, text='OPTION B:', font=('', 25, 'bold')).grid(row=2, column=0, sticky='w', pady=7, padx=20)
        self.option_b = ct.CTkEntry(self.question_frame, font=('Times New Roman', 20), placeholder_text='b', border_width=0)
        self.option_b.grid(row=2, column=1, padx=10, pady=7, ipady=5, sticky='nsew')
        ct.CTkLabel(self.question_frame, text='OPTION C:', font=('', 25, 'bold')).grid(row=3, column=0, sticky='w', pady=7, padx=20)
        self.option_c = ct.CTkEntry(self.question_frame, font=('Times New Roman', 20), placeholder_text='c', border_width=0)
        self.option_c.grid(row=3, column=1, padx=10, pady=7, ipady=5, sticky='nsew')
        ct.CTkLabel(self.question_frame, text='OPTION D:', font=('', 25, 'bold')).grid(row=4, column=0, sticky='w', pady=7, padx=20)
        self.option_d = ct.CTkEntry(self.question_frame, font=('Times New Roman', 20), placeholder_text='d', border_width=0)
        self.option_d.grid(row=4, column=1, padx=10, pady=7, ipady=5, sticky='nsew')
        ct.CTkLabel(self.question_frame, text='ANSWER:', font=('', 25, 'bold')).grid(row=5, column=0, sticky='w', pady=7, padx=20)
        self.answer = ct.CTkEntry(self.question_frame, font=('Times New Roman', 20), placeholder_text='a or b or c or d', border_width=0)
        self.answer.grid(row=5, column=1, padx=10, pady=7, ipady=5, sticky='nsew')

        # buttons
        nav_frame2 = ct.CTkFrame(self.main_frame)
        nav_frame2.grid(row=2, column=0, padx=5, pady=(1, 5), sticky='nsew')
        nav_frame2.columnconfigure((0, 1, 2), weight=1)

        prev_btn = ct.CTkButton(nav_frame2, text='PREV', fg_color='#2266bb', hover_color='#2266ee')
        prev_btn.grid(row=1, column=0, pady=8)
        next_btn = ct.CTkButton(nav_frame2, text='NEXT', command=self.save, fg_color='#2266bb', hover_color='#2266ee')
        next_btn.grid(row=1, column=2, pady=8)

    def save(self):
        global total
        num = len(convert())
        num += 1
        number = f'v{num}'

        # append new questions to csv file
        headers = ['numbers', 'questions', 'alpha', 'beta', 'gamma', 'delta', 'answer']
        diction = {'numbers': number, 'questions': str(f"{self.question.get(1.0, 'end-1c')}?"), 'alpha': self.option_a.get(),
                   'beta': self.option_b.get(),
                   'gamma': self.option_c.get(), 'delta': self.option_d.get(), 'answer': self.answer.get()}
        with open('testQuestions.csv', 'a') as file:
            assign = DictWriter(file, fieldnames=headers)
            assign.writerow(diction)
            print(diction)
            total += 1
        self.question.delete(1.0, 'end')
        self.option_a.delete(0, END)
        self.option_b.delete(0, END)
        self.option_c.delete(0, END)
        self.option_d.delete(0, END)
        self.answer.delete(0, END)
        # end main frame

    def view_results(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

        profile_frame = ct.CTkFrame(self.main_frame)
        profile_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        ct.CTkLabel(profile_frame, text='NO CURRENT RESULTS', font=('', 35, 'bold')).pack(pady=100)

# ----------------------------------------------------------------------------------------------------------
# end of admin dashboard


def change_mode():
    mode = ct.get_appearance_mode()
    if mode == 'Light':
        ct.set_appearance_mode('dark')
    else:
        ct.set_appearance_mode('light')


# class to assign questions to answers
class Question:
    def __init__(self, num, prompt, alpha1, beta1, gamma1, delta1, ans):
        self.num = num
        self.prompt = prompt
        self.alpha = alpha1
        self.beta = beta1
        self.gamma = gamma1
        self.delta = delta1
        self.ans = ans


def convert():
    # convert questions in csv file to array
    with open(f'testQuestions.csv', 'r') as f:
        Reader = csv.DictReader(f)
        items = list(Reader)

    questionsList = []
    for item in items:
        n = item.get('number')
        q = item.get('questions')
        al = item.get('alpha')
        be = item.get('beta')
        ga = item.get('gamma')
        de = item.get('delta')
        ar = item.get('answer')

        questionsList.append([n, q, al, be, ga, de, ar])

    testQuestions = [
        Question(questionsList[n][0], questionsList[n][1], questionsList[n][2], questionsList[n][3], questionsList[n][4], questionsList[n][5], questionsList[n][6])
        for n in range(0, len(questionsList))
    ]
    return testQuestions


total = len(convert())

login()
root.mainloop()
