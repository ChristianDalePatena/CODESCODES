import pyodbc
import bcrypt
import uuid

DRIVER_NAME = "SQL Server"
SERVER_NAME = "Christian"
DATABASE_NAME = "FARMERS_FARMERS"

connection_string = f"""
    DRIVER={DRIVER_NAME};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""

def get_connection():
    """
    Establishes a connection to the SQL Server database.
    Returns:
        pyodbc.Connection: A connection object.
    """
    return pyodbc.connect(connection_string)

# ---------------------------------------------------------- User management -----------------------------------------------------------------------------------------------------

def create_users(user_id, username, password):
    """
    Creates a new user in the Users table.

    Args:
        user_id (str): The unique ID for the user.
        username (str): The username.
        password (str): The password (will be hashed).
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Users (Users_ID, Username, Password) VALUES (?, ?, ?)""",
                       (user_id, username, hashed_password.decode('utf-8')))
        conn.commit()

def get_user_by_username(username):
    """
    Retrieves a user from the Users table by username.

    Args:
        username (str): The username to search for.

    Returns:
        tuple: The user data as a tuple, or None if not found.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Username = ?", (username,))
        return cursor.fetchone()

def get_user_by_id(user_id):
    """
    Retrieves a user from the Users table by user ID.
    Args:
        user_id (str): the user's ID
    Returns:
        tuple: the user data or None
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Users_ID = ?", (user_id,))
        return cursor.fetchone()

def login_user(username=None, user_id=None, password=None):
    """
    Authenticates a user and retrieves their role.

    Args:
        username (str, optional): The username. Defaults to None.
        user_id (str, optional): The user ID. Defaults to None.
        password (str, optional): The password. Defaults to None.

    Returns:
        tuple: (user_id, username, role), or None if authentication fails.
    """
    if not password:
        return None

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            if username:
                cursor.execute("SELECT Users_ID, Username, Password FROM Users WHERE Username = ?", (username,))
            elif user_id:
                cursor.execute("SELECT Users_ID, Username, Password FROM Users WHERE Users_ID = ?", (user_id,))
            else:
                return None

            user = cursor.fetchone()
            if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                user_id = user[0]
                # Pang Identify ng role
                cursor.execute("""
                    SELECT r.Role_Name FROM Roles r JOIN User_Roles ur ON r.Role_ID = ur.Role_ID WHERE ur.User_ID = ?""", (user_id,))
                role_result = cursor.fetchone()
                role = role_result[0] if role_result else None
                return (user[0], user[1], role)
            else:
                return None
    except Exception as e:
        print("Login error:", e)
        return None


def assign_role_to_user(user_id, role_id):
    """
    Assigns a role to a user in the User_Roles table.

    Args:
        user_id (str): The user ID.
        role_id (str): The role ID.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO User_Roles (User_ID, Role_ID) VALUES (?, ?)", (user_id, role_id))
        conn.commit()

def get_user_role(user_id):
    """
    Retrieves the role of a user.

    Args:
        user_id (str): The user ID.

    Returns:
        str: The role name, or None if not found.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.Role_Name FROM Roles r  JOIN User_Roles ur ON r.Role_ID = ur.Role_ID  WHERE ur.User_ID = ?""", (user_id,))
        return cursor.fetchone()

