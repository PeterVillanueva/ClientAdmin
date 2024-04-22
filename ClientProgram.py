import socket
import psutil
# Import customtkinter library
from customtkinter import CTk

def get_hardware_info():
    cpu_freq = psutil.cpu_freq().current
    memory_usage = psutil.virtual_memory().percent
    storage_usage = psutil.disk_usage('/').percent
    return cpu_freq, memory_usage, storage_usage


def connect_to_server():
    HOST = 'localhost'  # Replace with server IP if running on different machines
    PORT = 65432        # Define a port to connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock


def send_info(sock):
    cpu_freq, memory_usage, storage_usage = get_hardware_info()
    data = f"CPU Freq: {cpu_freq} MHz, Memory Usage: {memory_usage}%, Storage Usage: {storage_usage}%"
    sock.sendall(data.encode())


def main():
    sock = connect_to_server()
    send_info(sock)
    sock.close()

if __name__ == '__main__':
    main()
