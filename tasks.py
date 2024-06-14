import tkinter as tk
import tkinter.messagebox
import sqlite3 as sq
import datetime as dd
import tkinter.simpledialog as t

sample = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
          'l',
          'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
          'H',
          'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#',
          '$',
          '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']',
          '^',
          '_', '`', '{', '|', '}', '~', ' ']  # organized characters
key = ['?', '{', 'S', '/', 'n', 'b', 'J', '>', '|', 'r', ',', 'E', 'm', '8', '*', '0', 'Y', 'p', 'H', '%', 'C', '_',
       'w', 'l', 'A', '}', 'e', ')', '.', '5', 's', '#', 'o', 'V', 'I', 'P', '6', '!', 'x', 't', ';', 'M', ']', '=',
       'D', '+', '"', '@', '\\', 'Q', '-', 'u', '2', 'B', "'", 'K', 'R', 'v', 'i', '$', '^', '(', 'z', 'N', 'T',
       '4',
       'f', ' ', 'h', 'U', 'W', '`', 'q', 'Z', 'y', ':', 'k', 'F', '3', '9', 'a', 'G', '1', '~', 'L', '&', '[', 'O',
       'c',
       '7', '<', 'X', 'j', 'g', 'd']  # shuffled

num, task, tdate = [], [], []  # temporary storage for decrypted data


def encrypt(word):  # ecrypting text
    eid = ""
    for i in word:
        ind = sample.index(i)
        eid += key[ind]
    return eid


def decrypt(word):  # decrypting text
    eid = ""
    for i in word:
        ind = key.index(i)
        eid += sample[ind]
    return eid


class Database:  # Class for managing database
    def __init__(self, db):  # Constructor with parameter - connecting and creating database if it does not exist
        self.con = sq.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS TODO(TASK_NUMBER INTEGER PRIMARY KEY AUTOINCREMENT,TASK TEXT, TASK_DATE DATE);")
        self.con.commit()

    def loadTask(self):  # returning all the datas from every domain
        self.cur.execute("SELECT * FROM TODO")
        self.con.commit()
        fetchData = self.cur.fetchall()
        return fetchData

    def addTask(self, work):  # performing Insert query in database
        x = dd.datetime.now()
        datenow = str(x.day) + "|" + str(x.month) + "|" + str(x.year)
        self.cur.execute("INSERT INTO TODO(TASK, TASK_DATE) VALUES(?,?);", [work, encrypt(datenow)])
        self.con.commit()

    def removeTask(self, r):  # performing delete query in database
        self.cur.execute("DELETE FROM TODO WHERE TASK_NUMBER = ?", (r,))
        self.con.commit()

    def godemo(self):  # closing connection
        self.con.close()

    def __delattr__(self):  # Destructor
        self.con.close()


d = Database("todo.db")  # Instance of the class Database


def loadgui():  # Loading the encrypted data in decrytped form along with GUI
    global num, task, tdate
    num.clear()
    task.clear()
    tdate.clear()
    temp = 1
    listbox.delete(0, tk.END)
    fetchData = d.loadTask()
    for i in fetchData:
        num.append(i[0])
        task.append(decrypt(i[1]))
        tdate.append(decrypt(i[2]))
        full = decrypt(i[2]) + "-    " + decrypt(i[1])
        listbox.insert(tk.END, (temp, full))
        temp += 1


def addgui():  # adding the data from entry box Graphically
    work = entry.get()
    if work == "" or work.isspace():
        tk.messagebox.showwarning(title="Warning", message="Enter a task")
        return
    d.addTask(encrypt(work))
    loadgui()
    entry.delete(0, tk.END)


def removegui():  # Removing the selected data from GUI and Database
    try:
        remove = listbox.curselection()
        r = num[listbox.get(remove)[0] - 1]
        d.removeTask(r)
        listbox.delete(remove)
    except Exception as e:
        tk.messagebox.showwarning(title="Warning", message="Select a task")


def updategui():  # Update the selected task
    try:
        update = listbox.curselection()
        u = listbox.get(update)[0]
        d.removeTask(num[u - 1])
        listbox.delete(update)
        entry.insert(0, str(task[u - 1]))
    except Exception as e:
        tk.messagebox.showwarning(title="Warning", message="Select a task")


def godemogui():  # close app
    d.godemo()
    root.destroy()


root = tk.Tk()  # instance of Tkinter
root.minsize(height=500, width=600)

mainpart = tk.Frame(root)  # Common window
mainpart.pack()

midpart = tk.Frame(root)  # space for displaying data and adding scrollbar
midpart.pack()

bottompart = tk.Frame(root)  # space for buttons which perform commands on clicking
bottompart.pack()

root.title("toDO by Bharat")  # titlebar text for GUI window

name = t.askstring(title="Authentication", prompt="Enter Password: ")
if name != "abc123":
    name = t.askstring(title="Access Denied", prompt="Try again: ")
else:
    pass
listbox = tk.Listbox(mainpart, height=15, width=90, bg="#fff680")  # contents space
listbox.grid(row=0, column=0)

loadgui()  # adding data in contents space

entry = tk.Entry(midpart, width=90, border=5, bg="#fff466")  # entry box for typing data
entry.grid(row=1)

scroll = tk.Scrollbar(mainpart)  # to scroll through multiple lines of data
scroll.grid(row=0, column=1)

listbox.config(yscrollcommand=scroll.set)  # connecting scrollbar behaviour with content space
scroll.config(command=listbox.yview)  # configuring scrollbar

add_button = tk.Button(bottompart, text="Add", height=3, width=10, command=addgui, bg="#fff24d")
add_button.grid(row=1, pady=5)

update_button = tk.Button(bottompart, text="Update", height=3, width=10, command=updategui, bg="#fff033")
update_button.grid(row=2, pady=5)

remove_button = tk.Button(bottompart, text="Remove", height=3, width=10, command=removegui, bg="#ffee1a")
remove_button.grid(row=3, pady=5)

add_text = tk.Label(bottompart, text="Add the specified task", height=1, width=0, font=("bold", 15), fg="#ff551a")
add_text.grid(row=1, column=1)

update_text = tk.Label(bottompart, text="Update the selected task", height=6, font=("bold", 15), fg="#ff4200")
update_text.grid(row=2, column=1)

del_text = tk.Label(bottompart, text="Delete the selected task", height=0, font=("bold", 15), fg="#e63b00")
del_text.grid(row=3, column=1)

demo_button = tk.Button(bottompart, text="Exit", height=3, width=10, command=godemogui)
demo_button.grid(row=4)

root.mainloop()
