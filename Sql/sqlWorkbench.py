import streamlit as st
import mysql.connector
import pandas as pd

# Set the page layout to wide
st.set_page_config(layout="wide")
st.title("MySQL Workbench")

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "connection" not in st.session_state:
    st.session_state["connection"] = None
if "db_connection" not in st.session_state:
    st.session_state["db_connection"] = None
if "query_results" not in st.session_state:
    st.session_state["query_results"] = None

def add_message(message, msg_type="success"):
    st.session_state["messages"].append((msg_type, message))
    # Keep only the last 2 messages
    if len(st.session_state["messages"]) > 2:
        st.session_state["messages"] = st.session_state["messages"][-2:]

def login_connection(host, user, password, port):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        if connection.is_connected():
            add_message("Connected to MySQL Server", "success")
            return connection
    except mysql.connector.Error as err:
        add_message(f"Error: {err}", "error")
    return None

def main_connection(host, user, password, database, port):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        if connection.is_connected():
            add_message(f"Connected to MySQL database: {database}", "success")
            return connection
    except mysql.connector.Error as err:
        add_message(f"Error: {err}", "error")
    return None

def fetch_databases(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SHOW DATABASES")
        results = cursor.fetchall()
        databases = [row[0] for row in results]
        return databases
    except mysql.connector.Error as err:
        add_message(f"Error: {err}", "error")
    finally:
        cursor.close()

def create_database(connection, database_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {database_name}")
        add_message(f"Database {database_name} created successfully", "success")
    except mysql.connector.Error as err:
        add_message(f"Error: {err}", "error")
    finally:
        cursor.close()

def execute_query(connection, query, limit=None):
    cursor = connection.cursor()
    try:
        # For SELECT queries, apply the selected limit
        if query.strip().lower().startswith("select") and limit:
            query = f"{query.strip()} LIMIT {limit}"
        cursor.execute(query)
        if not query.strip():
            add_message("Please enter a valid SQL query.", "warning")  
        elif cursor.description:
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            df = pd.DataFrame(results, columns=columns)
            st.session_state["query_results"] = df
            add_message(f"{query} executed successfully.", "info")
        else:
            connection.commit()
            st.session_state["query_results"] = None
            add_message(f"{query} executed successfully.", "info")
    except mysql.connector.Error as err:
        st.session_state["query_results"] = None
        add_message(f"Error: {err}", "error")
    finally:
        cursor.close()
    st.rerun()

def calculate_table_height(df, row_height=36, max_height=362):
    """Calculate the height of the table based on the number of rows."""
    num_rows = len(df)
    table_height = min(row_height * num_rows + 35, max_height)
    return table_height

# Layout: left column (35%) and right column (65%)
col1, col2 = st.columns([0.35, 0.65])

with col1:
    # --- Connection Section ---
    host = st.text_input("Enter Host", value="localhost")
    port = st.text_input("Enter Port", value="3306")
    user = st.text_input("Enter User", value="root")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        st.session_state["connection"] = login_connection(host, user, password, port)

    if st.session_state["connection"]:
        databases = fetch_databases(st.session_state["connection"]) or []
        col3, col4 = st.columns(2)
        with col3:
            database = st.selectbox("Select Existing Database", ["No Database Selected"] + databases)
            if st.button("Connect to Database"):
                if database == "No Database Selected":
                    add_message("Please select a valid database.", "warning")
                else:
                    st.session_state["db_connection"] = main_connection(host, user, password, database, port)
                    execute_query(st.session_state["db_connection"], f"USE {database}")
        with col4:
            new_database = st.text_input("Create and Select New Database")
            if st.button("Create Database"):
                if databases and new_database in databases:
                    add_message(f"Database {new_database} already exists, please select it from left panel.", "warning")
                elif not new_database:
                    add_message("Please enter a valid database name.", "warning")
                else:
                    create_database(st.session_state["connection"], new_database)
                    st.session_state["db_connection"] = main_connection(host, user, password, new_database, port)
                    execute_query(st.session_state["db_connection"], f"USE {new_database}")

    # --- Messages Container at Bottom Left ---
    st.markdown("---")
    st.subheader("Messages")
    for msg_type, msg in st.session_state.get("messages", []):
        if msg_type == "success":
            st.success(msg)
        elif msg_type == "error":
            st.error(msg)
        elif msg_type == "warning":
            st.warning(msg)
        else:
            st.info(msg)
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

with col2:
    # --- Query Execution Section ---
    if st.session_state["db_connection"]:
        query = st.text_area("Enter SQL Query", height=165)
        col5, col6, col7, col8 = st.columns([0.55, 0.60, 2, 1])
        with col8:
            limit = st.selectbox("Select Limit", ["Don't Limit", "Limit to 10 rows", "Limit to 50 rows", "Limit to 100 rows", "Limit to 200 rows", "Limit to 300 rows", "Limit to 500 rows"], index=3)
            limit_value = None
            if limit != "Don't Limit":
                limit_value = int(limit.split()[2])
        with col5:
            if st.button("Execute Query"):
                execute_query(st.session_state["db_connection"], query, limit=limit_value)
        with col6:
            if st.button("Show Databases"):
                execute_query(st.session_state["db_connection"], "SHOW DATABASES")
        with col7:
            current_database = st.session_state["db_connection"].database if st.session_state["db_connection"] else "Database"
            if st.button(f"Show Tables of {current_database}"):
                execute_query(st.session_state["db_connection"], "SHOW TABLES")
        
        # --- Output Section ---
        st.markdown("---")
        st.subheader("Query Results")
        if st.session_state["query_results"] is not None:
            table_height = calculate_table_height(st.session_state["query_results"])
            st.dataframe(st.session_state["query_results"], height=table_height, use_container_width=True)  # Set a dynamic height for the table
        else:
            st.info("No results to display.")
    else:
        st.markdown(
            """
            <div style='display: flex; align-items: center; justify-content: center; height: 100%; margin-top: 100px;'>
                <div style='text-align: center; font-size: 20px;'>
                    Please connect to a database to execute queries.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )