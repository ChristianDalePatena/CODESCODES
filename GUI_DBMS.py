import tkinter
import pyodbc
from tkinter import *
from tkinter import messagebox, ttk
import customtkinter as ctk
from FUNCTION import *
from customtkinter import set_appearance_mode, set_default_color_theme

# Set appearance and theme
set_appearance_mode("System")  # Options: "Light", "Dark", "System"
set_default_color_theme("blue")  # Still required for button colors

# Color Constants
THEME_COLOR = "#26547C"
ACCENT_COLOR = "white"
FONT_COLOR = "#4A90E2"
PLACEHOLDER_COLOR = "#A9A9A9"
FONT_SIZE = 12

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Farmers Cubao")
        self.geometry("800x550")
        self.configure(fg_color=THEME_COLOR)
        self.resizable(False, False)
        self.init_ui()

    def init_ui(self):
        # Image Label (Placeholder)
        self.image_label = ctk.CTkLabel(self, text="[Image Not Found]",
                                        fg_color="transparent",
                                        text_color=ACCENT_COLOR,
                                        font=("Arial", 16, "bold"))
        self.image_label.place(x=330, y=150)

        # Username Entry
        self.user_id_input = ctk.CTkEntry(self, font=("Arial", 14), width=200, height=30, text_color="black")
        self.user_id_input.insert(0, "Please enter your username")
        self.user_id_input.place(x=300, y=250)
        self.user_id_input.bind("<FocusIn>", self.clear_placeholder_username)
        self.user_id_input.bind("<FocusOut>", self.add_placeholder_username)

        # Password Entry
        self.password_input = ctk.CTkEntry(self, font=("Arial", 14), width=200, height=30, text_color="black")
        self.password_input.insert(0, "Please enter your password")
        self.password_input.place(x=300, y=300)
        self.password_input.bind("<FocusIn>", self.clear_placeholder_password)
        self.password_input.bind("<FocusOut>", self.add_placeholder_password)

        # Login Button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_function,
                                          fg_color=ACCENT_COLOR, text_color=FONT_COLOR,
                                          font=("Arial", 14), width=105, height=40)
        self.login_button.place(x=290, y=350)

        # Sign Up Button
        self.signup_button = ctk.CTkButton(self, text="Sign Up", command=lambda: SignUpWindow(self),
                                           fg_color=ACCENT_COLOR, text_color=FONT_COLOR,
                                           font=("Arial", 14), width=105, height=40)
        self.signup_button.place(x=410, y=350)

    def clear_placeholder_username(self, event):
        if self.user_id_input.get() == "Please enter your username":
            self.user_id_input.delete(0, END)

    def add_placeholder_username(self, event):
        if not self.user_id_input.get():
            self.user_id_input.insert(0, "Please enter your username")

    def clear_placeholder_password(self, event):
        if self.password_input.get() == "Please enter your password":
            self.password_input.delete(0, END)
            self.password_input.configure(show="*")

    def add_placeholder_password(self, event):
        if not self.password_input.get():
            self.password_input.configure(show="")
            self.password_input.insert(0, "Please enter your password")

    def login_function(self):
        username = self.user_id_input.get()
        password = self.password_input.get()
        print(username, password)

        information = Login(username, password)


        userID = information[0]
        userNAME = information[2]
        role = information[1]

        if role == "Consumer":
            self.create_consumer_dashboard(userID,userNAME)
        elif role == "Seller":
            self.create_seller_dashboard(userID,userNAME)
        elif role == "Admin":
            pass
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def create_seller_dashboard(self, userID, userNAME):
        seller_window = ctk.CTkToplevel(self)
        seller_window.title("Seller Dashboard")
        seller_window.geometry("800x600")
        seller_window.configure(bg="#26547C")

        cart_items = []

        def clear_entries():
            item_name_entry.delete(0, ctk.END)
            description_entry.delete(0, ctk.END)
            quantity_entry.delete(0, ctk.END)

        def update_cart_list():
            cart_list.delete(*cart_list.get_children())
            for item in cart_items:
                cart_list.insert('', 'end', values=(item["name"], item["description"], item["price"], item["quantity"]))



        def update_cart_item():
            item_name_entry.configure(state=NORMAL)
            description_entry.configure(state=NORMAL)

            Product_Name = item_name_entry.get()
            Desc = description_entry.get()
            Quan = quantity_entry.get()
            Price = price_entry.get()

            update_check = update(Product_Name,Desc,Quan,Price)

            if update_check is True:
                messagebox.showinfo("Success", "Updated Market.")
                item_name_entry.delete(0, END)
                description_entry.delete(0, END)
                quantity_entry.delete(0, END)
                price_entry.delete(0, END)


            else:
                messagebox.showerror("Error", "Failed Update Market.")




        def remove_from_cart():
            item_name_entry.configure(state=NORMAL)
            description_entry.configure(state=NORMAL)

            Product_Name = item_name_entry.get()
            Desc = description_entry.get()
            Quan = quantity_entry.get()
            Price = price_entry.get()

            Remove_check = Remove(Product_Name, Desc, Quan, Price)

            if Remove_check is True:
                messagebox.showinfo("Success", "Remove from Market")
                item_name_entry.delete(0, END)
                description_entry.delete(0, END)
                quantity_entry.delete(0, END)
                price_entry.delete(0, END)

        def check_add_to_cart_result(item_name_entry,description_entry,quantity_entry,price_entry):
            result = add_to_cart(userID, userNAME, item_name_entry, description_entry, quantity_entry,
                                 price_entry)
            print("add_to_cart returned:", result)  # Print to console
            if result is True:
                messagebox.showinfo("Success", "Item added to market.")
            else:
                messagebox.showerror("Error", "Failed to add item.")

        def SELECTED(e):

            selected = cart_list.focus()
            values = cart_list.item(selected, 'values')
            if not values or len(values) < 4:
                return  # Prevents IndexError

            item_name_entry.delete(0, END)
            description_entry.delete(0, END)
            quantity_entry.delete(0, END)
            price_entry.delete(0, END)


            item_name_entry.insert(0, values[0])
            description_entry.insert(0, values[1])
            quantity_entry.insert(0, values[2])
            price_entry.insert(0,values[3])

            item_name_entry.configure(state=DISABLED)
            description_entry.configure(state=DISABLED)

        def refresh_market():
            products = refresh(userID,userNAME)
            item_name_entry.configure(state=NORMAL)
            description_entry.configure(state=NORMAL)

            if products:
                for item in cart_list.get_children():
                    cart_list.delete(item)

                counter = 1
                for product in products:
                    counter += 1
                    cart_list.insert('', 'end', text=f'{counter}', values=(
                        f'{product[3]}',f'{product[4]}', f'{product[5]}', f'{product[6]}'))

        def logout():
            response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
            if response:
                seller_window.destroy()  # Close the seller window

        # UI Components
        ctk.CTkLabel(seller_window, text=f"Welcome Seller, {userNAME}!", text_color="#FFFFF0",
                     font=("Helvetica", 24, "bold")).place(relx=0.5, rely=0.05, anchor="n")

        # Item Name
        ctk.CTkLabel(seller_window, text="Product Name", text_color="#FFFFF0").place(x=50, y=80, anchor="w")
        item_name_entry = ctk.CTkEntry(seller_window, width=250, text_color="black")
        item_name_entry.place(x=50, y=105, anchor="w")

        # Description
        ctk.CTkLabel(seller_window, text="Description", text_color="#FFFFF0").place(x=50, y=140, anchor="w")
        description_entry = ctk.CTkEntry(seller_window, width=250, text_color="black")
        description_entry.place(x=50, y=165, anchor="w")

        # Quantity
        ctk.CTkLabel(seller_window, text="Quantity", text_color="#FFFFF0").place(x=50, y=200, anchor="w")
        quantity_entry = ctk.CTkEntry(seller_window, width=250, text_color="black")
        quantity_entry.place(x=50, y=225, anchor="w")

        price_label = ctk.CTkLabel(seller_window, text="Price:", text_color="#FFFFF0")
        price_label.place(x=50, y=260, anchor="w")
        price_entry = ctk.CTkEntry(seller_window, width=250, text_color="black")
        price_entry.place(x=50, y=290, anchor="w")

        # Buttons Frame
        button_frame = ctk.CTkFrame(seller_window, fg_color="#26547C", width=260, height=250)
        button_frame.place(x=50, y=330, anchor="nw")

        ctk.CTkButton(button_frame, text="Add to Market", command= lambda : check_add_to_cart_result(item_name_entry.get(),description_entry.get(),quantity_entry.get(),price_entry.get()),
                      fg_color="#FFFFF0", text_color="black", hover_color="#FFD166").place(relx=0.05, rely=0.07,
                                                                                           relwidth=0.9, relheight=0.20)



        ctk.CTkButton(button_frame, text="Update Market", command=update_cart_item,
                      fg_color="#FFFFF0", text_color="black", hover_color="#FFD166").place(relx=0.05, rely=0.3,
                                                                                           relwidth=0.9, relheight=0.20)
        ctk.CTkButton(button_frame, text="Remove from Market", command=remove_from_cart,
                      fg_color="#FFFFF0", text_color="black", hover_color="#FFD166").place(relx=0.05, rely=0.53,
                                                                                           relwidth=0.9, relheight=0.20)
        ctk.CTkButton(button_frame, text="Refresh Market", command=refresh_market,
                      fg_color="#FFFFF0", text_color="black", hover_color="#FFD166").place(relx=0.05, rely=0.77,
                                                                                           relwidth=0.9, relheight=0.20)


        # Logout Button
        ctk.CTkButton(seller_window, text="Logout", command=logout,
                      fg_color="#06D6A0", text_color="black", hover_color="#FFFFF0").place(relx=0.97, rely=0.05,
                                                                                           anchor="ne")



        # Cart Frame
        cart_frame = ctk.CTkFrame(seller_window, fg_color="#26547C")
        cart_frame.place(relx=0.4, rely=0.15, relwidth=0.58, relheight=0.76)

        cart_list = ttk.Treeview(cart_frame, columns=("Name", "Description", "Price", "Quantity"), show='headings')
        cart_list.heading("Name", text="Name", anchor="w")
        cart_list.heading("Description", text="Description", anchor="w")
        cart_list.heading("Price", text="Price", anchor="w")
        cart_list.heading("Quantity", text="Quantity", anchor="w")
        cart_list.column("Name", width=int(0.38 * 800 * 0.25), anchor="w")
        cart_list.column("Description", width=int(0.38 * 800 * 0.4), anchor="w")
        cart_list.column("Price", width=int(0.38 * 800 * 0.15), anchor="w")
        cart_list.column("Quantity", width=int(0.38 * 800 * 0.15), anchor="w")
        cart_list.place(relx=0, rely=0, relwidth=1, relheight=1)
        cart_list.bind("<ButtonRelease-1>", SELECTED)


    def create_consumer_dashboard(self,User_ID,userNAME):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self = ctk.CTk()
        self.title("Consumer Dashboard")
        self.geometry("660x510")
        self.resizable(False, False)

        # Updated background color
        bg_color = "royalblue3"
        self.configure(bg=bg_color)  # Apply the background color here

        header_label = ctk.CTkLabel(self, text=f"Welcome Consumer, {userNAME}!", text_color="white",
                                    font=("Arial", 20, "bold"))
        header_label.place(x=20, y=20)

        logout_button = ctk.CTkButton(self, text="Logout", fg_color="#A8E6CF", text_color="black", width=70, height=30,
                                      hover_color="#96dbc6", corner_radius=12, command=self.quit)
        logout_button.place(x=570, y=20)

        search_entry = ctk.CTkEntry(self, placeholder_text="Search Item", width=150, height=30, corner_radius=12)
        search_entry.place(x=30, y=80)

        button_texts = ["ADD TO BASKET", "SELECT", "REMOVE PRODUCT", "CHECK BASKET", "CHECK-OUT"]
        for idx, text in enumerate(button_texts):
            button = ctk.CTkButton(
                self, text=text,
                width=150, height=30,
                fg_color="#DCEDC1", text_color="black", hover_color="#C8E6B7",
                corner_radius=12,
                command=lambda t=text: print(f"{t} clicked")
            )
            button.place(x=30, y=130 + idx * 50)

        product_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20, width=400, height=330)
        product_frame.place(x=230, y=100)

        header_names = ["Name", "Description", "Price"]
        header_positions = [30, 160, 300]
        for name, xpos in zip(header_names, header_positions):
            header = ctk.CTkLabel(product_frame, text=name, text_color="black", font=("Arial", 12, "bold"))
            header.place(x=xpos, y=10)

        sample_textbox = ctk.CTkTextbox(product_frame, width=360, height=270, corner_radius=12)
        sample_textbox.place(x=20, y=40)
       

        self.mainloop()

