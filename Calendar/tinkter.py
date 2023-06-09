# Import Required Library
from tkinter import *
from tkcalendar import Calendar
from tkcalendar import DateEntry
from start import main, auth, is_authenticated, deauth, get_token, get_user_profile
import tkinter.messagebox as tmsg
import tkinter as tk


def say_hello(root, message):
    tk.messagebox.showinfo("Info", message)


# Create Object
root = Tk()
# Define Title
root.title('Time Sheet Automation')
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVarAuth = StringVar()

CheckVarAuth.set("Not Authenticated")
auth_label = Label(root, textvariable=CheckVarAuth)
auth_label.pack(pady=5)

# Set geometry

root.geometry("400x500")


def callback(self):
    if is_authenticated():
        token = get_token()
        user_profile = get_user_profile(token)
        print(user_profile)
        print("Authenticated")
        CheckVarAuth.set("Authenticated user is "+user_profile['name'])
    else:
        print("Not Authenticated")
        CheckVarAuth.set("Not Authenticated")

    # only call `callback` the first time `root` becomes visible
    root.unbind('<Visibility>')
def date_entry_selected(event):
    w = event.widget
    date = w.get_date()
    print('Selected Date:{}'.format(date))
    C1.config(text="Synchronise on Date "+str(date))
    # <ref to Calendar>.calevent_create(date, 'Hello ...`)

def date_entry_selected_range_lower(event):
    w = event.widget
    date = w.get_date()
    print('Selected Date:{}'.format(date))
    C2.config(text="Synchronise on Date Range from"+str(date)+" to "+str(cal_range2.get_date()))
    # <ref to Calendar>.calevent_create(date, 'Hello ...`)

def date_entry_selected_range_upper(event):
    w = event.widget
    date = w.get_date()
    print('Selected Date:{}'.format(date))
    C2.config(text="Synchronise on Date Range from"+str(cal_range1.get_date())+" to "+str(date))
    # <ref to Calendar>.calevent_create(date, 'Hello ...`)

# call `callback` whenever `root` becomes visible
root.bind('<Visibility>', callback)
# variable to store the date


def authenticate():
    print("10")
    creds = auth()
    if creds:
        token = get_token()
        user_profile = get_user_profile(token)
        print(user_profile)
        print("Authenticated")
        CheckVarAuth.set("Authenticated user is "+user_profile['name'])


def deauthenticate():
    if deauth():
        CheckVarAuth.set("Not Authenticated")


Button(root, text="Authenticate",
       command=authenticate).pack(pady=5)
Button(root, text="Deauthenticate",
       command=deauthenticate).pack(pady=5)

label1 = Label(root, text="Synchronise from the last Date")
label1.pack(pady=5)
cal_range1 = DateEntry(root, width=12, year=2023, month=4, day=22,
                       background='darkblue', foreground='white', borderwidth=2)
cal_range1.pack(padx=10, pady=10)
cal_range1.bind("<<DateEntrySelected>>", date_entry_selected_range_lower)  # callback
label2 = Label(root, text="Synchronise up to the coming Date")
label2.pack(pady=5)
cal_range2 = DateEntry(root, width=12, year=2023, month=6, day=22,
                       background='darkblue', foreground='white', borderwidth=2)
cal_range2.pack(padx=10, pady=10)
cal_range2.bind("<<DateEntrySelected>>", date_entry_selected_range_upper)  # callback
label3 = Label(root, text="Synchronise of to the Datesync")
label3.pack(pady=5)

cal = DateEntry(root, width=12, year=2023, month=6, day=22,
                background='darkblue', foreground='white', borderwidth=2)
cal.pack(padx=10, pady=10)
cal.bind("<<DateEntrySelected>>", date_entry_selected)  # callback

def grad_date():
    start_date = cal.get_date()
    date_range1 = cal_range1.get_date()
    date_range2 = cal_range2.get_date()
    if CheckVar1.get() == 1:
        # C2.deselect()
        # CheckVar2.set(0)
        print("Synchronise on Date")
        print(start_date)
        main(2, str(start_date))
        date.config(text="Date Sync is :" + str(start_date))
    elif CheckVar2.get() == 1:
        # C1.deselect()
        # CheckVar1.set(0)
        print("Synchronise on Date Range")
        print(date_range1)
        print(date_range2)
        main(3, str(date_range1), str(date_range2))
        date.config(text="Date Sync Range is from" +
                    str(date_range1) + " to " + str(date_range2))
    tmsg.showinfo(
        "CSV Saved", f"CSV File is saved in the SavedCalendar directory")
    print(start_date)
    print(CheckVar1.get())


def _show_value(*pargs):
    print(*pargs)
    print(root.globalgetvar(pargs[0]))


C1 = Checkbutton(root, text="Synchronise on Date "+str(cal.get_date()) , variable=CheckVar1,
                 onvalue=1, offvalue=0, height=1,
                 width=80)
C2 = Checkbutton(root, text="Synchronise on Date Range from"+ str(cal_range1.get_date())+" to "+ str(cal_range2.get_date()), variable=CheckVar2,
                 onvalue=1, offvalue=0, height=1,
                 width=80)
C1.pack()
C2.pack()

# Add Button and Label
Button(root, text="Submit",
       command=grad_date).pack(pady=20)

date = Label(root, text="")
date.pack(pady=20)


# Execute Tkinter
root.mainloop()
