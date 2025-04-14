🔐 Secure Data Encryption System :

📌 Overview

This Secure Data Encryption System is a Streamlit-based Python application that allows users to:
✅ Register and Login securely
✅ Encrypt & Store sensitive data using AES-128 (Fernet Encryption)
✅ Decrypt stored data using a passkey
✅ Prevent brute-force attacks with 3-attempt lockout
✅ Persist data in a JSON file (no database required)

🚀 Features
🔐 Security Features
✔ PBKDF2 Password Hashing (SHA-256 + Salt)
✔ Fernet Encryption (AES-128) for stored data
✔ 3 Failed Attempts = 60-second Lockout
✔ Session Management (No unauthorized access)

📂 Data Management
✔ Multi-User Support (Each user has separate data)
✔ JSON Storage (Data persists after app restart)
✔ Encrypted Data Retrieval (Only with correct passkey)

🎨 User-Friendly UI
✔ Streamlit-Based Interface (Easy navigation)
✔ Success Animations (Balloons 🎈 on successful actions)
✔ Error Handling (Clear feedback for wrong inputs)

🛠 Installation & Setup
1. Install Required Libraries
bash
Copy
pip install streamlit cryptography
2. Run the Application
bash
Copy
streamlit run app.py
3. Access the App
Open http://localhost:8501 in your browser.

📝 How to Use?
1. Register a New User
Go to "Register" page

Enter a username and password

Click "Register"

2. Login to Your Account
Go to "Login" page

Enter your credentials

3 wrong attempts = 60-second lockout

3. Store Encrypted Data
Go to "Store Data"

Enter text and a passkey

Click "Store Data" (Encrypted & saved in JSON)

4. Retrieve Decrypted Data
Go to "Retrieve Data"

Enter encrypted text and passkey

Click "Decrypt" to see the original text

🎉 Ready to Use!
Run the app and start securing your data today! 🔒
