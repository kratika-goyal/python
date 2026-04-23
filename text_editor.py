import tkinter as tk
from tkinter import filedialog,messagebox
from tkinter import colorchooser

root=tk.Tk()
root.title("My Text Editor")
root.geometry("500x500")

font_family=tk.StringVar()
font_size=tk.IntVar()
font_family.set("Times New Roman")
font_size.set(14)


text = tk.Text(
    root,
    wrap=tk.WORD,
    font=(font_family.get(), font_size.get())
)

#save
def confirm_save():
    if is_modified:
        response = messagebox.askyesnocancel("Save", "Do you want to save changes?")
        
        if response == True:
            save_file()
            return True
        
        elif response == False:
            return True
        
        else:
            return False
    return True

#new file
def new_file():
     global is_modified

     if confirm_save():
         text.delete(1.0,tk.END)
         is_modified=False

#open a new file
def open_file():
    #dialog
    file_path=filedialog.askopenfilename(
      defaultextension=".txt" ,
      filetypes=[("text files","*.txt")] 
    )

    if file_path:
        #open file
        with open(file_path,"r")as file:
            text.delete(1.0,tk.END)
            text.insert(tk.END,file.read())

#save file
def save_file():
    global is_modified
    #dialog
    file_path=filedialog.asksaveasfilename(
        defaultextension=".txt" ,
      filetypes=[("text files","*.txt")] 
    )

    if file_path:
        with open(file_path,"w") as file:
            file.write(text.get(1.0,tk.END))
    
    messagebox.showinfo("Info","file saved successfully")
    is_modified=False

# exit
def exit_file():
    root.destroy()

#bg color

def bg_color():
    color=colorchooser.askcolor()[1]

    if color:
        text.config(bg=color)

#text color

def text_color():
    color=colorchooser.askcolor()[1]

    if color:
        text.config(fg=color)

is_dark=False

def dark_mode():
    global is_dark

    if is_dark==False:
         root.config(bg="black")
         text.config(bg="black",fg="white",insertbackground="white")
         is_dark=True

         menu.entryconfig("Dark Mode",label="Light Mode")
    else:
         root.config(bg="white")
         text.config(bg="white",fg="black",insertbackground="black")
         is_dark=False

         menu.entryconfig("Light Mode",label="Dark Mode")


def font_update(*args):
    text.config(font=(font_family.get(),font_size.get()))

fonts = [
    "Times New Roman",
    "Arial",
    "Calibri",
    "Courier",
    "Helvetica",
    "Verdana",
    "Comic Sans MS"
]
sizes = [8, 10, 12, 14, 16, 18, 20, 24, 28, 32]

is_modified=False

def text_change(event):
    global is_modified
    is_modified=True

    text.edit_modified(False)

text.bind("<<Modified>>",text_change)

def on_closing():
     if confirm_save():
         root.destroy()
#menu

menu=tk.Menu(root)
root.config(menu=menu)

format_menu=tk.Menu(menu,tearoff=0)
file_menu=tk.Menu(menu)

#functions

menu.add_cascade(label="File",menu=file_menu)
menu.add_cascade(label="Format",menu=format_menu)
menu.add_command(label="Dark Mode",command=dark_mode)

file_menu.add_command(label="New",command=new_file)
file_menu.add_command(label="Open",command=open_file)
file_menu.add_command(label="Save",command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=exit_file)

format_menu.add_command(label="Background Color", command=bg_color)
format_menu.add_command(label="Text Color", command=text_color)

toolbar = tk.Frame(root)
toolbar.pack(fill="x")

font_menu = tk.OptionMenu(toolbar, font_family, *fonts, command=font_update)
font_menu.pack(side="left", padx=5, pady=5)

size_menu = tk.OptionMenu(toolbar, font_size, *sizes, command=font_update)
size_menu.pack(side="left", padx=5, pady=5)

text.pack(expand=True,fill=tk.BOTH)
root.protocol("WM_DELETE_WINDOW",on_closing)

root.mainloop()