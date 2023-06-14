#!/bin/python3
import threading
import xmlrpc.client
import subprocess
import os
import shutil
from dotenv import load_dotenv


load_dotenv()
server_url = os.getenv('SERVERURL')
server = xmlrpc.client.Server(server_url)

# RUTORRENT PATHS
rtorrent = []
torrenthash = server.download_list("", "main")
def ru_paths():
	for i in torrenthash:
		if server.d.get_complete(i) == 1:
			i = "~" + server.d.base_path(i)
			#print("RU: " + i)
			rtorrent.append(i)

# HOST PATHS
def contractuser(path):
    return path.replace(os.path.expanduser('~'), '~', 1)

host = []
def host_paths():
	root = '~/data/downloads/complete/'
	root = os.path.expanduser(root)
	for name in os.listdir(root):
		path = os.path.join(root, name)
		if os.path.isdir(path):
			for inner_name in os.listdir(path):
				inner_path = os.path.join(path, inner_name)
				inner_path = contractuser(inner_path)
				#print("HOST: " + inner_path)
				host.append(inner_path)

# SCRIPT STARTS
thr1 = threading.Thread(target=ru_paths)
thr2 = threading.Thread(target=host_paths)

thr1.start()
thr2.start()

thr1.join()
thr2.join()

print()

set1 = set(rtorrent)
set2 = set(host)

unique_to_rtorrent = set1 - set2
unique_to_host = set2 - set1

for i in unique_to_host:
	print()
	print(i)
	i = os.path.expanduser(i)
	delete = input("Do you want to delete this file/directory? (yes/no): ")
	if delete.lower() == 'yes':
		try:
			if os.path.isfile(i):
				os.remove(i)
				print(f"File {i} has been deleted.")
			elif os.path.isdir(i):
				shutil.rmtree(i)
				print(f"Directory {i} has been deleted.")
			else:
				print(f"{i} is not a file or directory.")
		except FileNotFoundError:
			print(f"{i} was not found.")
		except PermissionError:
			print(f"Permission denied to delete {i}.")
		except Exception as e:
			print(f"Unable to delete {i} due to: {str(e)}")
