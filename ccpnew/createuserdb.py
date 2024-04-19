import streamlit as st
import mysql.connector

# Connect to MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="ccproj.cjquiyiqg0o6.us-east-1.rds.amazonaws.com",
            user="admin",
            password="12345678",
            database="ccproj"
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Check if username or email already exist in the database
def check_existing_user(username, email):
    connection = connect_to_database()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM userdetails WHERE username = %s OR email = %s", (username, email))
        result = cursor.fetchone()
        connection.close()
        if result:
            return True
    return False

# Create user page
def create_user_page():
    st.title("Create User")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email ID")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Create User"):
        if not full_name or not email or not username or not password:
            st.error("Please fill in all fields.")
        else:
            if not check_existing_user(username, email):
                connection = connect_to_database()
                if connection is not None:
                    cursor = connection.cursor()
                    try:
                        cursor.execute("INSERT INTO userdetails (fullname, email, username, password) VALUES (%s, %s, %s, %s)",
                                       (full_name, email, username, password))
                        connection.commit()
                        st.success("User created successfully!")
                    except mysql.connector.Error as err:
                        st.error(f"Error: {err}")
                    finally:
                        connection.close()
            else:
                st.error("Username or Email ID already exists!")

create_user_page()
