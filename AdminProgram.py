import socket
import threading
from customtkinter import CTk, CTkEntry, CTkButton, CTkLabel
import mysql.connector

HOST = 'localhost'
PORT = 65432


class DatabaseManager:
	def __init__(self, host, user, password, database):
		self.host = host
		self.user = user
		self.password = password
		self.database = database

	def verify_credentials(self, username, password):
		try:
			db = mysql.connector.connect(
				host=self.host,
				user=self.user,
				password=self.password,
				database=self.database
			)
			cursor = db.cursor()

			sql = "SELECT * FROM users WHERE username = %s AND password = %s"
			cursor.execute(sql, (username, password))
			result = cursor.fetchone()

			cursor.close()
			db.close()

			return result is not None

		except mysql.connector.Error as err:
			print(err)
			return False


def handle_client(conn, addr, gui=None):
	data = conn.recv(1024).decode()
	info_parts = data.split(",")
	cpu_freq, memory_usage, storage_usage = None, None, None
	for part in info_parts:
		key, value = part.strip().split(":")
		if key == "CPU Freq":
			cpu_freq = float(value.split()[0])
		elif key == "Memory Usage":
			memory_usage = float(value.split()[0])
		elif key == "Storage Usage":
			storage_usage = float(value.split()[0])

	# Update GUI elements with parsed data
	gui.update_info(cpu_freq, memory_usage, storage_usage)

	conn.close()
	print(f"Client {addr} disconnected")


class HardwareMonitorServer:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((self.host, self.port))
		self.client_threads = []

	def start_server(self):
		self.server_socket.listen()
		print(f"Server listening on {self.host}:{self.port}")
		while True:
			conn, addr = self.server_socket.accept()
			print(f"Connected by {addr}")
			thread = threading.Thread(target=handle_client, args=(conn, addr))
			thread.start()
			self.client_threads.append(thread)


class AdminGUI(CTk):
	def __init__(self):
		super().__init__()
		self.title("ADMIN LOGIN")
		self.geometry("400x300")

		# Username label and entry
		self.username_label = CTkLabel(self, text="Username:")
		self.username_label.grid(row=0, column=0, padx=10, pady=10)
		self.username_entry = CTkEntry(self)
		self.username_entry.grid(row=0, column=1, padx=10, pady=10)

		# Password label and entry
		self.password_label = CTkLabel(self, text="Password:")
		self.password_label.grid(row=1, column=0, padx=10, pady=10)
		self.password_entry = CTkEntry(self, show="*")
		self.password_entry.grid(row=1, column=1, padx=10, pady=10)

		# Login button
		self.login_button = CTkButton(self, text="Login", command=self.login)
		self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

		# Login label
		self.login_label = CTkLabel(self, text="")
		self.login_label.grid(row=3, column=0, columnspan=2)

		# Hardware monitoring elements
		self.cpu_label = CTkLabel(self, text="CPU Freq: - MHz")
		self.cpu_label.grid(row=4, column=0, columnspan=2)
		self.memory_label = CTkLabel(self, text="Memory Usage: - %")
		self.memory_label.grid(row=5, column=0, columnspan=2)
		self.storage_label = CTkLabel(self, text="Storage Usage: - %")
		self.storage_label.grid(row=6, column=0, columnspan=2)

		# Initially hide hardware monitoring labels
		self.cpu_label.grid_forget()
		self.memory_label.grid_forget()
		self.storage_label.grid_forget()

		# Database manager
		self.db_manager = DatabaseManager(
			host="127.0.0.1",
			user="PeterVillanueva",
			password="villanueva12345",
			database="admin_panel"
		)

		# Hardware monitor server
		self.server = HardwareMonitorServer(HOST, PORT)

	def login(self):
		username = self.username_entry.get().strip()
		password = self.password_entry.get().strip()

		if self.db_manager.verify_credentials(username, password):
			# Hide login elements
			self.username_label.grid_forget()
			self.username_entry.grid_forget()
			self.password_label.grid_forget()
			self.password_entry.grid_forget()
			self.login_button.grid_forget()
			self.login_label.grid_forget()

			# Show hardware monitoring elements
			self.cpu_label.grid()
			self.memory_label.grid()
			self.storage_label.grid()

			# Start the hardware monitoring server
			threading.Thread(target=self.server.start_server).start()
		else:
			self.login_label.configure(text="Invalid username or password!")

	def update_info(self, cpu_freq, memory_usage, storage_usage):
		if cpu_freq is not None:
			self.cpu_label.configure(text=f"CPU Freq: {cpu_freq} MHz")
		if memory_usage is not None:
			self.memory_label.configure(text=f"Memory Usage: {memory_usage} %")
		if storage_usage is not None:
			self.storage_label.configure(text=f"Storage Usage: {storage_usage} %")


def main():
	gui = AdminGUI()
	gui.mainloop()


if __name__ == "__main__":
	main()
