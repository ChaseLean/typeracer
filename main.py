import random
import pygame
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

question = ""
hp = 100
score = 0
level = 1
audio = 1
flag = 1


def ask(op, lower1, upper1, lower2, upper2):
    operators = ['+', '-', '*', '/']

    number_list = []
    if op in [0, 1]:
        for i in range(2):
            number_list.append(str(random.randint(lower1, upper1)))
    elif op == 2:
        for i in range(2):
            number_list.append(str(random.randint(lower2, upper2)))
    else:
        num1 = random.randint(lower2, upper2)
        num2 = random.randint(lower2, upper2)
        product = num1 * num2
        number_list.extend([str(product), str(num1)])

    global question
    question = number_list[0] + " " + operators[op] + " " + number_list[1]


def generate():
    op = score % 4

    if globals()['level'] == 1:
        ask(op, 1, 10, 1, 5)
    elif globals()['level'] == 2:
        ask(op, 5, 20, 5, 10)
    elif globals()['level'] == 3:
        ask(op, 10, 50, 5, 12)


def window():
    def instructions():
        messagebox.showinfo('Instructions',
                            "1. Type the correct answer into the box.\n"
                            "2. The colored bar is your health bar.\n"
                            "3. As time passes, your health bar will decrease.\n"
                            "4. You gain health for a correct answer.\n"
                            "5. You lose health for a wrong answer.\n"
                            "6. When you run out of health, Game Over.\n"
                            "7. See how many points you can score.")

    def give_help():
        messagebox.showinfo('Help',
                            "1. Click the 'Difficulty' button to change the game difficulty.\n"
                            "2. You cannot change the difficulty during a game.\n"
                            "3. The higher your score, the faster your health bar decreases.\n"
                            "4. Easy mode:\n\tAdd/subtract numbers from 1-10\n\tMultiply/divide numbers from 1-5\n"
                            "5. Medium mode:\n\tAdd/subtract numbers from 5-20\n\tMultiply/divide numbers from 5-10\n"
                            "6. Hard mode:\n\tAdd/subtract numbers from 10-30\n\tMultiply/divide numbers from 5-12\n"
                            "7. The questions follow the order +, -, *, /\n"
                             "8. The answers to some questions can be negative.")

    def change(light):
        if light == 1:
            answer_entry.configure(background='#AAFFAA')
        else:
            answer_entry.configure(background='#FFAAAA')

        root.after(300, change_back)

    def change_back():
        answer_entry.configure(background='#FFFFFF')

    def change_level():
        global level, score

        if score != 0 or hp < 100:
            return

        level_dict = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
        if level < 3:
            level += 1
        else:
            level = 1
        generate()
        question_var.set(question)
        difficulty.set(level_dict[level])

        if level == 1:
            s.configure("red.Horizontal.TProgressbar", troughcolor='#444444', bordercolor='#444444',
                        lightcolor='#33AE6B', darkcolor='#33AE6B', background='#33AE6B')
        if level == 2:
            s.configure("red.Horizontal.TProgressbar", troughcolor='#444444', bordercolor='#444444',
                        lightcolor='#FCAE1E', darkcolor='#FCAE1E', background='#FCAE1E')
        if level == 3:
            s.configure("red.Horizontal.TProgressbar", troughcolor='#444444', bordercolor='#444444',
                        lightcolor='red', darkcolor='red', background='red')
        root.update()

    def stop_audio():
        global audio
        if audio == 1:
            audio = 0
            music.stop()
        else:
            audio = 1
            music.play(-1)

    def bar():
        global hp, score
        if hp <= 0:
            return
        if score == 0:
            hp -= 0.05
        else:
            hp -= 0.05 * (score ** (1/4))

        if hp > 0:
            progress['value'] = hp
            root.after(10, bar)
            root.update()
        check()

    def check():
        global hp, score, flag
        if hp <= 0:
            hp = 100
            game_over_sound.play()
            messagebox.showinfo("Game Over", f"Oops. You ran out of health!\nYour final score was {score}")
            prev_score_var.set("{0:02d}".format(score))
            if score > int(high_score_var.get()):
                high_score_var.set("{0:02d}".format(score))
            score = 0
            flag = 1
            progress['value'] = hp
            score_var.set("{0:02d}".format(score))
            user_input.set("")
            if audio == 1:
                music.stop()
                music.play(-1)

    def submit(*args):
        music.stop()
        global question, hp, score, flag
        if flag == 1:
            bar()
            flag = 0
        user_answer = float(answer_entry.get())
        answer = float(eval(question))

        user_input.set("")

        if user_answer == answer:
            change(1)
            score += 1
            if hp < 100:
                hp += 10
            if audio == 1:
                if score % 5 != 0:
                    correct_sound1.play()
                else:
                    correct_sound2.play()
        else:
            change(0)
            if score != 0:
                hp -= 10
            if audio == 1:
                wrong_sound1.play()

        generate()
        question_var.set(question)
        score_var.set("{0:02d}".format(score))

        root.update()

    root = Tk()
    root.geometry("450x300")
    root.title("Calculator")
    root.attributes("-topmost", True)

    pygame.mixer.init()
    music = pygame.mixer.Sound("Sound effects/start_sound.wav")
    correct_sound1 = pygame.mixer.Sound("Sound effects/correct_sound1.wav")
    correct_sound2 = pygame.mixer.Sound("Sound effects/correct_sound2.wav")
    wrong_sound1 = pygame.mixer.Sound("Sound effects/wrong_sound1.wav")
    game_over_sound = pygame.mixer.Sound("Sound effects/game_over_sound.wav")
    music.play(-1)

    user_input = StringVar()
    generate()

    global question, score
    question_var = StringVar()
    score_var = StringVar()
    prev_score_var = StringVar()
    high_score_var = StringVar()
    difficulty = StringVar()
    question_var.set(question)
    score_var.set("{0:02d}".format(score))
    prev_score_var.set("{0:02d}".format(score))
    high_score_var.set("{0:02d}".format(score))
    difficulty.set("Easy")

    title = Label(root, text="MathRacer", font=('Arial', 30, ''))
    score_display = Label(root, text="Current score : ", font=('Arial', 14, ''))
    score_label = Label(root, textvariable=score_var, font=('Arial', 14, ''))
    difficulty_display = Label(root, text="Difficulty : ", font=('Arial', 14, ''))
    difficulty_label = Label(root, textvariable=difficulty, font=('Arial', 14, ''))

    button1 = Button(root, width=10, font=("Arial", 14, ""), text="Instructions", borderwidth=1, command=instructions)
    button2 = Button(root, width=10, font=("Arial", 14, ""), text="Difficulty", borderwidth=1, command=change_level)
    button3 = Button(root, width=5, font=("Arial", 12, ""), text="Help", borderwidth=1, command=give_help)
    button4 = Button(root, width=5, font=("Arial", 12, ""), text="Audio", borderwidth=1, command=stop_audio)

    instructions_label = Label(root, text="Answer the following question:", font=('Arial', 14, ''))
    question_label = Label(root, textvariable=question_var, font=('Arial', 24, ''))
    equals_label = Label(root, text=" = ", font=('Arial', 24, ''))
    answer_entry = Entry(root, textvariable=user_input, font=('Arial', 24, 'normal'), width=10)
    answer_entry.bind("<Return>", submit)

    prev_label = Label(root, text="Previous:\tHigh:", font=('Arial', 8, 'bold'))
    prev_score_label = Label(root, textvariable=prev_score_var, font=('Arial', 8, 'bold'))
    high_score_label = Label(root, textvariable=high_score_var, font=('Arial', 8, 'bold'))
    credit_label = Label(root, text="MathRacer Version 1.1 by ChaseLean 8/8/2021", font=('Arial', 8, ''))

    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", troughcolor='#444444', bordercolor='#444444', lightcolor='#33AE6B',
                darkcolor='#33AE6B', background='#33AE6B')

    progress = ttk.Progressbar(root, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=390,
                               mode='determinate')
    progress['value'] = 100

    title.place(x=30, y=10)
    difficulty_display.place(x=30, y=70)
    difficulty_label.place(x=120, y=70)
    score_display.place(x=30, y=95)
    score_label.place(x=160, y=95)
    prev_label.place(x=30, y=122)
    prev_score_label.place(x=85, y=122)
    high_score_label.place(x=158, y=122)

    button1.place(x=300, y=20)
    button2.place(x=300, y=70)
    button3.place(x=365, y=120)
    button4.place(x=300, y=120)

    instructions_label.place(x=30, y=150)
    question_label.place(x=30, y=190)
    equals_label.place(x=180, y=190)
    answer_entry.place(x=230, y=190)

    progress.place(x=30, y=250)
    credit_label.place(x=180, y=280)

    root.mainloop()


window()
