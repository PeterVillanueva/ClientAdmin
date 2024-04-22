import socket
import psutil

# Define the server IP and port
SERVER_HOST = '192.168.0.101' #
SERVER_PORT = 65432


def get_hardware_info():
    cpu_freq = psutil.cpu_freq().current
    memory_usage = psutil.virtual_memory().percent
    storage_usage = psutil.disk_usage('/').percent
    return cpu_freq, memory_usage, storage_usage


def send_info():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_HOST, SERVER_PORT))
            cpu_freq, memory_usage, storage_usage = get_hardware_info()
            data = f"CPU Freq: {cpu_freq} MHz, Memory Usage: {memory_usage}%, Storage Usage: {storage_usage}%"
            sock.sendall(data.encode())
            print("Data sent successfully!")
    except Exception as e:
        print(f"Error occurred while sending data: {e}")


def main():
    send_info()


if __name__ == '__main__':
    main()
