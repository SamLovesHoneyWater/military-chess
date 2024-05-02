# -*- coding: utf-8 -*-
"""
Created on Thu May  2 01:15:50 2024

@author: Sammy
"""

import socket

def main():
    # Define the IP address and port of the receiver
    receiver_ip = '192.168.194.16'
    receiver_port = 14514

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the receiver
        s.connect((receiver_ip, receiver_port))

        while True:
            # Send data
            data = input("Enter message to send (type 'exit' to quit): ")
            if data.lower() == 'exit':
                break
            s.sendall(data.encode())
            print("Data sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        s.close()

if __name__ == "__main__":
    main()