def create_admin_dashboard():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("660x510")
    root.title("Admin Dashboard")
    root.resizable(False, False)
    root.configure(bg="#26547C")  # Match your desired background color

    # --- Welcome Label ---
    welcome_label = ctk.CTkLabel(
        root, text="Welcome Admin, 20!",
        font=('Arial', 20, 'bold'),
        text_color="white"
    )
    welcome_label.place(x=20, y=20)

    # --- Logout Button ---
    logout_button = ctk.CTkButton(
        root, text="Logout",
        width=70, height=30,
        fg_color="#A8E6CF", text_color="black",
        hover_color="#96dbc6", corner_radius=12,
        command=root.quit
    )
    logout_button.place(x=570, y=20)

    # --- Account Verification Frame ---
    verification_frame = ctk.CTkFrame(
        root, fg_color="white",
        corner_radius=20, width=400, height=330
    )
    verification_frame.place(x=30, y=100)

    header_label = ctk.CTkLabel(
        verification_frame, text="Account Verification",
        text_color="black", font=('Arial', 14, 'bold')
    )
    header_label.place(x=130, y=5)

    # --- Column Headers ---
    col_headers = ["user_Id", "username", "Role"]
    col_positions = [30, 140, 270]

    for text, x in zip(col_headers, col_positions):
        label = ctk.CTkLabel(
            verification_frame, text=text,
            text_color="black", font=('Arial', 12, 'bold')
        )
        label.place(x=x, y=30)

    # --- User List Textbox ---
    user_listbox = ctk.CTkTextbox(verification_frame, width=360, height=250, corner_radius=12)
    user_listbox.place(x=20, y=60)
    user_listbox.insert("0.0", "1\tJohnDoe\tUser\n2\tJaneDoe\tAdmin")

    # --- Buttons on Right ---
    button_texts = ["Approve", "Reject", "Remove account"]
    button_commands = [lambda: print("Approved"), lambda: print("Rejected"), lambda: print("Removed")]
    for i, (text, cmd) in enumerate(zip(button_texts, button_commands)):
        button = ctk.CTkButton(
            root, text=text,
            width=130, height=30,
            fg_color="#DCEDC1", text_color="black",
            hover_color="#C8E6B7",
            corner_radius=12,
            command=cmd
        )
        button.place(x=480, y=150 + i * 50)

    root.mainloop()







