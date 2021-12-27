from tkinter import *
from PIL import ImageTk, Image
root = Tk()
root.title('Codemy.com - Learn To Code!')
# root.iconbitmap('c:/gui/codemy.ico')
root.geometry("400x400")

my_menu = Menu(root)
root.config(menu=my_menu)

# click command
def our_command():
	my_label = Label(root, text="You Clicked a Dropdown Menu!").pack()

# File New Function
def file_new():
	hide_all_frames()
	file_new_frame.pack(fill="both", expand=1)
	my_label = Label(file_new_frame, text="You Clicked the File >> New Menu!").pack()

# Edit Cut
def edit_cut():
	hide_all_frames()
	edit_cut_frame.pack(fill="both", expand=1)
	my_label = Label(edit_cut_frame, text="You Clicked the Edit >> Cut Menu!").pack()

# Hide all frames
def hide_all_frames():
	file_new_frame.pack_forget()
	edit_cut_frame.pack_forget()

#Create a menu item

file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New...", command=file_new)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create an edit menu item
edit_menu = Menu(my_menu)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=edit_cut)
edit_menu.add_command(label="Copy", command=our_command)

#Create an Options menu item
option_menu = Menu(my_menu)
my_menu.add_cascade(label="Options", menu=option_menu)
option_menu.add_command(label="Find", command=our_command)
option_menu.add_command(label="Find Next", command=our_command)

# Create some frames
file_new_frame = Frame(root, width=400, height=400, bg="red")
edit_cut_frame = Frame(root, width=400, height=400, bg="blue")


# root = Tk()
# root.title("BO project")
#
# frame_add = LabelFrame(root, text = "Edytuj bazy", padx=20, pady=50)
# frame_add.pack(padx=10, pady= 0)
#
# frame_option = LabelFrame(root, text = "Ustawienia", padx= 20, pady= 50)
# frame_option.pack(padx=0, pady= 1)

# e = Entry(root, width = 30)
# e.pack()
# e.insert(0, "XD na zawsze:")
#
# size = 128, 128

# my_img = ImageTk.PhotoImage(Image.open("kxd.jpg"))
# my_label = Label(image = my_img)
# my_label.pack()


# def JD():
#     h = "" + e.get()
#     myLabel = Label(root, text = h).pack()
# myLabel2 = Label(root, text = "JD").grid()
# #
# b = Button(frame_add, text = 'Dodaj danie').grid(row = 0, column = 0)
# b1 = Button(frame_add, text = 'Dodaj produkt do lodówki').grid(row = 1, column = 0)
# b2 = Button(frame_add, text = 'Dodaj produkt do sklepu').grid(row = 2, column = 0)
#
# c = Button(frame_option, text = 'Dodaj danie').grid(row = 0, column = 0)





root.mainloop()