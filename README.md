Enhanced Secure IPC Chat
Overview
The Enhanced Secure IPC Chat application is a Python-based inter-process communication (IPC) chat program that allows secure messaging between a client and a server. It utilizes encryption to ensure that messages sent over the network are secure and private.

Features
Secure Communication: Messages are encrypted using the cryptography library's Fernet symmetric encryption.
Multi-Process Architecture: The server and client run in separate processes, allowing for non-blocking communication.
Graphical User Interface (GUI): Built with Tkinter, the application provides a user-friendly interface for sending and receiving messages.
Message Logging: The application displays original messages, encrypted messages, and server responses (both decrypted and encrypted) in the GUI.
Requirements
Python 3.6 or higher
cryptography library
tkinter (comes pre-installed with Python)
Installation
Clone the repository or download the source code.

Navigate to the project directory.

Install the required dependencies by running:

pip install cryptography  
Set the environment variable for the secret key (optional):

export IPC_SECRET_KEY='your_secret_key_here'  
If the environment variable is not set, a default key will be used for testing purposes.

Usage
Run the application by executing the following command in your terminal:

python ipc_chat.py  
The server will start automatically in a background process.

Enter a message in the "Your Message" field and click the "Send" button.

The application will display:

The original message sent by the client.
The encrypted message sent to the server.
The server's decrypted response.
The server's encrypted response.
You can send multiple messages, and the application will log all communications in their respective sections.

Important Notes
The default encryption key provided in the code is for development and testing purposes only. It should be replaced with a secure key in a production environment.
Ensure that the server is running before attempting to send messages from the client.
Troubleshooting
If you encounter a "Connection refused" error, make sure the server is running.
Check for any exceptions in the console output for debugging purposes.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
This application uses the cryptography library for encryption.
The GUI is built using Tkinter, which is included with Python.
