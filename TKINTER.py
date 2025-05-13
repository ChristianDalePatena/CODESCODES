import tkinter as tk
from tkinter import messagebox, ttk
import uuid
import os

# GLOBAL THEME FOR EASY MODIFICATION
THEME_COLOR = "#26547C"
ACCENT_COLOR = "#FFFFF0"
BUTTON_HOVER_COLOR = "#FFD166"
FONT_COLOR = "black"
FONT_SIZE = 14
WINDOW_ICON_PATH = "C:\\Users\\Chris\\Downloads\\cubaoo.png"  # Adjust if needed

def dummy_get_user_by_username(username):
    # Dummy function simulating database return: (user_id, role, username)
    if username == "admin":
        return ("U123456", "admin", username)
    elif username == "seller":
        return ("U654321", "seller", username)
    elif username == "consumer":
        return ("U112233", "consumer", username)
    return None

def dummy_login_user(username, password):
    # Dummy authentication: accepts any password for the example
    user = dummy_get_user_by_username(username)
    return user if user else None

def dummy_signup_user(username, password, role):
    # Dummy signup, always success unless username exists
    if dummy_get_user_by_username(username):
        return False
    # Pretend to create user
    return True

def dummy_get_seller_by_user_id(user_id):
    # Dummy seller ID for user_id
    return ("S123456",)

def dummy_get_all_categories():
    # Return dummy category list (id, name)
    return [(1, "Fruits"), (2, "Vegetables"), (3, "Dairy")]

def dummy_create_product(product_id, seller_id, name, description, price, category_text):
    # Dummy function just print
    print(f"Create product: {product_id}, {seller_id}, {name}, {description}, {price}, {category_text}")

def dummy_update_product(product_id, name, description, price):
    print(f"Update product: {product_id}, {name}, {description}, {price}")

def dummy_delete_product(product_id):
    print(f"Delete product: {product_id}")

def set_current_user(user_id, username, role):
    # Dummy session setter
    global CURRENT_USER
    CURRENT_USER = {"user_id": user_id, "username": username, "role": role}

CURRENT_USER = None

class AdminDashboard(tk.Toplevel):
    def __init__(self, username, main_window):
        super().__init__()
        self.main_window = main_window
        self.title("Admin Dashboard")
        self.geometry("800x600")
        self.configure(bg=THEME_COLOR)
        self.resizable(False, False)

        title = tk.Label(self, text=f"Welcome Admin, {username}!", bg=THEME_COLOR, fg=ACCENT_COLOR, font=("Arial", 24, "bold"))
        title.place(x=50, y=50)

        self.logout_button = tk.Button(self, text="Logout", command=self.logout_function, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 14), relief="raised", bd=2)
        self.logout_button.place(x=650, y=50, width=100, height=40)

    def logout_function(self):
        set_current_user(None, None, None)
        self.destroy()
        self.main_window.show_main_window()


