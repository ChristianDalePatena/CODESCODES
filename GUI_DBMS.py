from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
)
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QTimer
from Functions import (
    login_user,
    set_current_user,
    get_user_role,
    signup_user,
    get_products_by_seller,
    get_current_user,
    create_product,
    delete_product,
    update_product,
    get_user_by_username,
    get_seller_by_user_id,
    get_all_categories,
    create_category,
    get_connection,
)
import sys
import uuid


# GLOBAL THEME PARA MADALING MA MODIFY
THEME_COLOR = "#26547C"
ACCENT_COLOR = "#FFFFF0"
BUTTON_HOVER_COLOR = "#FFD166"
FONT_COLOR = "black"
FONT_SIZE = "14px"
BUTTON_BORDER_RADIUS = "10px"
BUTTON_PADDING = "8px 16px"
BORDER_WIDTH = "2px"
BORDER_COLOR = "#06D6A0"

BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {ACCENT_COLOR};
        color: {FONT_COLOR};
        font-size: {FONT_SIZE};
        padding: {BUTTON_PADDING};
        border-radius: {BUTTON_BORDER_RADIUS};
        border: {BORDER_WIDTH} solid {BORDER_COLOR};
    }}
    QPushButton:hover {{
        background-color: {BUTTON_HOVER_COLOR};
    }}
"""

INPUT_STYLE = f"""
    QLineEdit {{
        font-size: {FONT_SIZE};
        padding: 5px;
        border-radius: {BUTTON_BORDER_RADIUS};
        border: {BORDER_WIDTH} solid {BORDER_COLOR};
    }}