def signup_user(user_id, username, password, role_name):
    """
    Creates a new user, assigns a role, and creates a role-specific record.

    Args:
        user_id (str): The unique user ID.
        username (str): The username.
        password (str): The password.
        role_name (str): The role name ('Consumer', 'Seller', or 'Admin').

    Returns:
        bool: True on success, False on failure.
    """
    user = get_user_by_username(username)
    user_by_id = get_user_by_id(user_id)

    if user or user_by_id:
        return False

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert new user
            cursor.execute("""
                INSERT INTO Users (Users_ID, Username, Password) VALUES (?, ?, ?)""",
                (user_id, username, hashed_password.decode('utf-8')))

            # Get or create role
            cursor.execute("SELECT Role_ID FROM Roles WHERE Role_Name = ?", (role_name,))
            role_result = cursor.fetchone()

            if not role_result:
                new_role_id = "R" + uuid.uuid4().hex[:6].upper()
                cursor.execute("INSERT INTO Roles (Role_ID, Role_Name) VALUES (?, ?)", (new_role_id, role_name))
                role_id = new_role_id
            else:
                role_id = role_result[0]

            # Assign role to user
            cursor.execute("INSERT INTO User_Roles (User_ID, Role_ID) VALUES (?, ?)", (user_id, role_id))

            # Create role-specific record
            if role_name.lower() == "consumer":
                consumer_id = "C" + uuid.uuid4().hex[:6].upper()
                cursor.execute("INSERT INTO Consumers (Consumer_ID, Users_ID, Customer_Name) VALUES (?, ?, ?)",
                               (consumer_id, user_id, username))

            elif role_name.lower() == "seller":
                seller_id = "S" + uuid.uuid4().hex[:6].upper()
                cursor.execute("INSERT INTO Sellers (Seller_ID, Users_ID, Seller_Name) VALUES (?, ?, ?)",
                               (seller_id, user_id, username))

            conn.commit()
            return True

    except Exception as e:
        print("Signup error:", e)
        if conn:
            conn.rollback()
        return False

# ---------------------------------------------------------- Session manager -----------------------------------------------------------------------------------

current_user = {"user_id": None, "username": None, "role": None}

def set_current_user(user_id, username, role):
    """
    Sets the current user's information.

    Args:
        user_id (str): The user ID.
        username (str): The username.
        role (str): The user's role.
    """
    current_user["user_id"] = user_id
    current_user["username"] = username
    current_user["role"] = role

def get_current_user():
    """
    Retrieves the current user's information.

    Returns:
        dict: A dictionary containing the user's ID, username, and role.
    """
    return current_user

# ---------------------------------------------------------- Seller manager -----------------------------------------------------------------------------------

def create_seller(seller_id, user_id, seller_name):
    """
    Creates a new seller record.

    Args:
        seller_id (str): The seller ID.
        user_id (str): The user ID.
        seller_name (str): The seller's name.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Sellers (Seller_ID, Users_ID, Seller_Name) VALUES (?, ?, ?)",
                       (seller_id, user_id, seller_name))
        conn.commit()

def get_seller_by_user_id(user_id):
    """
    Retrieves a seller record by user ID.

    Args:
        user_id (str): The user ID.

    Returns:
        tuple: The seller data, or None if not found.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sellers WHERE Users_ID = ?", (user_id,))
        return cursor.fetchone()

# ---------------------------------------------------------- Consumer manager ---------------------------------------------------------------------------------

def create_consumer(consumer_id, user_id, customer_name):
    """
    Creates a new consumer record.

    Args:
        consumer_id (str): The consumer ID.
        user_id (str): The user ID.
        customer_name (str): The consumer's name.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Consumers (Consumer_ID, Users_ID, Customer_Name) VALUES (?, ?, ?)",
                       (consumer_id, user_id, customer_name))
        conn.commit()

def get_consumer_by_user_id(user_id):
    """
    Retrieves a consumer record by user ID.

    Args:
        user_id (str): The user ID.

    Returns:
        tuple: The consumer data, or None if not found.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Consumers WHERE Users_ID = ?", (user_id,))
        return cursor.fetchone()

