import streamlit as st
import numpy as np
import pickle
import mysql.connector
from functions import skills_names, prospects_dict
from career_desc2 import display_job_info
from data import finance_prospects_dict
from business import business_page  # Import the business_page function

# Load the trained model for the career prediction
loaded_model = pickle.load(open("technical.pkl", "rb"))

# Load the trained model for the finance page
loaded_model_finance = pickle.load(open("finance.pkl", "rb"))

# Define the skills and their names for the finance page
skills_names_finance = [
    "Ethical Conduct",
    "Leadership and Management",
    "Strategic Impact",
    "Communication and Presentation",
    "Analytical Skills",
    "Regulatory Compliance",
    "Risk Management",
    "Decision-Making Skills",
    "Continuous Learning",
    "Adaptability",
    "Financial Reporting",
    "Team Collaboration",
    "Client or Stakeholder Relationship Management",
    "Technology Proficiency",
    "Problem-Solving Skills",
]

# Define the pages
pages = [
    "Home",
    "Login",
    "Sign Up",
]  # Add "Business" to the list of pages

page = st.sidebar.selectbox("Select Page", pages)

# Function to display the home page content
def home_page():
    st.title("Career Prediction App - Home")

    # Add steps to use the app
    st.header("How to Use the App:")
    st.write("1. Choose a Domain")
    st.write("2. Adjust the skill levels using sliders in the sidebar.")
    st.write("2. Click the 'Predict' button.")
    st.write("3. View the predicted career.")



# Function to display the technical page content
def technical_page():
    st.title("Career Prediction App - Technical")

    st.sidebar.header("About the Skills")
    st.sidebar.info(
        "Use the sliders to input your skill levels (0-10). 0 means no knowledge, and 10 means expert level."
    )

    # Input for the user to enter skill levels
    user_skills = []
    for i, skill_name in enumerate(skills_names):
        user_input = st.sidebar.slider(f"{skill_name} (0-10)", 0, 10, 5)
        user_skills.append(user_input)

    # Button to make predictions
    predict_button_clicked = st.button("Predict Career")

    # Condition to display the steps only when the button is not clicked
    if not predict_button_clicked:
        # Add steps to use the app
        st.header("How to Use the App:")
        st.write("1. Adjust skill levels using the sliders in the sidebar.")
        st.write("2. Click the 'Predict Career' button.")
        st.write("3. View the predicted career.")

    # Condition to display the steps only when the button is clicked
    if predict_button_clicked:
        # Convert user input to NumPy array
        input_data = np.array(user_skills).reshape(1, -1)

        # Make predictions
        predictions = loaded_model.predict(input_data)
        probabilities = loaded_model.predict_proba(input_data)

        # Display predictions with increased and colorful font
        st.subheader("Predicted Career:")
        max_prob_index = np.argmax(probabilities)
        predicted_career = list(prospects_dict.keys())[max_prob_index]

        # HTML styling for increased font size and color
        styled_predicted_career = (
            f'<p style="font-size:34px; color:green;"><b>{predicted_career}</b></p>'
        )
        st.markdown(styled_predicted_career, unsafe_allow_html=True)

        # Display job information for the predicted career
        st.subheader("Job Information:")
        job_info = display_job_info(predicted_career)

        # Format and display job information
        for key, value in job_info.items():
            st.write(f"**{key}:** {value}")

        # Create an expander for detailed predictions
        with st.expander("Prediction Probabilities"):
            # Display probabilities
            for i, prob in enumerate(probabilities[0]):
                st.write(f"{list(prospects_dict.keys())[i]}: {prob * 100:.2f}%")

            # Display additional information based on probability threshold
            threshold = 5  # You can adjust this threshold
            selected_jobs = [
                list(prospects_dict.keys())[i]
                for i, prob in enumerate(probabilities[0])
                if prob > threshold / 100
            ]
            if selected_jobs:
                st.subheader("Potential Careers (Probability > 5%):")
                st.write(selected_jobs)
            else:
                st.subheader("No potential careers found.")