"""


class AdminDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setFixedSize(800, 600)  # Changed to 800x600
        self.setWindowIcon(QIcon("C:\\Users\\Chris\\Downloads\\cubaoo.png"))
        self.setStyleSheet(f"background-color: {THEME_COLOR};")
        title = QLabel(f"Welcome Admin, {username}!", self)
        title.setStyleSheet(f"color: {ACCENT_COLOR}; font-size: 24px; font-weight: bold;")
        title.adjustSize()
        title.move(50, 50)

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setStyleSheet(BUTTON_STYLE)
        self.logout_button.move(650, 50)
        self.logout_button.clicked.connect(self.logout_function)

    def logout_function(self):
        set_current_user(None, None, None)
        self.close()
        self.main_window.show()

    def set_main_window(self, main_window):
        self.main_window = main_window


class SellerDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Seller Dashboard")
        self.setFixedSize(800, 600)
        self.setStyleSheet(f"background-color: {THEME_COLOR};")
        self.setWindowIcon(QIcon("C:\\Users\\Chris\\Downloads\\cubaoo.png"))
        self.username = username
        self.seller_id = self.get_seller_id_from_db()
        self.current_category_id = None
        self.init_ui()
        self.load_categories()
        self.highlighted_row = -1  # Initialize highlighted row

    def get_seller_id_from_db(self):
        """Retrieves the seller ID from the database based on the user's username."""
        try:
            user = get_user_by_username(self.username)
            if user:
                user_id = user[0]
                seller = get_seller_by_user_id(user_id)
                if seller:
                    return seller[0]
            return None
        except Exception as e:
            print(f"Error in get_seller_id_from_db: {e}")
            QMessageBox.critical(
                self, "Database Error", "Failed to retrieve seller information."
            )
            return None

    def init_ui(self):
        title_label = QLabel("Seller's Window", self)
        title_label.setStyleSheet(
            f"color: {ACCENT_COLOR}; font-size: 18px; font-weight: bold;"
        )
        title_label.adjustSize()
        title_label.move(300, 20)

        # Product Input Fields
        item_name_label = QLabel("Item Name:", self)
        item_name_label.move(40, 110)
        self.item_name_input = QLineEdit(self)
        self.item_name_input.setFixedSize(150, 30)
        self.item_name_input.setStyleSheet(INPUT_STYLE)
        self.item_name_input.move(120, 100)

        item_amount_label = QLabel("Price:", self)
        item_amount_label.move(40, 150)
        self.item_amount_input = QLineEdit(self)
        self.item_amount_input.setFixedSize(150, 30)
        self.item_amount_input.setStyleSheet(INPUT_STYLE)
        self.item_amount_input.move(120, 140)

        item_description_label = QLabel("Description:", self)
        item_description_label.move(40, 185)
        self.item_description_input = QLineEdit(self)
        self.item_description_input.setFixedSize(150, 30)
        self.item_description_input.setStyleSheet(INPUT_STYLE)
        self.item_description_input.move(120, 180)

        # Category Dropdown
        self.category_label = QLabel("Category:", self)
        self.category_label.move(40, 220)
        self.category_combo = QComboBox(self)
        self.category_combo.setEditable(True)  # Make it editable
        self.category_combo.setFixedSize(150, 30)
        self.category_combo.setStyleSheet(INPUT_STYLE)
        self.category_combo.move(120, 210)
        self.category_combo.currentIndexChanged.connect(self.category_selected)

        # Buttons
        self.check_orders_button = QPushButton("Check Orders", self)
        self.check_orders_button.setFixedSize(135, 40)
        self.check_orders_button.setStyleSheet(BUTTON_STYLE)
        self.check_orders_button.move(50, 260)

        self.add_product_button = QPushButton("Add Product", self)
        self.add_product_button.setFixedSize(135, 40)
        self.add_product_button.setStyleSheet(BUTTON_STYLE)
        self.add_product_button.move(50, 310)

        self.update_product_button = QPushButton("Update Product", self)
        self.update_product_button.setFixedSize(135, 40)
        self.update_product_button.setStyleSheet(BUTTON_STYLE)
        self.update_product_button.move(50, 360)

        self.delete_product_button = QPushButton("Delete Product", self)
        self.delete_product_button.setFixedSize(135, 40)
        self.delete_product_button.setStyleSheet(BUTTON_STYLE)
        self.delete_product_button.move(50, 410)

        self.table = QTableWidget(self)
        self.table.setGeometry(350, 100, 400, 400)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Name", "Description", "Price", "Product ID", "Category"]
        )
        self.table.setStyleSheet("background-color: #C1B098;")
        if self.seller_id:
            self.load_products()
        else:
            self.table.setRowCount(0)
            QMessageBox.warning(
                self, "Error", "Invalid Seller ID.  Cannot load products."
            )

        self.check_orders_button.clicked.connect(self.check_orders)
        self.add_product_button.clicked.connect(self.add_product)
        self.update_product_button.clicked.connect(self.update_product)
        self.delete_product_button.clicked.connect(self.delete_product)

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setStyleSheet(BUTTON_STYLE)
        self.logout_button.move(670, 20)
        self.logout_button.clicked.connect(self.logout_function)

    def load_categories(self):
        """Loads category names from the database into the category combo box."""
        try:
            categories = get_all_categories()
            self.category_combo.clear()

            if categories:
                for category in categories:
                    self.category_combo.addItem(category[1])
            else:
                print("No categories found in the database.")
        except Exception as e:
            print(f"Error loading categories: {e}")
            QMessageBox.critical(
                self, "Database Error", "Failed to load categories."
            )

    def category_selected(self, index):
        """Handles the selection of a category from the combo box."""
        if index > 0:
            self.current_category_id = self.category_combo.itemText(index)
        else:
            self.current_category_id = None

    def load_products(self):
        """Loads products for the seller into the table."""
        try:
            if self.seller_id:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                                   SELECT p.Product_ID,
                                          p.Product_Name,
                                          p.Description,
                                          p.Price,
                                          c.Category_Name  FROM Products p    JOIN  Product_Categories pc ON p.Product_ID = pc.Product_ID   JOIN   Categories c ON pc.Category_ID = c.Category_ID WHERE p.Seller_ID = ?  ORDER BY p.Product_Name""",
                        (self.seller_id,),
                    )

                    products = cursor.fetchall()
                    self.table.setRowCount(0)

                    for product in products:
                        row_position = self.table.rowCount()
                        self.table.insertRow(row_position)
                        self.table.setItem(row_position, 0, QTableWidgetItem(product[1]))
                        self.table.setItem(row_position, 1, QTableWidgetItem(product[2]))
                        self.table.setItem(
                            row_position, 2, QTableWidgetItem(f"{product[3]:.2f}")
                        )
                        self.table.setItem(row_position, 3, QTableWidgetItem(product[0]))
                        self.table.setItem(row_position, 4, QTableWidgetItem(product[4]))
            else:
                self.table.setRowCount(0)
                QMessageBox.warning(
                    self, "Error", "Invalid Seller ID. Cannot load products."
                )

        except Exception as e:
            print(f"Error in load_products: {e}")
            QMessageBox.critical(
                self, "Database Error", "Failed to load products."
            )
            self.table.setRowCount(0)

    def get_category_name(self, category_name):
        """
        Retrieves the category name.

        Args:
            category_name (str): The name of the category.

        Returns:
            str: The name of the category, or "Unknown" if not found.
        """
        try:
            categories = get_all_categories()
            for category in categories:
                if category[1] == category_name:
                    return category[1]
            return "Unknown"
        except Exception as e:
            print(f"Error getting category name: {e}")
            return "Unknown"

    def check_orders(self):
        QMessageBox.information(
            self, "Check Orders", "Check Orders functionality will go here."
        )

    def add_product(self):
        """Adds a new product to the database and highlights it in the table."""
        try:
            name = self.item_name_input.text()
            description = self.item_description_input.text()
            try:
                price = float(self.item_amount_input.text())
            except ValueError:
                QMessageBox.warning(
                    self, "Error", "Invalid price format. Please enter a number."
                )
                return

            if not name or not description or not price:
                QMessageBox.warning(self, "Error", "All fields are required.")
                return

            product_id = "P" + uuid.uuid4().hex[:6].upper()
            category_text = self.category_combo.currentText()  # Get category text

            # Pass the category text to create_product
            create_product(
                product_id, self.seller_id, name, description, price, category_text
            )
            self.load_products()  # Reload products to include the new one

            # Find the row of the newly added product
            for row in range(self.table.rowCount()):
                if self.table.item(row, 3).text() == product_id:  # Product ID is unique
                    self.highlighted_row = row
                    break

            # Highlight the row
            self.highlight_row(self.highlighted_row)

            QMessageBox.information(self, "Success", "Product added successfully.")
            self.clear_input_fields()

        except ValueError as ve:  # Catch the ValueError from create_product
            QMessageBox.critical(self, "Category Error", str(ve))
        except Exception as e:
            print(f"Error in add_product: {e}")
            QMessageBox.critical(self, "Database Error", "Failed to add product.")

    def highlight_row(self, row):
        """Highlights a row in the table with a flash effect."""
        if row < 0 or row >= self.table.rowCount():
            return  # Invalid row

        original_bg_color = (
            self.table.item(row, 0).background().color()
        )  # get original color.
        highlight_color = QColor("#63B0CD")  # Yellow

        def restore_color():
            for col in range(self.table.columnCount()):
                self.table.item(row, col).setBackground(original_bg_color)

        def flash_color():
            for col in range(self.table.columnCount()):
                current_color = self.table.item(row, col).background().color()
                if current_color == original_bg_color:
                    self.table.item(row, col).setBackground(highlight_color)
                else:
                    self.table.item(row, col).setBackground(original_bg_color)

        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(flash_color)
        self.flash_timer.start(500)  # Flash every 500ms

        # Stop flashing after 2 seconds (4 flashes)
        QTimer.singleShot(2000, lambda: [self.flash_timer.stop(), restore_color()])

    def update_product(self):
        """Updates an existing product in the database."""
        try:
            selected_row = self.table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(
                    self, "Error", "Please select a product to update."
                )
                return

            product_id = self.table.item(selected_row, 3).text()
            name = self.item_name_input.text()
            description = self.item_description_input.text()
            try:
                price = float(self.item_amount_input.text())
            except ValueError:
                QMessageBox.warning(
                    self, "Error", "Invalid price format. Please enter a number."
                )
                return

            if not name or not description or not price:
                QMessageBox.warning(self, "Error", "All fields are required.")
                return

            update_product(product_id, name, description, price)
            self.load_products()
            QMessageBox.information(self, "Success", "Product updated successfully.")
            self.clear_input_fields()
        except Exception as e:
            print(f"Error in update_product: {e}")
            QMessageBox.critical(self, "Database Error", "Failed to update product.")

    def delete_product(self):
        """Deletes a product from the database."""
        try:
            selected_row = self.table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(
                    self, "Error", "Please select a product to delete."
                )
                return

            product_id = self.table.item(selected_row, 3).text()
            delete_product(product_id)
            self.load_products()
            QMessageBox.information(self, "Success", "Product deleted successfully.")
            self.clear_input_fields()
        except Exception as e:
            print(f"Error in delete_product: {e}")
            QMessageBox.critical(
                self, "Database Error", "Failed to delete product."
            )

    def clear_input_fields(self):
        """Clears the input fields after an operation."""
        self.item_name_input.clear()
        self.item_description_input.clear()
        self.item_amount_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.current_category_id = None

    def logout_function(self):
        set_current_user(None, None, None)
        self.close()
        self.main_window.show()

    def set_main_window(self, main_window):
        self.main_window = main_window


class ConsumerDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Consumer Dashboard")
        self.setFixedSize(800, 600)  # Changed to 800x600
        self.setWindowIcon(QIcon("C:\\Users\\Chris\\Downloads\\cubaoo.png"))
        self.setStyleSheet(f"background-color: {THEME_COLOR};")
        title = QLabel(f"Welcome Consumer, {username}!", self)
        title.setStyleSheet(
            f"color: {ACCENT_COLOR}; font-size: 24px; font-weight: bold;"
        )
        title.adjustSize()
        title.move(50, 50)

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setStyleSheet(BUTTON_STYLE)
        self.logout_button.move(650, 50)  # Adjusted position
        self.logout_button.clicked.connect(self.logout_function)

    def logout_function(self):
        set_current_user(None, None, None)
        self.close()
        self.main_window.show()

    def set_main_window(self, main_window):
        self.main_window = main_window


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Farmers Cubao")
        self.setFixedSize(800, 550)
        self.setStyleSheet(f"background-color: {THEME_COLOR};")
        self.setWindowIcon(QIcon("C:\\Users\\Chris\\Downloads\\cubaoo.png"))
        self.signup_window = None
        self.init_ui()
        self.admin_dashboard = None
        self.seller_dashboard = None
        self.consumer_dashboard = None

    def init_ui(self):
        self.image_label = QLabel(self)
        pixmap = QPixmap("C:\\Users\\Chris\\Downloads\\cubaoo.png").scaled(
            300, 300, Qt.AspectRatioMode.KeepAspectRatio
        )
        self.image_label.setPixmap(pixmap)
        self.image_label.adjustSize()
        self.image_label.move(250, 30)

        self.user_id_input = QLineEdit(self)
        self.user_id_input.setPlaceholderText("Please enter your username")
        self.user_id_input.setFixedSize(200, 30)
        self.user_id_input.setStyleSheet(INPUT_STYLE)
        self.user_id_input.move(300, 250)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Please enter your password")
        self.password_input.setFixedSize(200, 30)
        self.password_input.setStyleSheet(INPUT_STYLE)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.move(300, 300)

        self.login_button = QPushButton("Login", self)
        self.signup_button = QPushButton("Sign Up", self)

        button_style_main = f"""
            QPushButton {{
                background-color: {ACCENT_COLOR};
                color: {FONT_COLOR};
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 15px;
                font-weight: bold;
                border: {BORDER_WIDTH} solid {BORDER_COLOR};
            }}
            QPushButton:hover {{
                background-color: #cccccc;
            }}
        """
        self.login_button.setStyleSheet(button_style_main)
        self.signup_button.setStyleSheet(button_style_main)

        self.login_button.setFixedWidth(105)
        self.signup_button.setFixedWidth(105)

        self.login_button.move(290, 350)
        self.signup_button.move(410, 350)

        self.login_button.clicked.connect(self.login_function)
        self.signup_button.clicked.connect(self.signup_function)

    def signup_function(self):
        if self.signup_window is None:
            self.signup_window = SignUpWindow(self)
        self.signup_window.show()
        self.hide()

    def login_function(self):
        username = self.user_id_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(
                self, "Error!", "Please enter both username and password."
            )
            return

        user = login_user(username=username, password=password)
        if user:
            user_id_from_db = user[0]
            username = user[1]
            role = user[2]
            set_current_user(user_id_from_db, username, role)
            QMessageBox.information(self, "Success!", f"Welcome, {username} ({role})!")
            self.hide()

            # PANG OPEN NG DASHBOARDS DEPENDE KUNG ANONG TYPE OF USER SIYA
            if role.lower() == "admin":
                if self.admin_dashboard is None:
                    self.admin_dashboard = AdminDashboard(username)
                    self.admin_dashboard.set_main_window(self)
                self.admin_dashboard.show()
            elif role.lower() == "seller":
                if self.seller_dashboard is None:
                    self.seller_dashboard = SellerDashboard(username)
                    self.seller_dashboard.set_main_window(self)
                self.seller_dashboard.show()
            else:
                if self.consumer_dashboard is None:
                    self.consumer_dashboard = ConsumerDashboard(username)
                    self.consumer_dashboard.set_main_window(self)
                self.consumer_dashboard.show()
        else:
            QMessageBox.critical(
                self, "Login Failed!", "Invalid username or password."
            )

    def show_main_window(self):
        self.show()


class SignUpWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Sign Up")
        self.setFixedSize(450, 320)
        self.setStyleSheet(f"background-color: {THEME_COLOR};")
        self.setWindowIcon(QIcon("C:\\Users\\Chris\\Downloads\\cubaoo.png"))
        self.init_ui()

    def init_ui(self):
        self.title_label = QLabel("Create an Account", self)
        self.title_label.setStyleSheet(
            f"font-size: 20px; font-weight: bold; color: {ACCENT_COLOR};"
        )
        self.title_label.adjustSize()
        self.title_label.move((self.width() - self.title_label.width()) // 2, 20)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Create a username")
        self.username_input.setFixedSize(250, 30)
        self.username_input.setStyleSheet(INPUT_STYLE)
        self.username_input.move(100, 75)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setFixedSize(250, 30)
        self.password_input.setStyleSheet(INPUT_STYLE)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.move(100, 115)

        self.role_label = QLabel("Sign-up as?", self)
        self.role_label.setStyleSheet(f"color: {ACCENT_COLOR}; font-size: {FONT_SIZE};")
        self.role_label.adjustSize()
        self.role_label.move(100, 155)

        self.role_combo = QComboBox(self)
        self.role_combo.addItems(["Consumer", "Seller", "Admin"])
        self.role_combo.setStyleSheet(INPUT_STYLE)
        self.role_combo.setFixedSize(250, 30)
        self.role_combo.move(100, 175)

        self.signup_button = QPushButton("Submit", self)
        self.signup_button.setStyleSheet(BUTTON_STYLE)
        self.signup_button.adjustSize()
        self.signup_button.move(
            (self.width() - self.signup_button.width()) // 2, 250
        )
        self.signup_button.clicked.connect(self.submit_signup)

        self.back_button = QPushButton("🡸", self)
        self.back_button.setStyleSheet(BUTTON_STYLE)
        self.back_button.setFixedSize(50, 30)
        self.back_button.move((self.width() - self.back_button.width()) // 50, 10)
        self.back_button.clicked.connect(self.back_function)

    def back_function(self):
        self.hide()
        self.main_window.show()

    def submit_signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()

        if username == "" or password == "" or role == "":
            QMessageBox.warning(
                self, "I no no :(", "All fields must be filled to create an account!"
            )
            return

        user_id = "U" + uuid.uuid4().hex[:6].upper()

        success = signup_user(user_id, username, password, role)
        if success:
            QMessageBox.information(self, "wow! :)", "Account created successfully!")
        else:
            QMessageBox.warning(
                self, "Error", "Username already exists or account creation failed."
            )

        self.hide()
        self.main_window.show()