# ---------------------------------------------------------- Product manager ----------------------------------------------------------------------------------
def create_product(product_id, seller_id, name, desc, price, category_id):
    """
    Creates a new product and links it to a category via Product_Categories.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Check if the category_id exists in the Categories table
            cursor.execute("SELECT Category_ID FROM Categories WHERE Category_ID = ?", (category_id,))
            if cursor.fetchone() is None:
                # Option 1: Create the category if it doesn't exist
                # This is the suggested approach.
                new_category_name = category_id  # Or, derive a name if category_id is not the name
                new_category_id = "CAT" + uuid.uuid4().hex[:6].upper()
                cursor.execute("INSERT INTO Categories (Category_ID, Category_Name) VALUES (?, ?)", (new_category_id, new_category_name))
                category_id = new_category_id # Use the newly created category ID

                # Option 2:  Raise an error and require the user to create the category first.
                # raise ValueError(f"Category_ID '{category_id}' does not exist in the Categories table.  Please create the category first.")

                # Option 3:  Log the error and return.  The product will not be created.
                # print(f"Warning: Category_ID '{category_id}' does not exist. Product not created.")
                # return

            cursor.execute("""
                INSERT INTO Products (Product_ID, Seller_ID, Product_Name, Description, Price)
                VALUES (?, ?, ?, ?, ?)""",
                (product_id, seller_id, name, desc, price))

            cursor.execute("""
                INSERT INTO Product_Categories (Product_ID, Category_ID)
                VALUES (?, ?)""",
                (product_id, category_id))
            conn.commit()
    except ValueError as ve:
        print(f"Error in create_product: {ve}")
        #  Consider re-raising the exception or logging it.
        raise ve # Re-raise the exception so the caller knows.
    except Exception as e:
        print(f"Error in create_product: {e}")
        #  Consider re-raising the exception or logging it.
        raise e # Re-raise the exception so the caller knows.



def update_product(product_id, name, desc, price):
    """
    Updates an existing product.

    Args:
        product_id (str): The product ID.
        name (str): The new product name.
        desc (str): The new product description.
        price (float): The new product price.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Products SET Product_Name = ?, Description = ?, Price = ? WHERE Product_ID = ?""",
            (name, desc, price, product_id))
        conn.commit()

def delete_product(product_id):
    """
    Deletes a product from the Products table, handling potential errors.

    Args:
        product_id (str): The ID of the product to delete.

    Returns:
        bool: True if the product was successfully deleted, False otherwise.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            #  Important:  Delete from the Product_Categories table first.
            cursor.execute("DELETE FROM Product_Categories WHERE Product_ID = ?", (product_id,))
            cursor.execute("DELETE FROM Products WHERE Product_ID = ?", (product_id,))
            conn.commit()
            print(f"Product with ID '{product_id}' deleted successfully.")
            return True
    except Exception as e:
        print(f"Error in delete_product: {e}")
        conn.rollback()  #  Rollback the transaction on error
        return False

def get_products_by_seller(seller_id):
    """
    Retrieves all products for a given seller.

    Args:
        seller_id (str): The seller ID.

    Returns:
        list: A list of tuples, where each tuple represents a product.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.Product_ID, p.Seller_ID, p.Product_Name, p.Description, p.Price, c.Category_Name
            FROM Products p
            JOIN Product_Categories pc ON p.Product_ID = pc.Product_ID
            JOIN Categories c ON pc.Category_ID = c.Category_ID
            WHERE p.Seller_ID = ?""", (seller_id,))
        return cursor.fetchall()

def get_all_categories():
    """
    Retrieves all categories from the Categories table.

    Returns:
        list: A list of tuples, where each tuple contains (Category_ID, Category_Name).
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Category_ID, Category_Name FROM Categories")
            categories = cursor.fetchall()
            return categories
    except Exception as e:
        print(f"Error in get_all_categories: {e}")
        return []

def create_category(category_name):
    """
    Creates a new category in the Categories table.

    Args:
        category_name (str): The name of the new category.

    Returns:
        str: The newly generated Category_ID, or None if creation failed.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            category_id = "CAT" + uuid.uuid4().hex[:6].upper()
            cursor.execute("INSERT INTO Categories (Category_ID, Category_Name) VALUES (?, ?)", (category_id, category_name))
            conn.commit()
            return category_id
    except Exception as e:
        print(f"Error in create_category: {e}")
        return None
def get_all_products():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        query = '''
        SELECT 
            p.product_id,
            p.product_name,
            p.description,
            p.price,
            c.category_name,
            s.first_name + ' ' + s.last_name AS seller_name
        FROM Products p
        JOIN Product_Categories pc ON p.product_id = pc.product_id
        JOIN Categories c ON pc.category_id = c.category_id
        JOIN Sellers s ON p.seller_id = s.seller_id
        '''
        cursor.execute(query)
        products = cursor.fetchall()

        product_list = []
        for p in products:
            product_list.append({
                'product_id': p[0],
                'name': p[1],
                'description': p[2],
                'price': p[3],
                'category': p[4],
                'seller': p[5],
            })
        return product_list
    except Exception as e:
        print("Error retrieving all products:", e)
        return []
    finally:
        conn.close()






