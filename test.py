import netifaces
import socket
import os
import numpy as np
import time
import sys

DD = 2000

#network interface parameter
SIP='172.16.100.1'
CIP='172.16.100.1'
SPORT=31500  
CPORT=31501  
BUFSIZE = DD*8*2 #recvfrom(bufsize)

#get host ip address
def get_local_ip(interface_name): 
	info = netifaces.ifaddresses(interface_name) 
	return info[netifaces.AF_INET][0]['addr']

#init socket
def init_socket(role):
	if role == 's':
		local_addr = (LOCAL_IP, SPORT) 	
		ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ser.bind(local_addr)
	elif role == 'c':
		local_addr = (LOCAL_IP, CPORT)  
		ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ser.bind(local_addr)
	else:
		print('Error: wrong socket role.')
		input()
	return ser

#local ip
LOCAL_IP = get_local_ip('eth1')

pid = os.fork()

#--------------------------------------------bridge---------------------------------------------
if pid==0:	
	ser = init_socket('s')
	print('server is running...')
	while(True):
		r_msg, addr = ser.recvfrom(BUFSIZE)
		print('server got data:',DD)
		r_data = np.fromstring(r_msg,dtype=data.dtype).reshape([DD])
		if np.array_equal(r_data, data) == True:
			print('GOOD!!')
		else:
			print('BAD!!')
		DD += 1
else:
	ser = init_socket('c')
	time.sleep(0.5)
	print('client is sending...')
	while(True):
		data=np.random.normal(0.0, 1.0, [DD*2]).reshape([DD,2])
		print(DD, sys.getsizeof(data))
		ser.sendto(data.tostring(),(SIP, SPORT))
		DD += 1
	
