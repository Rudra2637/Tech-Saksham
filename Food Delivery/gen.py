import mysql.connector
from mysql.connector import Error


def create_database(host_name, user_name, user_password, db_name=None):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, password=user_password
        )
        print("MySQL Database connection successful")

        cursor = connection.cursor()

        if db_name:
            try:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                print(f"Database '{db_name}' created successfully or already exists.")
            except Error as e:
                print(f"Error creating database: {e}")
                return None

            cursor.execute(f"USE {db_name}")
            print(f"Using database '{db_name}'.")

        sql_script = """
        -- Create Users table
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            phone VARCHAR(50) NOT NULL,
            address TEXT NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_email (email)
        );

        -- Create Restaurants table
        CREATE TABLE IF NOT EXISTS Restaurants (
            restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            address TEXT NOT NULL,
            phone VARCHAR(50) NOT NULL,
            cuisine_type VARCHAR(50) NOT NULL,
            rating DECIMAL(3,2) DEFAULT 0.0,
            is_active BOOLEAN DEFAULT true,
            opening_hours TIME NOT NULL,
            closing_hours TIME NOT NULL,
            INDEX idx_cuisine (cuisine_type),
            INDEX idx_rating (rating)
        );

        -- Create Menu_Items table
        CREATE TABLE IF NOT EXISTS Menu_Items (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            restaurant_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            category VARCHAR(50) NOT NULL,
            is_available BOOLEAN DEFAULT true,
            image_url VARCHAR(255),
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
            INDEX idx_category (category),
            INDEX idx_restaurant (restaurant_id)
        );

        -- Create Delivery_Partners table
        CREATE TABLE IF NOT EXISTS Delivery_Partners (
            partner_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(50) NOT NULL UNIQUE,
            vehicle_type VARCHAR(50) NOT NULL,
            is_available BOOLEAN DEFAULT true,
            rating DECIMAL(3,2) DEFAULT 0.0,
            INDEX idx_availability (is_available)
        );

        -- Create Orders table
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            restaurant_id INT NOT NULL,
            order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(10,2) NOT NULL,
            status ENUM('pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled') DEFAULT 'pending',
            payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
            payment_method ENUM('cash', 'credit_card', 'debit_card', 'upi', 'wallet') NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
            INDEX idx_user (user_id),
            INDEX idx_restaurant_order (restaurant_id),
            INDEX idx_status (status),
            INDEX idx_order_time (order_time)
        );

        -- Create Order_Items table
        CREATE TABLE IF NOT EXISTS Order_Items (
            order_item_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            item_id INT NOT NULL,
            quantity INT NOT NULL,
            item_price DECIMAL(10,2) NOT NULL,
            special_instructions TEXT,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (item_id) REFERENCES Menu_Items(item_id),
            INDEX idx_order (order_id)
        );

        -- Create Delivery table
        CREATE TABLE IF NOT EXISTS Delivery (
            delivery_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            partner_id INT NOT NULL,
            pickup_time DATETIME,
            delivery_time DATETIME,
            delivery_status ENUM('assigned', 'picked_up', 'in_transit', 'delivered', 'cancelled') DEFAULT 'assigned',
            delivery_fee DECIMAL(6,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (partner_id) REFERENCES Delivery_Partners(partner_id),
            INDEX idx_order_delivery (order_id),
            INDEX idx_partner (partner_id),
            INDEX idx_delivery_status (delivery_status)
        );

        -- Create Reviews table
        CREATE TABLE IF NOT EXISTS Reviews (
            review_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            restaurant_id INT NOT NULL,
            rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
            INDEX idx_user_review (user_id),
            INDEX idx_restaurant_review (restaurant_id)
        );
        """

        for statement in sql_script.split(";"):
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except Error as e:
                    print(f"Error executing SQL statement: {e}\nStatement: {statement}")

        connection.commit()
        print("Tables created successfully.")

    except Error as e:
        print(f"The error '{e}' occurred")
        if connection:
            connection.rollback()
    finally:
        if connection:
            if connection.is_connected():
                cursor.close()

    return connection

host = "localhost"
user = "root"
password = "sa3394hil"
database_name = "food_delivery_system"

db_connection = create_database(host, user, password, database_name)

if db_connection:
    print("Database operation completed.")
    db_connection.close()
    print("Database connection closed.")