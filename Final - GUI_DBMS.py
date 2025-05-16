import tkinter
import pyodbc
from tkinter import *
from tkinter import messagebox, ttk
import customtkinter as ctk
from FUNCTIONS_DBMS import *
from customtkinter import *

# Set appearance and theme
set_appearance_mode("System")
set_default_color_theme("blue")  # Still used for button styling

THEME_COLOR = "#F0E68C"      # Khaki - background
ACCENT_COLOR = "#8B4513"     # Saddle Brown - accent
FONT_COLOR = "#3B2F2F"       # Dark Brown - font
BUTTON_HOVER_COLOR = "#DEB887"  # BurlyWood - hover color

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

        if information:
            userID = information[0]
            userNAME = information[2]
            role = information[1]

            if role == "Consumer":
                self.create_consumer_dashboard(userID, userNAME)
            elif role == "Seller":
                self.create_seller_dashboard(userID, userNAME)
            elif role == "Admin":
                # Pass the admin ID and username to the dashboard
                create_admin_dashboard(userID, userNAME)
            else:
                messagebox.showerror("Login Failed", "Invalid user role.")
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

            update_check = update(Product_Name, Desc, Quan, Price)

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

        def check_add_to_cart_result(item_name_entry, description_entry, quantity_entry, price_entry):
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
            price_entry.insert(0, values[3])

            item_name_entry.configure(state=DISABLED)
            description_entry.configure(state=DISABLED)

        def refresh_market():
            products = refresh(userID, userNAME)
            item_name_entry.configure(state=NORMAL)
            description_entry.configure(state=NORMAL)

            if products:
                for item in cart_list.get_children():
                    cart_list.delete(item)

                counter = 1
                for product in products:
                    counter += 1
                    cart_list.insert('', 'end', text=f'{counter}', values=(
                        f'{product[3]}', f'{product[4]}', f'{product[5]}', f'{product[6]}'))

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

        ctk.CTkButton(button_frame, text="Add to Market",
                      command=lambda: check_add_to_cart_result(item_name_entry.get(), description_entry.get(),
                                                               quantity_entry.get(), price_entry.get()),
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

    def create_consumer_dashboard(self, User_ID, userNAME):
        import customtkinter as ctk
        from PIL import Image, ImageTk
        import pyodbc
        from tkinter import messagebox

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        window = ctk.CTk()
        window.title("Consumer Dashboard")
        window.geometry("900x600")
        window.resizable(False, False)

        # Modern color scheme
        primary_color = "#3a7ebf"
        accent_color = "#f0f0f0"
        text_color = "#333333"
        highlight_color = "#4CAF50"

        # Create frames for layout
        header_frame = ctk.CTkFrame(window, fg_color=primary_color, corner_radius=0, height=70)
        header_frame.pack(fill="x")

        content_frame = ctk.CTkFrame(window, fg_color=accent_color)
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Header elements
        header_label = ctk.CTkLabel(
            header_frame,
            text=f"Welcome, {userNAME}!",
            text_color="white",
            font=("Arial", 22, "bold")
        )
        header_label.place(x=20, y=20)

        # Cart and items count display
        cart_items = 0
        cart_label = ctk.CTkLabel(
            header_frame,
            text=f"Cart: {cart_items} items",
            text_color="white",
            font=("Arial", 14)
        )
        cart_label.place(x=700, y=15)

        logout_button = ctk.CTkButton(
            header_frame,
            text="Logout",
            fg_color="#e74c3c",
            text_color="white",
            width=100,
            height=30,
            hover_color="#c0392b",
            corner_radius=5,
            command=window.quit
        )
        logout_button.place(x=780, y=20)

        # Left sidebar for actions
        sidebar_frame = ctk.CTkFrame(content_frame, fg_color="#2c3e50", width=200, corner_radius=0)
        sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)

        # Product display area
        product_area = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=0)
        product_area.pack(side="right", fill="both", expand=True)

        # Shopping cart to store selected items (now includes quantity)
        shopping_cart = []
        products = []  # Initialize products in the outer scope

        # Function to add product to cart
        # Function to add product to cart
        def add_to_cart(product_id):
            nonlocal cart_items
            nonlocal products
            selected_product_row = next((p for p in products if p[0] == product_id), None)
            if selected_product_row:
                selected_product_tuple = tuple(selected_product_row)  # Convert pyodbc.Row to tuple
                # For simplicity, let's assume adding always adds 1 kg.
                # In a real application, you'd have a quantity input.
                shopping_cart.append(selected_product_tuple + (1,))  # Add a tuple with quantity (1)
                cart_items += 1
                cart_label.configure(text=f"Cart: {cart_items} items")
                update_cart_display()

        # Function to remove product from cart
        def remove_from_cart(product_id):
            nonlocal cart_items
            for i, item in enumerate(shopping_cart):
                if item[0] == product_id:
                    shopping_cart.pop(i)
                    cart_items -= 1
                    cart_label.configure(text=f"Cart: {cart_items} items")
                    update_cart_display()
                    break

        # Function to view cart
        def view_cart():
            cart_window = ctk.CTkToplevel(window)
            cart_window.title("Your Shopping Cart")
            cart_window.geometry("600x400")

            if not shopping_cart:
                empty_label = ctk.CTkLabel(
                    cart_window,
                    text="Your cart is empty",
                    font=("Arial", 16)
                )
                empty_label.pack(pady=30)
            else:
                # Display items in cart
                header_frame = ctk.CTkFrame(cart_window)
                header_frame.pack(fill="x", padx=10, pady=10)

                ctk.CTkLabel(header_frame, text="Product", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10)
                ctk.CTkLabel(header_frame, text="Quantity (kg)", font=("Arial", 14, "bold")).grid(row=0, column=1,
                                                                                                  padx=10)
                ctk.CTkLabel(header_frame, text="Price", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10)
                ctk.CTkLabel(header_frame, text="Actions", font=("Arial", 14, "bold")).grid(row=0, column=3, padx=10)

                cart_frame = ctk.CTkScrollableFrame(cart_window, height=250)
                cart_frame.pack(fill="both", expand=True, padx=10)

                total = 0
                for i, item in enumerate(shopping_cart):
                    product_id, product_name, description, price, quantity_in_stock, purchased_quantity = item
                    total += price * purchased_quantity

                    ctk.CTkLabel(cart_frame, text=product_name).grid(row=i, column=0, sticky="w", padx=10, pady=5)
                    ctk.CTkLabel(cart_frame, text=str(purchased_quantity)).grid(row=i, column=1, padx=10, pady=5)
                    ctk.CTkLabel(cart_frame, text=f"₱{price * purchased_quantity:.2f}").grid(row=i, column=2, padx=10,
                                                                                             pady=5)

                    remove_btn = ctk.CTkButton(
                        cart_frame,
                        text="Remove",
                        fg_color="#e74c3c",
                        text_color="white",
                        width=80,
                        command=lambda pid=product_id: remove_from_cart(pid)
                    )
                    remove_btn.grid(row=i, column=3, padx=10, pady=5)

                total_frame = ctk.CTkFrame(cart_window)
                total_frame.pack(fill="x", padx=10, pady=10)

                ctk.CTkLabel(
                    total_frame,
                    text=f"Total: ₱{total:.2f}",
                    font=("Arial", 16, "bold")
                ).pack(side="left", padx=10)

                checkout_btn = ctk.CTkButton(
                    total_frame,
                    text="Proceed to Checkout",
                    fg_color=highlight_color,
                    text_color="white",
                    width=150,
                    command=lambda: checkout()
                )
                checkout_btn.pack(side="right", padx=10)

        def checkout():
            if not shopping_cart:
                return

            checkout_window = ctk.CTkToplevel(window)
            checkout_window.title("Checkout")
            checkout_window.geometry("400x300")

            ctk.CTkLabel(
                checkout_window,
                text="Order Completed!",
                font=("Arial", 20, "bold")
            ).pack(pady=20)

            total = sum(
                item[3] * item[5] for item in shopping_cart)  # Calculate total based on price and purchased quantity

            ctk.CTkLabel(
                checkout_window,
                text=f"Total paid: ₱{total:.2f}",
                font=("Arial", 16)
            ).pack(pady=10)

            ctk.CTkLabel(
                checkout_window,
                text=f"Thank you for your purchase, {userNAME}!",
                font=("Arial", 14)
            ).pack(pady=10)

            # Clear cart after checkout
            shopping_cart.clear()
            nonlocal cart_items
            cart_items = 0
            cart_label.configure(text=f"Cart: {cart_items} items")

            close_btn = ctk.CTkButton(
                checkout_window,
                text="Close",
                command=checkout_window.destroy
            )
            close_btn.pack(pady=20)

        # Function to update cart display (currently empty)
        def update_cart_display():
            pass

        # Create sidebar buttons
        button_data = [
            {"text": "View Products", "command": lambda: display_products()},
            {"text": "View Cart", "command": lambda: view_cart()},
            {"text": "My Orders", "command": lambda: display_message("Order history will be shown here")},
            {"text": "My Profile", "command": lambda: display_message(f"Profile for {userNAME} (ID: {User_ID})")},
            {"text": "Settings", "command": lambda: display_message("Settings will be shown here")},
        ]

        for i, btn in enumerate(button_data):
            action_btn = ctk.CTkButton(
                sidebar_frame,
                text=btn["text"],
                fg_color="transparent",
                text_color="white",
                hover_color="#34495e",
                anchor="w",
                height=40,
                command=btn["command"]
            )
            action_btn.pack(fill="x", padx=10, pady=(10 if i == 0 else 5))

        # Display a message in the product area
        def display_message(message):
            for widget in product_area.winfo_children():
                widget.destroy()

            message_label = ctk.CTkLabel(
                product_area,
                text=message,
                font=("Arial", 16)
            )
            message_label.pack(pady=50)

        # Display products in the product area
        def display_products():
            nonlocal products
            for widget in product_area.winfo_children():
                widget.destroy()

            scroll_frame = ctk.CTkScrollableFrame(product_area)
            scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

            header_frame = ctk.CTkFrame(scroll_frame)
            header_frame.pack(fill="x", pady=(0, 10))

            headers = ["Product", "Description", "Price", "Available (kg)", "Action"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=("Arial", 14, "bold")
                )
                label.grid(row=0, column=i, padx=10, sticky="w")

            try:
                cursor = connect.cursor()
                cursor.execute(
                    "SELECT Product_ID, Product_Name, Description, Price, Quantity FROM Products")
                products = cursor.fetchall()

                for i, product in enumerate(products):
                    frame = ctk.CTkFrame(scroll_frame, fg_color=("#f9f9f9" if i % 2 == 0 else "white"))
                    frame.pack(fill="x", pady=5)

                    ctk.CTkLabel(
                        frame,
                        text=product[1],
                        font=("Arial", 13)
                    ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

                    ctk.CTkLabel(
                        frame,
                        text=product[2],
                        font=("Arial", 13)
                    ).grid(row=0, column=1, padx=10, pady=10, sticky="w")

                    ctk.CTkLabel(
                        frame,
                        text=f"₱{product[3]:.2f}",
                        font=("Arial", 13, "bold")
                    ).grid(row=0, column=2, padx=10, pady=10, sticky="w")

                    ctk.CTkLabel(
                        frame,
                        text=str(product[4]),
                        font=("Arial", 13)
                    ).grid(row=0, column=3, padx=10, pady=10, sticky="w")

                    add_button = ctk.CTkButton(
                        frame,
                        text="Add to Cart",
                        fg_color=highlight_color,
                        text_color="white",
                        width=100,
                        height=30,
                        corner_radius=5,
                        command=lambda pid=product[0]: add_to_cart(pid)
                    )
                    add_button.grid(row=0, column=4, padx=10, pady=10)

            except pyodbc.Error as e:
                messagebox.showerror("Database Error", f"Error fetching products: {e}")

        # Show products by default when the dashboard opens
        display_products()

        window.mainloop()


def create_admin_dashboard(admin_id, admin_name):
    """
    Creates an admin dashboard window that displays all user accounts
    with options to delete any account.

    Args:
        admin_id: The ID of the admin user
        admin_name: The username of the admin user
    """
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("800x550")
    root.title("Admin Dashboard")
    root.resizable(False, False)
    root.configure(fg_color="#26547C")  # Using fg_color instead of bg for CTk

    # --- Welcome Label ---
    welcome_label = ctk.CTkLabel(
        root, text=f"Welcome Admin, {admin_name}!",
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
        command=root.destroy
    )
    logout_button.place(x=700, y=20)

    # --- Accounts List Frame ---
    accounts_frame = ctk.CTkFrame(
        root, fg_color="white",
        corner_radius=20, width=550, height=450
    )
    accounts_frame.place(x=30, y=70)

    header_label = ctk.CTkLabel(
        accounts_frame, text="All User Accounts",
        text_color="black", font=('Arial', 16, 'bold')
    )
    header_label.place(x=200, y=10)

    # Configure treeview style
    style = ttk.Style()
    style.configure("Treeview",
                    background="#F0F0F0",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#F0F0F0")
    style.map('Treeview', background=[('selected', '#3584e4')])

    # Create Treeview with standard scrollbar (not CTkScrollbar)
    # Standard tkinter Frame to hold the treeview and scrollbar
    tree_frame = Frame(accounts_frame, bg="white")
    tree_frame.place(x=10, y=45, width=530, height=390)

    # Standard tkinter Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create Treeview
    accounts_tree = ttk.Treeview(tree_frame,
                                 columns=("ID", "Username", "Role", "Status"),
                                 show='headings',
                                 yscrollcommand=tree_scroll.set)

    # Configure columns
    accounts_tree.heading("ID", text="User ID")
    accounts_tree.heading("Username", text="Username")
    accounts_tree.heading("Role", text="Role")
    accounts_tree.heading("Status", text="Status")

    accounts_tree.column("ID", width=50, anchor="center")
    accounts_tree.column("Username", width=150, anchor="w")
    accounts_tree.column("Role", width=100, anchor="center")
    accounts_tree.column("Status", width=100, anchor="center")

    # Pack treeview
    accounts_tree.pack(side=LEFT, fill=BOTH, expand=True)

    # Connect scrollbar to treeview
    tree_scroll.config(command=accounts_tree.yview)

    # --- Action Buttons ---
    buttons_frame = ctk.CTkFrame(
        root, fg_color="#26547C",
        corner_radius=20, width=180, height=300
    )
    buttons_frame.place(x=600, y=100)

    # Refresh button
    refresh_button = ctk.CTkButton(
        buttons_frame, text="Refresh List",
        width=150, height=40,
        fg_color="#DCEDC1", text_color="black",
        hover_color="#C8E6B7",
        corner_radius=12,
        command=lambda: load_all_accounts(accounts_tree)
    )
    refresh_button.place(x=15, y=20)

    # Delete account button
    delete_button = ctk.CTkButton(
        buttons_frame, text="Delete Account",
        width=150, height=40,
        fg_color="#FF6B6B", text_color="white",
        hover_color="#FF4949",
        corner_radius=12,
        command=lambda: delete_selected_account(accounts_tree)
    )
    delete_button.place(x=15, y=80)

    # Function to load all accounts from database
    def load_all_accounts(tree):
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)

        try:
            # Connect to database
            cursor = connect.cursor()

            # Fetch all accounts
            cursor.execute(
                "SELECT User_Id, Username, Role_type, CASE WHEN Verified IS NULL THEN 'Pending' WHEN Verified = 1 THEN 'Verified' ELSE 'Rejected' END as Status FROM Users")
            accounts = cursor.fetchall()

            # Insert accounts into treeview
            for account in accounts:
                # Skip the admin viewing the dashboard to prevent self-deletion
                if account[0] != admin_id:
                    tree.insert("", "end", values=(account[0], account[1], account[2], account[3]))

        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to load accounts: {str(e)}")

    # Function to delete selected account
    def delete_selected_account(tree):
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an account to delete.")
            return

        account_values = tree.item(selected_item, "values")
        user_id = account_values[0]
        username = account_values[1]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete account:\n\nID: {user_id}\nUsername: {username}?\n\nThis action cannot be undone.")

        if confirm:
            try:
                cursor = connect.cursor()

                # First delete any related records
                # For example: delete from Consumers, Sellers or Admin tables first
                cursor.execute("DELETE FROM Consumers WHERE Users_ID_FK = ?", (user_id,))
                cursor.execute("DELETE FROM Sellers WHERE User_ID_FK = ?", (user_id,))
                cursor.execute("DELETE FROM Admin WHERE User_ID_FK = ?", (user_id,))

                # Then delete the main user record
                cursor.execute("DELETE FROM Users WHERE User_Id = ?", (user_id,))
                connect.commit()

                # Remove from treeview
                tree.delete(selected_item)

                messagebox.showinfo("Success", f"Account '{username}' has been deleted.")

            except pyodbc.Error as e:
                connect.rollback()
                messagebox.showerror("Delete Error", f"Failed to delete account: {str(e)}")

    # Load accounts when the dashboard is opened
    load_all_accounts(accounts_tree)

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
        self.title_label = Label(self, text="Create an Account", bg=THEME_COLOR, fg=ACCENT_COLOR,
                                 font=("Arial", 20, "bold"))
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

        self.signup_button = Button(self, text="Submit", command=self.submit_signup, bg=ACCENT_COLOR, fg=FONT_COLOR,
                                    font=("Arial", 14))
        self.signup_button.place(x=(450 - 100) // 2, y=250, width=100, height=40)

        self.back_button = Button(self, text="🡸", command=self.back_function, bg=ACCENT_COLOR, fg=FONT_COLOR,
                                  font=("Arial", 14))
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

        SignUp(role, username, password)

        messagebox.showinfo("Sign Up Submitted", f"Username: {username}\nRole: {role}")

    def back_function(self):
        self.destroy()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