class SignUpWindow(Toplevel):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.title("Sign Up")
        self.geometry("450x320")
        self.configure(bg=THEME_COLOR)
        self.resizable(False, False)

        self.init_ui()

    def init_ui(self):
        self.title_label = Label(self, text="Create an Account", bg=THEME_COLOR, fg=ACCENT_COLOR, font=("Arial", 20, "bold"))
        self.title_label.place(x=(450 - 200) // 2, y=20, width=200)

        self.username_input = Entry(self, font=("Arial", 14))
        self.username_input.insert(0, "Create a username")
        self.username_input.place(x=100, y=75, width=250, height=30)
        self.username_input.bind("<FocusIn>", self.clear_placeholder_username)
        self.username_input.bind("<FocusOut>", self.add_placeholder_username)

        self.password_input = Entry(self, font=("Arial", 14))
        self.password_input.insert(0, "Create a password")
        self.password_input.place(x=100, y=115, width=250, height=30)
        self.password_input.bind("<FocusIn>", self.clear_placeholder_password)
        self.password_input.bind("<FocusOut>", self.add_placeholder_password)

        self.role_label = Label(self, text="Sign-up as?", bg=THEME_COLOR, fg=ACCENT_COLOR, font=("Arial", FONT_SIZE))
        self.role_label.place(x=100, y=155)

        self.role_combo = ttk.Combobox(self, state="readonly", font=("Arial", 14))
        self.role_combo['values'] = ["Consumer", "Seller", "Admin"]
        self.role_combo.place(x=100, y=180, width=250, height=30)
        self.role_combo.current(0)

        self.signup_button = Button(self, text="Submit", command=self.submit_signup, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 14))
        self.signup_button.place(x=(450 - 100) // 2, y=250, width=100, height=40)

        self.back_button = Button(self, text="🡸", command=self.back_function, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 14))
        self.back_button.place(x=10, y=10, width=50, height=30)

    def clear_placeholder_username(self, event):
        if self.username_input.get() == "Create a username":
            self.username_input.delete(0, END)

    def add_placeholder_username(self, event):
        if not self.username_input.get():
            self.username_input.insert(0, "Create a username")

    def clear_placeholder_password(self, event):
        if self.password_input.get() == "Create a password":
            self.password_input.delete(0, END)
            self.password_input.config(show="*")

    def add_placeholder_password(self, event):
        if not self.password_input.get():
            self.password_input.config(show="")
            self.password_input.insert(0, "Create a password")

    def submit_signup(self):
        # Placeholder function - implement actual sign-up logic here
        username = self.username_input.get()
        password = self.password_input.get()
        role = self.role_combo.get()

        SignUp(role,username,password)

        messagebox.showinfo("Sign Up Submitted", f"Username: {username}\nRole: {role}")

    def back_function(self):
        self.destroy()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
