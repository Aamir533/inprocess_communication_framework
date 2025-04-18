import socket
import multiprocessing
from cryptography.fernet import Fernet
import os
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

HOST = '127.0.0.1'
PORT = 65432

# Load secret key with fallback
def load_secret_key():
    key = os.environ.get("IPC_SECRET_KEY")
    if not key:
        print("[WARNING] IPC_SECRET_KEY not found. Using default key (for testing only).")
        # This key is for development/testing ONLY. Replace or secure it in production!
        key = "3ncYJJkCdibdEEd2H3hnqBBiZMHrv3oQrKSIiGn-X9U="
    return Fernet(key.encode())

# Server process
def ipc_server(queue):
    fernet = load_secret_key()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Server] Listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print(f"[Server] Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    decrypted = fernet.decrypt(data).decode()
                    print(f"[Server] Received (decrypted): {decrypted}")
                    queue.put(("server_received", decrypted))  # Send decrypted message to the main thread

                    response = f"ACK: {decrypted}"
                    encrypted_response = fernet.encrypt(response.encode())
                    queue.put(("server_response", response))  # Send decrypted response
                    queue.put(("encrypted_response_server", encrypted_response.decode()))  # Send encrypted response

                    conn.sendall(encrypted_response)
                except Exception as e:
                    print("[Server] Error decrypting message:", e)

# Client process
def ipc_client(message, queue, fernet):
    time.sleep(0.1)  # Give the server a tiny head start
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            encrypted = fernet.encrypt(message.encode())
            s.sendall(encrypted)
            print(f"[Client] Sent (encrypted): {encrypted}")

            queue.put(("original_sent", message))
            queue.put(("encrypted_sent", encrypted.decode()))

            response = s.recv(1024)
            if response:
                decrypted_response = fernet.decrypt(response).decode()
                queue.put(("decrypted_response_client", decrypted_response))
                queue.put(("encrypted_response_client", response.decode()))
            else:
                queue.put(("error", "Server disconnected or sent no response."))
    except ConnectionRefusedError:
        queue.put(("error", "Connection to server refused. Ensure the server is running."))
    except Exception as e:
        queue.put(("error", f"Client error: {e}"))

# UI interaction
def send_message(message_entry, original_display, encrypted_sent_display, decrypted_response_display, encrypted_response_display, queue, fernet):
    message = message_entry.get()
    if message:
        message_entry.delete(0, tk.END)
        # Start the client process
        client_proc = multiprocessing.Process(target=ipc_client, args=(message, queue, fernet))
        client_proc.start()

# Update the UI with messages from the queue
def update_ui_from_queue(queue, original_display, encrypted_sent_display, decrypted_response_display, encrypted_response_display, server_received_display, server_response_display, encrypted_response_server_display, error_display):
    while not queue.empty():
        item_type, message = queue.get()

        if item_type == "original_sent":
            original_display.config(state=tk.NORMAL)
            original_display.insert(tk.END, f"Client: {message}\n")
            original_display.see(tk.END)
            original_display.config(state=tk.DISABLED)
        elif item_type == "encrypted_sent":
            encrypted_sent_display.config(state=tk.NORMAL)
            encrypted_sent_display.insert(tk.END, f"Client (Encrypted): {message}\n")
            encrypted_sent_display.see(tk.END)
            encrypted_sent_display.config(state=tk.DISABLED)
        elif item_type == "server_received":
            server_received_display.config(state=tk.NORMAL)
            server_received_display.insert(tk.END, f"Server Received: {message}\n")
            server_received_display.see(tk.END)
            server_received_display.config(state=tk.DISABLED)
        elif item_type == "decrypted_response_client":
            decrypted_response_display.config(state=tk.NORMAL)
            decrypted_response_display.insert(tk.END, f"Server Response: {message}\n")
            decrypted_response_display.see(tk.END)
            decrypted_response_display.config(state=tk.DISABLED)
        elif item_type == "encrypted_response_client":
            encrypted_response_display.config(state=tk.NORMAL)
            encrypted_response_display.insert(tk.END, f"Server Response (Encrypted): {message}\n")
            encrypted_response_display.see(tk.END)
            encrypted_response_display.config(state=tk.DISABLED)
        elif item_type == "server_response":
            server_response_display.config(state=tk.NORMAL)
            server_response_display.insert(tk.END, f"Server Response (Decrypted): {message}\n")
            server_response_display.see(tk.END)
            server_response_display.config(state=tk.DISABLED)
        elif item_type == "encrypted_response_server":
            encrypted_response_server_display.config(state=tk.NORMAL)
            encrypted_response_server_display.insert(tk.END, f"Server Response (Encrypted): {message}\n")
            encrypted_response_server_display.see(tk.END)
            encrypted_response_server_display.config(state=tk.DISABLED)
        elif item_type == "error":
            messagebox.showerror("Error", message)

    window.after(100, lambda: update_ui_from_queue(queue, original_display, encrypted_sent_display, decrypted_response_display, encrypted_response_display, server_received_display, server_response_display, encrypted_response_server_display, error_display))

# GUI setup
def setup_gui():
    fernet = load_secret_key()  # Load fernet object for encryption/decryption
    global window
    window = tk.Tk()
    window.title("Enhanced Secure IPC Chat")
    window.geometry("800x600")

    # Title
    title_label = tk.Label(window, text="Enhanced Secure IPC Chat", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # Frames for better organization
    client_frame = tk.LabelFrame(window, text="Client Communication", padx=5, pady=5)
    client_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    server_frame = tk.LabelFrame(window, text="Server Communication", padx=5, pady=5)
    server_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Client Section
    tk.Label(client_frame, text="Your Message:").pack(anchor="w")
    message_entry = tk.Entry(client_frame)
    message_entry.pack(fill=tk.X, pady=5)
    send_button = tk.Button(client_frame, text="Send", command=lambda: send_message(message_entry, original_sent_display, encrypted_sent_display, decrypted_response_display, encrypted_response_display, queue, fernet))
    send_button.pack(pady=5)

    tk.Label(client_frame, text="Original Sent Messages:").pack(anchor="w")
    original_sent_display = scrolledtext.ScrolledText(client_frame, height=5, state=tk.DISABLED)
    original_sent_display.pack(fill=tk.X, expand=True, pady=2)

    tk.Label(client_frame, text="Encrypted Sent Messages:").pack(anchor="w")
    encrypted_sent_display = scrolledtext.ScrolledText(client_frame, height=5, state=tk.DISABLED)
    encrypted_sent_display.pack(fill=tk.X, expand=True, pady=2)

    tk.Label(client_frame, text="Server Response (Decrypted):").pack(anchor="w")
    decrypted_response_display = scrolledtext.ScrolledText(client_frame, height=5, state=tk.DISABLED)
    decrypted_response_display.pack(fill=tk.X, expand=True, pady=2)

    tk.Label(client_frame, text="Server Response (Encrypted):").pack(anchor="w")
    encrypted_response_display = scrolledtext.ScrolledText(client_frame, height=5, state=tk.DISABLED)
    encrypted_response_display.pack(fill=tk.X, expand=True, pady=2)

    # Server Section
    tk.Label(server_frame, text="Server Received Messages (Decrypted):").pack(anchor="w")
    server_received_display = scrolledtext.ScrolledText(server_frame, height=5, state=tk.DISABLED)
    server_received_display.pack(fill=tk.X, expand=True, pady=2)

    tk.Label(server_frame, text="Server Response (Decrypted):").pack(anchor="w")
    server_response_display = scrolledtext.ScrolledText(server_frame, height=5, state=tk.DISABLED)
    server_response_display.pack(fill=tk.X, expand=True, pady=2)

    tk.Label(server_frame, text="Server Response (Encrypted):").pack(anchor="w")
    encrypted_response_server_display = scrolledtext.ScrolledText(server_frame, height=5, state=tk.DISABLED)
    encrypted_response_server_display.pack(fill=tk.X, expand=True, pady=2)

    # Error Display
    error_display = tk.Label(window, text="", fg="red")
    error_display.pack()

    # Start Server in a Background Process
    server_proc = multiprocessing.Process(target=ipc_server, args=(queue,))
    server_proc.daemon = True
    server_proc.start()

    # Periodically check the queue for new messages and update the UI
    update_ui_from_queue(queue, original_sent_display, encrypted_sent_display, decrypted_response_display, encrypted_response_display, server_received_display, server_response_display, encrypted_response_server_display, error_display)

    window.mainloop()

if __name__ == "__main__":
    # Queue for inter-process communication
    queue = multiprocessing.Queue()
    setup_gui()