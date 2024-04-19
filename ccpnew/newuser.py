import streamlit as st

def create_new_user():
    st.title("Create New User")
    
    # Add input fields for new user registration
    new_email = st.text_input("Email")
    new_full_name = st.text_input("Full Name")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # Logic to create a new user
    if st.button("Create User"):
        if new_password == confirm_password:
            # Here you can add logic to save the new user to the database
            st.success("User created successfully!")
            # Add a link to redirect to the login page
            st.markdown("User created successfully! [Return to Login Page](login.py)")
        else:
            st.error("Passwords do not match.")

def main():
    create_new_user()

if __name__ == "__main__":
    main()
