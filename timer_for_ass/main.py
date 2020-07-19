from tkinter import *
from tkinter import messagebox
from random import randint
from time import sleep
from os import listdir, path, startfile, system
from webbrowser import open as open_url
from datetime import datetime
import psutil

names = [process.name() for process in psutil.process_iter()]  # All programmes which are opened
duty = dict(physics=7, english=5, olympiad=9, python=10, math=5)
weekdays_duty = [dict(math=2, physics=3), dict(english=2, math=3), dict(olympiad=3, english=1, python=2),
                 dict(olympiad=3, physics=3), dict(english=2, python=2),
                 dict(python=2, olympiad=3),
                 dict(python=4)]
subject_names = dict(GODOT="GODOT", physics="Физики", english="Английского",
                     olympiad="Олимпиадного программирования", python="Python", math="Математики",
                     russian="Русского")


def check_subject():
    """Return subject which i will learn next hour"""
    if "godot.windows.opt.tools.64.exe" in names:
        return "GODOT"

    elif "pycharm64.exe" in names:
        return "python"

    elif "browser.exe" in names:
        print("Выбор предмета на данный час!")
        return question() or check_subject()


def question():
    """Return subject which i choose in tkinter window """
    sub_choice = ''

    def q(subject):
        print(f"Выбран час {subject_names[subject]}\n")
        tp.quit()
        tp.destroy()
        nonlocal sub_choice
        sub_choice = subject

    root = Tk()
    root.withdraw()
    tp = Toplevel()
    tp.attributes("-topmost", True)
    tp.overrideredirect(1)
    m = Button(tp, text="Математика", width=20, command=lambda: q("math"))
    ph = Button(tp, text="Физика", width=20, command=lambda: q("physics"))
    e = Button(tp, text="Английский", width=20, command=lambda: q("english"))
    o = Button(tp, text="Программирование", width=20, command=lambda: q("olympiad"))
    if "math" in weekdays_duty[datetime.today().isoweekday() - 1]: m.pack()
    if "physics" in weekdays_duty[datetime.today().isoweekday() - 1]: ph.pack()
    if "english" in weekdays_duty[datetime.today().isoweekday() - 1]: e.pack()
    if "olympiad" in weekdays_duty[datetime.today().isoweekday() - 1]: o.pack()
    tp.mainloop()
    return sub_choice


def done_hour(subject):
    """Subtracts an hour from the duty and weekdays_duty file"""
    global names
    if subject is None:
        sleep(10)
        done_hour(check_subject())
    try:
        new_weekdays_duty = get_weekdays_duty_file()
        if new_weekdays_duty[datetime.today().isoweekday() - 1][subject] < 1:
            root = Tk()
            root.geometry("0x0")
            root.overrideredirect(1)
            messagebox.showwarning("", f"Ты выполнил все часы {subject_names[subject]} на сегодня!")
            sleep(10)
            names = [process.name() for process in psutil.process_iter()]
            done_hour(check_subject())
        new_weekdays_duty[datetime.today().isoweekday() - 1][subject] -= 1
        rewrite_weekdays_duty(new_weekdays_duty)
    except KeyError:
        root = Tk()
        root.geometry("0x0")
        root.overrideredirect(1)
        messagebox.showwarning("", f"Сегодня ты не должен делать {subject_names[subject]}!")
        sleep(10)
        names = [process.name() for process in psutil.process_iter()]
        done_hour(check_subject())

    new_duty = get_duty_file()
    new_duty[subject] -= 1
    rewrite_duty(new_duty)
    warning(f"Прошел час изучения {subject_names[subject]}")


def warning(text):
    root = Tk()
    root.geometry("0x0")
    root.overrideredirect(1)
    messagebox.showinfo(text, text)
    randint(0, 2) or messagebox.showinfo("Ура", "Ура")


def search_music(fpath):
    music = []
    for f in listdir(fpath):
        if path.isfile(f"{fpath}\{f}"):
            music.append(f"{fpath}\{f}")
        else:
            music.extend(search_music(f"{fpath}\{f}"))
    return music


def get_today_duty():
    return weekdays_duty[datetime.today().isoweekday() - 1]


def rewrite_duty(dictionary=None):
    if dictionary is None:
        dictionary = duty
    with open("duty.txt", "w") as file:
        for key, value in dictionary.items():
            file.write(f"{key} {value} \n")


def rewrite_weekdays_duty(dict_list=None):
    if dict_list is None:
        dict_list = weekdays_duty
    with open("weekdays_duty.txt", "w") as file:
        for d in dict_list:
            for key, value in d.items():
                file.write(f"{key} {value} \n")
            file.write("\n\n\n")


def rewrite_all():
    rewrite_duty()
    rewrite_weekdays_duty()


def get_duty_file():
    lines = {}
    with open("duty.txt", "r") as file:
        for i in range(len(duty)):
            line = file.readline().split()
            lines[line[0]] = int(line[1])
    return lines


def get_weekdays_duty_file():
    lines = {}
    with open("weekdays_duty.txt", "r") as file:
        file_all = file.read().split("\n\n\n")
        for i in range(len(file_all)):
            file_all[i] = file_all[i].split("\n")
            for s in file_all[i]:
                if not s:
                    continue
                s = s.split()
                lines[s[0]] = int(s[1])
            file_all[i] = lines
            lines = {}
    return file_all[:-1]


def main():
    print("Начинается новый час образования!")

    sleep(60)
    s = check_subject()
    sleep(3600)
    done_hour(s)

    names = [process.name() for process in psutil.process_iter()]
    open_url("https://vk.com/audios358433008")
    sleep(600)
    if not "browser.exe" in names: system(
        "taskkill /f /im browser.exe")  # If browser was opened before , do not close it
    startfile("work.mp3")
    sleep(10)
    try:
        system("taskkill /f /im AIMP.exe")
    except:
        pass
    main()


main()