class SellerDashboard(tk.Toplevel):
    def __init__(self, username, main_window):
        super().__init__()
        self.main_window = main_window
        self.title("Seller Dashboard")
        self.geometry("800x600")
        self.configure(bg=THEME_COLOR)
        self.resizable(False, False)
        self.username = username
        self.seller_id = self.get_seller_id_from_db()
        self.current_category_id = None
        self.highlighted_row = None

        self.init_ui()
        self.load_categories()
        self.load_products()

    def get_seller_id_from_db(self):
        user = dummy_get_user_by_username(self.username)
        if user:
            user_id = user[0]
            seller = dummy_get_seller_by_user_id(user_id)
            if seller:
                return seller[0]
        messagebox.showerror("Error", "Failed to get seller ID")
        return None

    def init_ui(self):
        title_label = tk.Label(self, text="Seller's Window", bg=THEME_COLOR, fg=ACCENT_COLOR, font=("Arial", 18, "bold"))
        title_label.place(x=300, y=20)

        # Labels and Entry fields
        lbl_name = tk.Label(self, text="Item Name:", bg=THEME_COLOR, fg=FONT_COLOR, font=("Arial", 12))
        lbl_name.place(x=40, y=110)
        self.item_name_input = tk.Entry(self, font=("Arial", 12))
        self.item_name_input.place(x=120, y=110, width=150, height=25)

        lbl_price = tk.Label(self, text="Price:", bg=THEME_COLOR, fg=FONT_COLOR, font=("Arial", 12))
        lbl_price.place(x=40, y=150)
        self.item_amount_input = tk.Entry(self, font=("Arial", 12))
        self.item_amount_input.place(x=120, y=150, width=150, height=25)

        lbl_desc = tk.Label(self, text="Description:", bg=THEME_COLOR, fg=FONT_COLOR, font=("Arial", 12))
        lbl_desc.place(x=40, y=190)
        self.item_description_input = tk.Entry(self, font=("Arial", 12))
        self.item_description_input.place(x=120, y=190, width=150, height=25)

        lbl_category = tk.Label(self, text="Category:", bg=THEME_COLOR, fg=FONT_COLOR, font=("Arial", 12))
        lbl_category.place(x=40, y=230)
        self.category_combo = ttk.Combobox(self, state="readonly", font=("Arial", 12))
        self.category_combo.place(x=120, y=230, width=150, height=25)
        self.category_combo.bind("<<ComboboxSelected>>", self.category_selected)

        btn_check_orders = tk.Button(self, text="Check Orders", command=self.check_orders, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 12))
        btn_check_orders.place(x=50, y=280, width=135, height=40)

        btn_add_product = tk.Button(self, text="Add Product", command=self.add_product, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 12))
        btn_add_product.place(x=50, y=330, width=135, height=40)

        btn_update_product = tk.Button(self, text="Update Product", command=self.update_product, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 12))
        btn_update_product.place(x=50, y=380, width=135, height=40)

        btn_delete_product = tk.Button(self, text="Delete Product", command=self.delete_product, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 12))
        btn_delete_product.place(x=50, y=430, width=135, height=40)

        self.logout_button = tk.Button(self, text="Logout", command=self.logout_function, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 12))
        self.logout_button.place(x=670, y=20, width=100, height=40)

        # Table (Treeview)
        self.table = ttk.Treeview(self, columns=("Name", "Description", "Price", "Product ID", "Category"), show='headings', height=15)
        self.table.place(x=350, y=100, width=430, height=400)
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=80, anchor="center")
        self.table.column("Description", width=100)
        self.table.column("Name", width=120)
        self.table.column("Category", width=100)

    def load_categories(self):
        categories = dummy_get_all_categories()
        category_names = [cat[1] for cat in categories]
        self.category_combo['values'] = category_names
        if category_names:
            self.category_combo.current(0)

    def category_selected(self, event):
        self.current_category_id = self.category_combo.get()

    def load_products(self):
        # Dummy loading products example
        self.table.delete(*self.table.get_children())
        # Here you could load from DB, for now we add dummy data
        dummy_products = [
            ("Apple", "Fresh red apple", "1.20", "P001", "Fruits"),
            ("Carrot", "Orange carrot", "0.80", "P002", "Vegetables"),
            ("Milk", "1 litre milk", "1.00", "P003", "Dairy"),
        ]
        # Only showing products for this seller in dummy
        for prod in dummy_products:
            self.table.insert('', 'end', values=prod)

    def check_orders(self):
        messagebox.showinfo("Check Orders", "Check Orders functionality will go here.")

    def add_product(self):
        name = self.item_name_input.get()
        description = self.item_description_input.get()
        price_text = self.item_amount_input.get()
        category_text = self.category_combo.get()

        try:
            price = float(price_text)
        except ValueError:
            messagebox.showwarning("Error", "Invalid price format. Please enter a number.")
            return

        if not name or not description or not price_text:
            messagebox.showwarning("Error", "All fields are required.")
            return

        product_id = "P" + uuid.uuid4().hex[:6].upper()
        dummy_create_product(product_id, self.seller_id, name, description, price, category_text)
        self.load_products()
        messagebox.showinfo("Success", "Product added successfully.")
        self.clear_input_fields()

    def update_product(self):
        selected_item = self.table.focus()
        if not selected_item:
            messagebox.showwarning("Error", "Please select a product to update.")
            return

        product_data = self.table.item(selected_item)["values"]
        product_id = product_data[3]

        name = self.item_name_input.get()
        description = self.item_description_input.get()
        price_text = self.item_amount_input.get()

        try:
            price = float(price_text)
        except ValueError:
            messagebox.showwarning("Error", "Invalid price format. Please enter a number.")
            return

        if not name or not description or not price_text:
            messagebox.showwarning("Error", "All fields are required.")
            return

        dummy_update_product(product_id, name, description, price)
        self.load_products()
        messagebox.showinfo("Success", "Product updated successfully.")
        self.clear_input_fields()

    def delete_product(self):
        selected_item = self.table.focus()
        if not selected_item:
            messagebox.showwarning("Error", "Please select a product to delete.")
            return

        product_data = self.table.item(selected_item)["values"]
        product_id = product_data[3]

        dummy_delete_product(product_id)
        self.load_products()
        messagebox.showinfo("Success", "Product deleted successfully.")
        self.clear_input_fields()

    def clear_input_fields(self):
        self.item_name_input.delete(0, tk.END)
        self.item_description_input.delete(0, tk.END)
        self.item_amount_input.delete(0, tk.END)
        self.category_combo.current(0)

    def logout_function(self):
        set_current_user(None, None, None)
        self.destroy()
        self.main_window.show_main_window()

