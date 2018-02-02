import netifaces
import socket

import globle as g

#get host ip address
def get_local_ip():
	try:
		info = netifaces.ifaddresses('eth0')
	except:
		info = netifaces.ifaddresses('docker0')
	return info[netifaces.AF_INET][0]['addr']

#init socket
def init_socket(role):
	if role == 'admin':
		local_addr = (LOCAL_IP, g.APORT) 	
		ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ser.bind(local_addr)
	elif role == 'bridge':
		local_addr = (LOCAL_IP, g.BPORT)  
		ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ser.bind(local_addr)
	elif role == 'worker':
		local_addr = (LOCAL_IP, g.WPORT)  
		ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ser.bind(local_addr)
	else:
		print('Error: wrong socket role.')
		input()
	return ser

#local ip
LOCAL_IP = get_local_ip()