# Function to display the finance page content
def finance_page():
    st.title("Career Prediction App - Finance")

    st.sidebar.title("Finance Page - Skill Levels")
    st.sidebar.info(
        "Use the sliders to input your skill levels (1-10). 1 means low, and 10 means high."
    )

    # Input for the user to enter skill levels
    user_skills_finance = []
    for i, skill_name in enumerate(skills_names_finance):
        user_input = st.sidebar.slider(f"{skill_name} (1-10)", 1, 10, 5)
        user_skills_finance.append(user_input)

    # Button to make predictions
    predict_button_clicked_finance = st.button("Predict Roles")

    # Condition to display the steps only when the button is not clicked
    if not predict_button_clicked_finance:
        # Add steps to use the app
        st.header("How to Use the App:")
        st.write("1. Adjust skill levels using sliders in the sidebar.")
        st.write("2. Click the 'Predict Roles' button above.")
        st.write("3. View the predicted roles.")

    # Condition to display the steps only when the button is clicked
    if predict_button_clicked_finance:
        # Convert user input to NumPy array
        input_data_finance = np.array(user_skills_finance).reshape(1, -1)

        # Make predictions
        try:
            predictions_finance = loaded_model_finance.predict(input_data_finance)
            pred_proba_finance = loaded_model_finance.predict_proba(input_data_finance)

            # Display predictions with increased and colorful font
            st.subheader("Predicted Roles:")
            predicted_roles_finance = predictions_finance[0]
            styled_predicted_roles_finance = (
                f'<p style="font-size:34px; color:green;"><b>{predicted_roles_finance}</b></p>'
            )
            st.markdown(styled_predicted_roles_finance, unsafe_allow_html=True)

            # Display job information for the predicted role
            st.subheader(f"Job Information for {predicted_roles_finance}:")
            job_info = finance_prospects_dict.get(predicted_roles_finance, {})
            if job_info:
                for section, content in job_info.items():
                    st.subheader(section)
                    if isinstance(content, list):
                        for item in content:
                            st.write(item)
                    else:
                        st.write(content)
            else:
                st.write("Job information not available.")

            # Display prediction probabilities
            with st.expander("Prediction Probabilities"):
                # Display probabilities
                for i, prob in enumerate(pred_proba_finance[0]):
                    st.write(f"{loaded_model_finance.classes_[i]}: {prob * 100:.2f}%")

                # Display additional information based on probability threshold
                threshold_finance = 5  # You can adjust this threshold
                selected_roles_finance = [
                    loaded_model_finance.classes_[i]
                    for i, prob in enumerate(pred_proba_finance[0])
                    if prob > threshold_finance / 100
                ]
                if selected_roles_finance:
                    st.subheader("Potential Roles (Probability > 5%):")
                    st.write(selected_roles_finance)
                else:
                    st.subheader("No potential roles found.")
        except ValueError as e:
            st.error(f"Error during prediction: {e}")

def suggest():
    st.title("Welcome to the Prediction Page!")
    st.sidebar.title("Prediction")
    pages2 = ["Technical","Finance","Business"]  # Add "Business" to the list of pages
    page2 = st.sidebar.selectbox("Select Page", pages2)

    if page2 == "Technical":
        technical_page()
    elif page2 == "Finance":
        finance_page()
    elif page2 == "Business":  # Add this block for the Business page
        business_page()

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
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.success("Logged in successfully!")

            suggest()
            
        else:
            st.error("Invalid username or password")
        
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
def sign_up_page():
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




# Display content based on selected page

if page == "Home":
    home_page()
elif page == "Login":
    login_page()
elif page == "Sign Up":
    sign_up_page()


# Add an "About" section at the bottom of the main content area
st.markdown("## About This App")
st.info(
    "This web application predicts your career based on your inputted skill levels. "
    "Adjust the skill levels using the sliders, click the 'Predict Career' button, "
    "and explore the predicted career along with additional information and job prospects."
)

st.markdown("<div style='margin-bottom: 200px;'></div>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; font-size: 125%; color: #777;'>"
    "<i>Made by the <span><strong>MAX, SAVILLE AND VEDANT</strong></span></i></p>",
    unsafe_allow_html=True,
)
