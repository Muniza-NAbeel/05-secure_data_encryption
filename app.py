import streamlit as st
import hashlib
import os
import json
import time
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac

# **** Constants for data storage and security ****

DATA_FILE = 'secure_data.json'  # File for storing user data
SALT = b'secure_salt_value'    # Salt for hashing to enhance security
LOCKOUT_DURATION = 60          # Lockout duration in seconds after 3 failed attempts


# **** Initialize session state variables for user authentication ****

if 'authenticated_user' not in st.session_state:
    st.session_state.authenticated_user = None  # Track the logged-in user

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0       # Track failed login attempts

if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = 0          # Lockout time tracking

# **** Functions for data handling and security ****

# Load user data from JSON file
def load_data():
    if os.path.exists(DATA_FILE):  # Check if file exists
        with open(DATA_FILE, 'r') as f:
            return json.load(f)   # Load and return data from file
    return {}  # Return empty dictionary if file doesn't exist

# Save user data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)  # Write data to file in JSON format

# Generate a key for encryption based on a passkey
def generate_key(passkey):
    key = pbkdf2_hmac('sha256', passkey.encode(), SALT, 100000)  # Derive key using PBKDF2
    return urlsafe_b64encode(key)  # Encode key to make it safe for URLs

# Hash a password securely using PBKDF2
def hash_password(password):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100000).hex()  # Return hex hash

# Encrypt text using Fernet with a derived key
def encrypt_text(text, key):
    cipher = Fernet(generate_key(key))  # Create cipher object with derived key
    return cipher.encrypt(text.encode()).decode()  # Encrypt and return as string

# Decrypt encrypted text using Fernet with a derived key
def decrypt_text(encrypt_text, key):
    try:
        cipher = Fernet(generate_key(key))  # Create cipher object with derived key
        return cipher.decrypt(encrypt_text.encode()).decode()  # Decrypt and return original text
    except:
        return None  # Return None if decryption fails

# Load stored data at the start
stored_data = load_data()

# **** UI Navigation Bar ****

st.set_page_config(page_title="Secure Data Encryption System", page_icon="🔐")  # Set page title and icon

st.title("Secure Data Encryption System 🔐")  # Main title of the app
menu = ["Home", "Register", "Login", "Store Data", "Retrieve Data"]  # Navigation options
choice = st.sidebar.selectbox("Navigation", menu)  # Sidebar navigation menu

# **** Home Page ****
if choice == "Home":
    st.subheader("🔐 Welcome to the Secure Data Encryption System")  # Welcome message
    st.markdown("This Streamlit app is a Secure Data Encryption System enabling user registration, login, encrypted data storage, and retrieval.")  # App description
    st.markdown("Please log in or register to get started.")  # Instructions

# **** User Registration Page ****
elif choice == "Register":
    st.subheader("📝 Register New User")  # Page header
    username = st.text_input("Enter Username")  # Input for username
    password = st.text_input("Choose Password", type='password')  # Input for password
    confirm_password = st.text_input("Confirm Password", type='password')  # Input to confirm password

    if st.button("Register"):  # Button to register
        if username and password:  # Ensure both fields are filled
            if username in stored_data:  # Check if username already exists
                st.error("⚠️ Username already exists. Please choose a different one.")
            else:
                # Store user with hashed password and empty data
                stored_data[username] = {
                    "password": hash_password(password),
                    "data": []
                }
                save_data(stored_data)  # Save data to file
                st.success("✅ User registered successfully!")
        else:
            st.error("⚠️ Both fields are required.")

# **** User Login Page ****
elif choice == "Login":
    st.subheader("User Login 🔑")  # Page header

    # Check if lockout duration is active
    if time.time() < st.session_state.lockout_time:
        remaining = int(st.session_state.lockout_time - time.time())  # Calculate remaining lockout time
        st.error(f"⏲️ You are locked out for {remaining} seconds due to multiple failed attempts.")
        st.stop()

    username = st.text_input("Username")  # Input for username
    password = st.text_input("Password", type='password')  # Input for password

    if st.button("Login"):  # Button to log in
        if username in stored_data and stored_data[username]["password"] == hash_password(password):  # Validate credentials
            st.session_state.authenticated_user = username  # Set logged-in user
            st.session_state.failed_attempts = 0  # Reset failed attempts
            st.success(f"✅ Welcome, {username}!")
            st.session_state.lockout_time = 0  # Reset lockout time
        else:
            st.session_state.failed_attempts += 1  # Increment failed attempts
            remaining = 3 - st.session_state.failed_attempts  # Calculate remaining attempts
            st.error(f"⚠️ Invalid credentials. {remaining} attempts left.")

            if st.session_state.failed_attempts >= 3:  # Lockout after 3 failed attempts
                st.session_state.lockout_time = time.time() + LOCKOUT_DURATION  # Set lockout time
                st.error(f"⏲️ Too many failed attempts. You are locked out for {LOCKOUT_DURATION} seconds.")
                st.stop()

# **** Store Data Page ****
elif choice == "Store Data":
    if not st.session_state.authenticated_user:  # Ensure user is logged in
        st.error("⚠️ Please log in to store data.")
    else:
        st.subheader("🔒 Store Data")  # Page header
        data = st.text_area("Enter Data to Store")  # Input for data to store
        passkey = st.text_input("Enter Passkey", type='password')  # Input for passkey

        if st.button("Store Data"):  # Button to store data
            if data and passkey:  # Ensure both fields are filled
                encrypted = encrypt_text(data, passkey)  # Encrypt the data
                stored_data[st.session_state.authenticated_user]["data"].append(encrypted)  # Save encrypted data
                save_data(stored_data) # Save updated data to file
                st.success("✅ Data stored successfully!")
                st.balloons()  # Celebrate success
            else:
                st.error("⚠️ Both fields are required.")

# **** Retrieve Data Page ****
elif choice == "Retrieve Data":
    if not st.session_state.authenticated_user:  # Ensure user is logged in
        st.warning("⚠️ Please log in to retrieve data.")
    else:
        st.subheader("🔍 Retrieve Data")  # Page header
        user_data = stored_data.get(st.session_state.authenticated_user, {}).get("data", [])  # Get user-specific data

        if not user_data:  # Check if user has any data stored
            st.info("⚠️ No data found for the user.")
        else:
            st.write("🔒 Encrypted Data Entries:")  # Display stored encrypted data
            for i, item in enumerate(user_data):  # Iterate through data entries
                st.code(item, language="text")  # Display encrypted data

            encrypted_input = st.text_area("Enter Encrypted Text")  # Input for encrypted text to decrypt
            passkey = st.text_input("Enter Passkey to Decrypt", type='password')  # Input for decryption passkey

            if st.button("Decrypt"):  # Button to decrypt data
                result = decrypt_text(encrypted_input, passkey)  
                if result:  
                    st.success(f"✅ Decrypted Data: {result}")
                    st.balloons()
                else:
                    st.error("⚠️ Invalid passkey or corrupted data.")

# **** Footer ****
st.markdown("🔐 Secure Data Encryption System by Muniza Nabeel 💕 | Educational Project")  # Footer
st.markdown("📅 Date: 2025-04-14")  # Date of project completion