from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# creates a random password for the user
def create_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbol = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_number = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_list = password_letter + password_symbol + password_number

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    pyperclip.copy(password)

def save_email():
    try:
        with open("email.txt", "r") as file:


#append the data that was input by the user to json
def save():
    allow_to_add = True
    show_askokcancel_message = True
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    with open("data.json", "r") as file:
        data = json.load(file)
        for i in data:
            if i == website:
                allow_to_add = False
                messagebox.showwarning(title="exiting site", message=f"There is already information saved on the site {website}")
    if password == '' and allow_to_add or website == '' and allow_to_add:
        messagebox.showwarning(title="wrong", message="Please fill all the empty fields.")
    else:
        try:
            with open("data.json", "r") as file:
                pass
        except:
            with open("data.json", "w") as file:
                file.write("{\n}")
            show_askokcancel_message = False
            save()


        if show_askokcancel_message and allow_to_add:
            is_okay = messagebox.askokcancel(title=website, message=f"These are the information:\nEmail: {email}\nPassword: {password}\n Is it okay to save?")
            if is_okay:
                with open("data.json", "r") as file:
                    data = json.load(file)
                    data.update(new_data)

                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
                website_entry.delete(0, "end")
                password_entry.delete(0, "end")

# tries to search the site input to see if there was a match and display email and password
def search():
    try:
        show_multiple_results = True
        with open("data.json", "r") as file:
            results_list = []
            data = json.load(file)
            website = website_entry.get()
            for i in data:
                if website in i:
                    results_list.append(i)
            for i in results_list:
                if i == website:
                    password = data[website]["password"]
                    email = data[website]["email"]
                    messagebox.showinfo(title=website, message=f"Email/Username: {email}\nPassword: {password}")
                    show_multiple_results = False
                    continue
            if len(results_list) > 1 and show_multiple_results:
                messagebox.showerror(title="Multiple results", message=f"There were multiple results\n{results_list}\nPlease search either one of them")
            elif len(results_list) == 0 and show_multiple_results:
                messagebox.showerror(title="No result", message=f'There was no data regarding website with "{website}" in it.')
            else:
                if show_multiple_results:
                    messagebox.showerror(title="No result", message=f"No info regarding {website} has been found.")
    except KeyError:
        messagebox.showerror(title="No result", message=f"No info regarding {website} has been found.")
    except FileNotFoundError:
        messagebox.showerror(title="No data", message=f"you haven't saved any information yet.")



# The UI of the password manager
window = Tk()
window.title("Password Manager")

window.winfo_screenwidth()
window.winfo_screenheight()

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

row0_column0 = Label(width=20, height=14, highlightthickness=0)
row0_column0.grid(row=0, column=0)

row0_column2 = Label(width=20, height=14, highlightthickness=0)
row0_column2.grid(row=0, column=2)

website_text = Label(text="Website:", font=("arial", 12, "bold"))
website_text.grid(row=1, column=0, sticky="e", padx=20, pady=8)

website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, ipadx=26)

email_text = Label(text="Email/Username:", font=("arial", 12, "bold"))
email_text.grid(row=2, column=0, sticky="e", padx=20, pady=8)

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, ipadx=50)
email_entry.insert(0, "email@google.com")

password_text = Label(text="Password:", font=("arial", 12, "bold"))
password_text.grid(row=3, column=0, sticky="e", padx=20, pady=8)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, ipadx=26)

generate_button = Button(text="Generate Password", font=("arial", 10, "bold"), command=create_password)
generate_button.grid(row=3, column=2)

add_button = Button(width=32, text="Add", font=("arial", 10, "bold"), command=save)
add_button.grid(row=4, column=1, columnspan=2, ipadx=50)

search_button = Button(width=17, text="Search", font=("arial", 10, "bold"), command=search)
search_button.grid(row=1, column=2)

window.mainloop()
