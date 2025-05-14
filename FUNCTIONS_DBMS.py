import pyodbc


DRIVER_NAME = "SQL Server"
SERVER_NAME = "Christian"
DATABASE_NAME = "Local_Farmers_Market"


connect = pyodbc.connect(
                    f'DRIVER={DRIVER_NAME};'
                    f'SERVER={SERVER_NAME};'
                    f'DATABASE={DATABASE_NAME};'
                    'Trusted_Connection=yes;'
                )

#=================================================SIGNUP FUNCTIONS=======================================================
def SignUp(Role_type,Username,User_pass):
    try:
        cursor = connect.cursor()
        current_id = cursor.execute("SELECT MAX(User_Id) FROM Users").fetchone()[0]

        if current_id:
            id = current_id + 1
        else:
            id = 1000


        query_stmt = "INSERT INTO Users (User_Id,Role_type,Username,User_pass) VALUES (?,?,?,?)"
        cursor.execute(query_stmt,(id,Role_type,Username,User_pass))
        connect.commit()


    except pyodbc.Error as ex:
        print(f'Failed to create account {ex}')

# ========================================LOGIN FUNCTIONS================================================================
def Login(user, password):
    try:
        cursor = connect.cursor()

        # Step 1: Check if user exists in Users table
        query_stmt = "SELECT * FROM Users WHERE Username = ? AND User_pass = ?"
        USER = cursor.execute(query_stmt, (user, password)).fetchone()

        if USER:
            user_id = USER[0]
            role_type = USER[1]
            username = USER[2]
            user_pass = USER[3]

            if role_type == "Consumer":
                # Check if exists in Consumers
                check = cursor.execute(
                    "SELECT * FROM Consumers WHERE Users_ID_FK = ?", (user_id,)
                ).fetchone()

                if not check:
                    cursor.execute("""
                        INSERT INTO Consumers (Users_ID_FK, Role_type, Username, User_pass)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, role_type, username, user_pass))
                    print("Inserted into Consumers table.")

            elif role_type == "Seller":
                # Check if exists in Sellers
                check = cursor.execute(
                    "SELECT * FROM Sellers WHERE User_ID_FK = ?", (user_id,)
                ).fetchone()

                if not check:
                    cursor.execute("""
                        INSERT INTO Sellers (User_ID_FK, Role_type, Username, User_pass)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, role_type, username, user_pass))
                    print("Inserted into Sellers table.")

            elif role_type == "Admin":
                # Check if exists in Admin
                check = cursor.execute(
                    "SELECT * FROM Admin WHERE User_ID_FK = ?", (user_id,)
                ).fetchone()

                if not check:
                    cursor.execute("""
                        INSERT INTO Admin (User_ID_FK, Role_type, Username, User_pass)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, role_type, username, user_pass))
                    print("Inserted into Admin table.")

            # Save all changes
            connect.commit()

            return USER

        else:
            print("User not found.")
            return None

    except pyodbc.Error as ex:
        print(f"Failed during login or role-based insertion: {ex}")
        return None

#================================================================Seller Functions========================================

def insert_product(user_id, product_name, description, price, quantity):
    cursor = connect.cursor()

    product_id = get_next_product_id()

    query = """
        INSERT INTO Products (Username, product_name, Description, Price, Quantity)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (product_id, user_id, product_name, description, price, quantity))
    conn.commit()



    try:
        cursor.execute(query, (User_ID, product_name, description, price, quantity))
        conn.commit()
        print("Product inserted successfully")
    except Exception as e:
        print("Error inserting product:", e)
    finally:
        cursor.close()
        conn.close()

def refresh(userID,userNAME):
    try:
        cursor = connect.cursor()
        query_stmt = "SELECT * FROM Products WHERE User_ID_FK = ? and Username = ?"
        products = cursor.execute(query_stmt,(userID,userNAME)).fetchall()

        return products



    except Exception as e:
        print("Error inserting product:", e)




def add_to_cart(userID,userNAME,item_name_entry,description_entry,quantity_entry,price_entry):

    prod = item_name_entry
    desc = description_entry
    quantity = quantity_entry
    price =price_entry

    print(prod)
    print(desc)
    print(quantity)
    print(price)
    if prod == "" or desc == "" or quantity == "" or price == "":
        return print("MISING ENTRIES")

    try:
        cursor = connect.cursor()

        current_id = cursor.execute("SELECT MAX(Product_ID) FROM Products").fetchone()[0]

        if current_id:
            id = current_id + 1
        else:
            id = 7000


        query_stmt = "INSERT INTO Products (Product_ID,User_ID_FK,Username,Product_Name,Description,Price,Quantity) VALUES (?,?,?,?,?,?,?)"

        cursor.execute(query_stmt,(int(id),int(userID),userNAME,prod,desc,quantity,price))
        connect.commit()

        if cursor.rowcount > 0:
            return True


    except Exception as e:
        print("Error inserting product:", e)


def update(Product_Name,Desc,Quan,Price):

    Quan = int(Quan)
    Price = int(Price)
    try:
        cursor = connect.cursor()

        query_stmt = "UPDATE Products SET Price = ?, Quantity = ? WHERE Product_Name = ? and Description = ?"
        cursor.execute(query_stmt,((Price,Quan,Product_Name,Desc)))
        connect.commit()

        if cursor.rowcount > 0:
            return True

    except Exception as e:
        print("Error inserting product:", e)


def Remove(Product_Name,Desc,Quan,Price):
    try:
        cursor = connect.cursor()

        query_stmt = "DELETE FROM Products WHERE Product_Name = ? and Description = ?"
        cursor.execute(query_stmt,(Product_Name,Desc))
        connect.commit()

        if cursor.rowcount > 0:
            return True

    except Exception as e:
        print("Error inserting product:", e)

'''
def add_to_cart():
    name = item_name_entry.get()
    description = description_entry.get()
    quantity_str = quantity_entry.get()

    if name and description and quantity_str:
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                messagebox.showerror("Input Error", "Quantity must be greater than zero!")
                return
            price = quantity * 10


            from db_functions import insert_product
            insert_product(userID, name, description, price, quantity)

            cart_items.append({"name": name, "description": description, "price": price, "quantity": quantity})
            update_cart_list()
            clear_entries()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid quantity. Please enter a valid number!")
    else:
        messagebox.showerror("Input Error", "All fields must be filled!")
'''

def delete_product(product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Products WHERE productID = ?", (product_id,))
        conn.commit()
        return "Product deleted successfully."
    except Exception as e:
        return str(e)
    finally:
        conn.close()

def get_last_inserted_product_id(seller_id, name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TOP 1 productID FROM Products
            WHERE sellerID = ? AND name = ?
            ORDER BY productID DESC
        """, (seller_id, name))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        return None
    finally:
        conn.close()


def get_next_product_id():
    cursor = connect.cursor()

    cursor.execute("SELECT MAX(Product_ID) FROM Products")
    current_id = cursor.fetchone()[0]

    if current_id:
        new_id = current_id + 1
    else:
        new_id = 500

    connect.close()
    return new_id

def refresh_market():
    pass

#========================================================Consumer Functions==========================================
def add_to_basket(Product_ID_FK,Product_Name, Price, Quantity):
    try:
        cursor = connect.cursor()

