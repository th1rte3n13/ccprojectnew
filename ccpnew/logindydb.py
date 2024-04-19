import streamlit as st
import mysql.connector

# Function to authenticate user
def authenticate(username, password):
    try:
        # Connect to MySQL database hosted on AWS RDS
        connection = mysql.connector.connect(
            host='ccproj.cjquiyiqg0o6.us-east-1.rds.amazonaws.com',
            user='admin',
            password='12345678',
            database='ccproj'
        )
        cursor = connection.cursor()

        # Check if user exists in the database
        query = "SELECT * FROM userdetails WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return True
        else:
            return False
    except mysql.connector.Error as error:
        st.error(f"Error: {error}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# Streamlit login page
def main():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.success("Logged in successfully!")
            # Add your code to redirect to the main app or dashboard
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()
