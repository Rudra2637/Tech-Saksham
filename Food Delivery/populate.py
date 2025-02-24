import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import datetime, timedelta, time


def populate_database(connection, database_name):
    cursor = connection.cursor()
    fake = Faker()

    try:
        cursor.execute(f"USE {database_name}")
        num_users = 50
        for _ in range(num_users):
            name = fake.name()
            email = fake.email()
            phone = fake.numerify(text="##########")
            address = fake.address()
            password = fake.password()

            insert_user_query = """
            INSERT INTO Users (name, email, phone, address, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_user_query, (name, email, phone, address, password))
        connection.commit()
        print(f"{num_users} Users inserted.")

        num_restaurants = 20
        cuisine_types = [
            "Italian",
            "Chinese",
            "Mexican",
            "Indian",
            "American",
            "Japanese",
            "Thai",
            "French",
            "Mediterranean",
            "Korean",
        ]
        for _ in range(num_restaurants):
            name = fake.company()
            address = fake.address()
            phone = fake.phone_number()
            cuisine_type = random.choice(cuisine_types)
            rating = round(random.uniform(1, 5), 2)  # Rating between 1 and 5
            is_active = random.choice([True, False])
            opening_hours = time(
                hour=random.randint(8, 11), minute=0, second=0
            )
            closing_hours = time(
                hour=random.randint(20, 23), minute=0, second=0
            )

            insert_restaurant_query = """
            INSERT INTO Restaurants (name, address, phone, cuisine_type, rating, is_active, opening_hours, closing_hours)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_restaurant_query,
                (
                    name,
                    address,
                    phone,
                    cuisine_type,
                    rating,
                    is_active,
                    opening_hours,
                    closing_hours,
                ),
            )
        connection.commit()
        print(f"{num_restaurants} Restaurants inserted.")

        cursor.execute("SELECT restaurant_id FROM Restaurants")
        restaurant_ids = [row[0] for row in cursor.fetchall()]

        num_menu_items = 100  # Total menu items across all restaurants
        categories = ["Appetizer", "Main Course", "Dessert", "Beverage", "Sides"]
        for _ in range(num_menu_items):
            restaurant_id = random.choice(restaurant_ids)
            name = fake.word() + " " + fake.word()  # e.g., "Spicy Noodles"
            description = fake.sentence()
            price = round(random.uniform(5, 50), 2)  # Price between 5 and 50
            category = random.choice(categories)
            is_available = random.choice([True, False])
            image_url = fake.image_url()

            insert_menu_item_query = """
            INSERT INTO Menu_Items (restaurant_id, name, description, price, category, is_available, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_menu_item_query,
                (
                    restaurant_id,
                    name,
                    description,
                    price,
                    category,
                    is_available,
                    image_url,
                ),
            )
        connection.commit()
        print(f"{num_menu_items} Menu Items inserted.")

        num_delivery_partners = 30
        vehicle_types = ["Bike", "Scooter", "Car", "Van"]
        for _ in range(num_delivery_partners):
            name = fake.name()
            phone = fake.phone_number()
            vehicle_type = random.choice(vehicle_types)
            is_available = random.choice([True, False])
            rating = round(random.uniform(1, 5), 2)

            insert_delivery_partner_query = """
            INSERT INTO Delivery_Partners (name, phone, vehicle_type, is_available, rating)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_delivery_partner_query,
                (name, phone, vehicle_type, is_available, rating),
            )
        connection.commit()
        print(f"{num_delivery_partners} Delivery Partners inserted.")

        cursor.execute("SELECT user_id FROM Users")
        user_ids = [row[0] for row in cursor.fetchall()]

        num_orders = 75
        order_statuses = [
            "pending",
            "confirmed",
            "preparing",
            "out_for_delivery",
            "delivered",
            "cancelled",
        ]
        payment_statuses = ["pending", "completed", "failed", "refunded"]
        payment_methods = ["cash", "credit_card", "debit_card", "upi", "wallet"]
        for _ in range(num_orders):
            user_id = random.choice(user_ids)
            restaurant_id = random.choice(restaurant_ids)
            # order_time = fake.date_time_between(start_date='-30d', end_date='now') # Orders within the last 30 days.  Better to use timedelta
            order_time = datetime.now() - timedelta(
                days=random.randint(0, 30)
            )  # Orders within last 30 days
            total_amount = round(random.uniform(10, 200), 2)
            status = random.choice(order_statuses)
            payment_status = random.choice(payment_statuses)
            payment_method = random.choice(payment_methods)

            insert_order_query = """
            INSERT INTO Orders (user_id, restaurant_id, order_time, total_amount, status, payment_status, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_order_query,
                (
                    user_id,
                    restaurant_id,
                    order_time,
                    total_amount,
                    status,
                    payment_status,
                    payment_method,
                ),
            )
        connection.commit()
        print(f"{num_orders} Orders inserted.")

        cursor.execute("SELECT order_id FROM Orders")
        order_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT item_id, price FROM Menu_Items")  # Need price too!
        menu_items = cursor.fetchall()  # Fetch all menu items and their prices
        menu_item_dict = {
            item[0]: item[1] for item in menu_items
        }  # create a dictionary {item_id: price}

        num_order_items = 150  # total
        for _ in range(num_order_items):
            order_id = random.choice(order_ids)
            item_id = random.choice(
                list(menu_item_dict.keys())
            )  # Get a random item_id from the keys
            item_price = menu_item_dict[item_id]  # Use the dictionary
            quantity = random.randint(1, 5)  # Quantity between 1 and 5
            special_instructions = (
                fake.sentence() if random.random() < 0.3 else None
            )

            insert_order_item_query = """
            INSERT INTO Order_Items (order_id, item_id, quantity, item_price, special_instructions)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_order_item_query,
                (order_id, item_id, quantity, item_price, special_instructions),
            )

        connection.commit()
        print(f"{num_order_items} Order Items inserted.")

        cursor.execute("SELECT partner_id FROM Delivery_Partners")
        partner_ids = [row[0] for row in cursor.fetchall()]

        num_deliveries = (
            50
        )
        delivery_statuses = [
            "assigned",
            "picked_up",
            "in_transit",
            "delivered",
            "cancelled",
        ]
        for _ in range(num_deliveries):
            order_id = random.choice(order_ids)
            partner_id = random.choice(partner_ids)

            pickup_time = None
            delivery_time = None
            delivery_status = random.choice(delivery_statuses)

            if delivery_status in ["picked_up", "in_transit", "delivered"]:
                cursor.execute(
                    "SELECT order_time FROM Orders WHERE order_id = %s", (order_id,)
                )
                order_time = cursor.fetchone()[
                    0
                ]
                pickup_time = order_time + timedelta(
                    minutes=random.randint(5, 30)
                )  # pickup 5-30 minutes after order.

            if delivery_status == "delivered":
                if pickup_time:  # Make sure pickup time is not none
                    delivery_time = pickup_time + timedelta(
                        minutes=random.randint(10, 60)
                    )  # deliver 10-60 min after pickup.
                else:  # if no pickup_time but the status is 'delivered'.
                    cursor.execute(
                        "SELECT order_time FROM Orders WHERE order_id = %s", (order_id,)
                    )
                    order_time = cursor.fetchone()[0]
                    delivery_time = order_time + timedelta(
                        minutes=random.randint(15, 90)
                    )
            delivery_fee = round(random.uniform(2, 10), 2)

            insert_delivery_query = """
            INSERT INTO Delivery (order_id, partner_id, pickup_time, delivery_time, delivery_status, delivery_fee)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_delivery_query,
                (
                    order_id,
                    partner_id,
                    pickup_time,
                    delivery_time,
                    delivery_status,
                    delivery_fee,
                ),
            )
        connection.commit()
        print(f"{num_deliveries} Deliveries inserted.")


        num_reviews = 60
        for _ in range(num_reviews):
            user_id = random.choice(user_ids)
            restaurant_id = random.choice(restaurant_ids)
            rating = random.randint(1, 5)  # Rating between 1 and 5
            comment = fake.paragraph()

            insert_review_query = """
            INSERT INTO Reviews (user_id, restaurant_id, rating, comment)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                insert_review_query, (user_id, restaurant_id, rating, comment)
            )
        connection.commit()
        print(f"{num_reviews} Reviews inserted.")

    except Error as e:
        print(f"Error populating database: {e}")
        connection.rollback()  # Rollback in case of any error
    finally:
        cursor.close()



host = "localhost"
user = "root"
password = "sa3394hil"
database_name = "food_delivery_system"


connection = mysql.connector.connect(host=host, user=user, password=password)
print("MySQL Database connection successful")

populate_database(connection, database_name)

connection.close()
print("Database populated and connection closed.")