class ConsumerDashboard(tk.Toplevel):
    def __init__(self, username, main_window):
        super().__init__()
        self.main_window = main_window
        self.title("Consumer Dashboard")
        self.geometry("800x600")
        self.configure(bg=THEME_COLOR)
        self.resizable(False, False)

        title = tk.Label(self, text=f"Welcome Consumer, {username}!", bg=THEME_COLOR, fg=ACCENT_COLOR, font=("Arial", 24, "bold"))
        title.place(x=50, y=50)

        self.logout_button = tk.Button(self, text="Logout", command=self.logout_function, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 14))
        self.logout_button.place(x=650, y=50, width=100, height=40)

    def logout_function(self):
        set_current_user(None, None, None)
        self.destroy()
        self.main_window.show_main_window()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Farmers Cubao")
        self.geometry("800x550")
        self.configure(bg=THEME_COLOR)
        self.resizable(False, False)

        # Window icon
        if os.path.exists(WINDOW_ICON_PATH):
            try:
                self.iconbitmap(WINDOW_ICON_PATH)
            except Exception:
                pass  # iconbitmap might fail for png on some systems

        # Dashboard windows references
        self.admin_dashboard = None
        self.seller_dashboard = None
        self.consumer_dashboard = None

        # UI Initialization
        self.init_ui()

    def init_ui(self):
        # Image
        from PIL import Image, ImageTk  # Pillow needed
        if os.path.exists(WINDOW_ICON_PATH):
            try:
                img = Image.open(WINDOW_ICON_PATH)
                img = img.resize((300, 300), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                self.image_label = tk.Label(self, image=photo, bg=THEME_COLOR)
                self.image_label.image = photo  # Keep ref
                self.image_label.place(x=250, y=30)
            except Exception:
                # If PIL not installed or error, fallback text
                self.image_label = tk.Label(self, text="[Image]", bg=THEME_COLOR, fg=ACCENT_COLOR)
                self.image_label.place(x=350, y=150)
        else:
            self.image_label = tk.Label(self, text="[Image Not Found]", bg=THEME_COLOR, fg=ACCENT_COLOR)
            self.image_label.place(x=350, y=150)

        # Username input
        self.user_id_input = tk.Entry(self, font=("Arial", 14))
        self.user_id_input.insert(0, "Please enter your username")
        self.user_id_input.place(x=300, y=250, width=200, height=30)
        self.user_id_input.bind("<FocusIn>", self.clear_placeholder_username)
        self.user_id_input.bind("<FocusOut>", self.add_placeholder_username)

        # Password input
        self.password_input = tk.Entry(self, font=("Arial", 14), show="")
        self.password_input.insert(0, "Please enter your password")
        self.password_input.place(x=300, y=300, width=200, height=30)
        self.password_input.bind("<FocusIn>", self.clear_placeholder_password)
        self.password_input.bind("<FocusOut>", self.add_placeholder_password)

        # Buttons
        self.login_button = tk.Button(self, text="Login", command=self.login_function, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 14))
        self.signup_button = tk.Button(self, text="Sign Up", command=self.signup_function, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 14))
        self.login_button.place(x=290, y=350, width=105, height=40)
        self.signup_button.place(x=410, y=350, width=105, height=40)

    def clear_placeholder_username(self, event):
        if self.user_id_input.get() == "Please enter your username":
            self.user_id_input.delete(0, tk.END)

    def add_placeholder_username(self, event):
        if not self.user_id_input.get():
            self.user_id_input.insert(0, "Please enter your username")

    def clear_placeholder_password(self, event):
        if self.password_input.get() == "Please enter your password":
            self.password_input.delete(0, tk.END)
            self.password_input.config(show="*")

    def add_placeholder_password(self, event):
        if not self.password_input.get():
            self.password_input.config(show="")
            self.password_input.insert(0, "Please enter your password")

    def signup_function(self):
        if not hasattr(self, 'signup_window') or self.signup_window is None:
            self.signup_window = SignUpWindow(self)
        self.signup_window.deiconify()
        self.withdraw()  # Hide main window

    def login_function(self):
        username = self.user_id_input.get()
        password = self.password_input.get()

        if username == "" or username == "Please enter your username" or password == "" or password == "Please enter your password":
            messagebox.showwarning("Error!", "Please enter both username and password.")
            return

        user = dummy_login_user(username, password)
        if user:
            user_id_from_db = user[0]
            role = user[1]
            username = user[2]
            set_current_user(user_id_from_db, username, role)
            messagebox.showinfo("Success!", f"Welcome, {username} ({role})!")
            self.withdraw()  # Hide main window

            try:
                role_lower = role.lower()
                if role_lower == "admin":
                    if self.admin_dashboard is None or not self.admin_dashboard.winfo_exists():
                        self.admin_dashboard = AdminDashboard(username, self)
                    self.admin_dashboard.deiconify()
                elif role_lower == "seller":
                    if self.seller_dashboard is None or not self.seller_dashboard.winfo_exists():
                        self.seller_dashboard = SellerDashboard(username, self)
                    self.seller_dashboard.deiconify()
                else:
                    if self.consumer_dashboard is None or not self.consumer_dashboard.winfo_exists():
                        self.consumer_dashboard = ConsumerDashboard(username, self)
                    self.consumer_dashboard.deiconify()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open dashboard: {e}")
        else:
            messagebox.showerror("Login Failed!", "Invalid username or password.")

    def show_main_window(self):
        self.deiconify()


class SignUpWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.title("Sign Up")
        self.geometry("450x320")
        self.configure(bg=THEME_COLOR)
        self.resizable(False, False)

        self.init_ui()

    def init_ui(self):
        self.title_label = tk.Label(self, text="Create an Account", bg=THEME_COLOR, fg=ACCENT_COLOR, font=("Arial", 20, "bold"))
        self.title_label.place(x=(450 - 200) // 2, y=20, width=200)

        self.username_input = tk.Entry(self, font=("Arial", 14))
        self.username_input.insert(0, "Create a username")
        self.username_input.place(x=100, y=75, width=250, height=30)
        self.username_input.bind("<FocusIn>", self.clear_placeholder_username)
        self.username_input.bind("<FocusOut>", self.add_placeholder_username)

        self.password_input = tk.Entry(self, font=("Arial", 14))
        self.password_input.insert(0, "Create a password")
        self.password_input.place(x=100, y=115, width=250, height=30)
        self.password_input.bind("<FocusIn>", self.clear_placeholder_password)
        self.password_input.bind("<FocusOut>", self.add_placeholder_password)

        self.role_label = tk.Label(self, text="Sign-up as?", bg=THEME_COLOR, fg=ACCENT_COLOR, font=("Arial", FONT_SIZE))
        self.role_label.place(x=100, y=155)

        self.role_combo = ttk.Combobox(self, state="readonly", font=("Arial", 14))
        self.role_combo['values'] = ["Consumer", "Seller", "Admin"]
        self.role_combo.place(x=100, y=180, width=250, height=30)
        self.role_combo.current(0)

        self.signup_button = tk.Button(self, text="Submit", command=self.submit_signup, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 14))
        self.signup_button.place(x=(450 - 100) // 2, y=250, width=100, height=40)

        self.back_button = tk.Button(self, text="🡸", command=self.back_function, bg=ACCENT_COLOR, fg=FONT_COLOR, font=("Arial", 14))
        self.back_button.place(x=10, y=10, width=50, height=30)

    def clear_placeholder_username(self, event):
        if self.username_input.get() == "Create a username":
            self.username_input.delete(0, tk.END)

    def add_placeholder_username(self, event):
        if not self.username_input.get():
            self.username_input.insert(0, "Create a username")

    def clear_placeholder_password(self, event):
        if self.password_input.get() == "Create a password":
            self.password_input.delete(0, tk.END)
            self.password_input.config(show="*")

    def add_placeholder_password(self, event):
        if not self.password_input.get():
            self.password_input.config(show="")
            self.password_input.insert(0, "Create a password")

    def submit_signup(self):
        username = self.username_input.get()
        password = self.password_input.get()
        role = self.role_combo.get()

        # Validate inputs
        if username == "" or username == "Create a username" or password == "" or password == "Create a password" or role == "":
            messagebox.showwarning("Error", "All fields must be filled to create an account!")
            return

        success = dummy_signup_user(username, password, role)
        if success:
            messagebox.showinfo("Success", "Account created successfully!")
            self.withdraw()
            self.main_window.show_main_window()
        else:
            messagebox.showwarning("Error", "Username already exists or account creation failed.")

    def back_function(self):
        self.withdraw()
        self.main_window.show_main_window()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

