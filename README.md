# Enhanced Secure IPC Chat  

This project implements a secure inter-process communication (IPC) chat application using Python's socket programming, multiprocessing, and cryptography libraries. The application allows a client to send messages to a server securely, with both encrypted and decrypted message displays.  

## Features  

- Secure message encryption and decryption using the `cryptography` library.  
- Real-time communication between a client and a server using sockets.  
- A graphical user interface (GUI) built with Tkinter for easy interaction.  
- Displays original, encrypted, and decrypted messages for both client and server.  
- Error handling for connection issues.  

## Requirements  

- Python 3.x  
- `cryptography` library  
- `tkinter` (comes pre-installed with Python)  

## Installation  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/yourusername/enhanced-secure-ipc-chat.git  
   cd enhanced-secure-ipc-chat  
Install the required packages:

pip install cryptography  
Set the IPC_SECRET_KEY environment variable for production use:

export IPC_SECRET_KEY=your_secret_key_here  
If not set, a default key will be used (for testing purposes only).

Usage
Run the application:

python your_script_name.py  
The GUI will open, allowing you to enter messages in the "Your Message" field.

Click the "Send" button to send the message to the server.

View the original sent message, encrypted message, and server responses in their respective text areas.

How It Works
The server listens for incoming connections on 127.0.0.1:65432.
When a client connects, it can send messages that are encrypted before transmission.
The server decrypts the received messages, processes them, and sends back an acknowledgment that is also encrypted.
The GUI displays all relevant information, including original messages, encrypted messages, and decrypted server responses.
Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Cryptography - For secure encryption and decryption.
Tkinter - For building the GUI.

### Instructions for Use  
1. Replace `yourusername` in the clone URL with your GitHub username.  
2. Replace `your_script_name.py` with the actual name of your Python script file.  
3. Adjust any other sections as necessary to fit your project specifics.   

This README provides a clear and concise overview of your project, making it easy for othe
