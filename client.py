import socket
import threading
import time

def receive_messages(conn, board):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print("Received:", data.decode())
            time.sleep(0.1)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def main():
    # Define the IP address and port to listen on
    host_ip = '0.0.0.0'  # Listen on all available interfaces
    port = 14514

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the address and port
        s.bind((host_ip, port))

        # Listen for incoming connections
        s.listen(1)
        print("Listening for incoming connections...")

        # Accept a connection
        conn, addr = s.accept()
        print(f"Connection established from {addr}")

        # Start a thread to receive messages
        receive_thread = threading.Thread(target=receive_messages, args=(conn,))
        receive_thread.start()

        while True:
            # Send data
            data = input("Enter message to send (type 'exit' to quit): ")
            if data.lower() == 'exit':
                break
            conn.sendall(data.encode())
            print("Data sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection and socket
        conn.close()
        s.close()

if __name__ == "__main__":
    main()
