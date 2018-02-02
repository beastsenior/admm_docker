import net_interface as ni
import globle as g
import numpy as np

def init_bridge(l_bridge,mode_i):
	print('Init bridges with mode_i=%d...'%mode_i)
	ser = ni.init_socket('admin')
	for ip in l_bridge:
		ser.sendto(np.int8(mode_i).tostring(),(ip,g.BPORT))
	l_ready_ip = []
	while(set(l_ready_ip)!=set(l_bridge)):
		r_msg, addr = ser.recvfrom(g.BUFSIZE)
		r_command = int(np.fromstring(r_msg,dtype=np.int8))
		if r_command == g.D_COMMAND['bridge ready']:
			l_ready_ip.append(addr[0])
	ser.close()
	print('All bridges are ready.')
	
def init_worker(l_worker,mode_i):
	print('Init workers with mode_i=%d...'%mode_i)
	ser = ni.init_socket('admin')
	for ip in l_worker:
		ser.sendto(np.int8(mode_i).tostring(),(ip,g.WPORT))
		print(ip)
	l_ready_ip = []
	while(set(l_ready_ip)!=set(l_worker)):
		r_msg, addr = ser.recvfrom(g.BUFSIZE)
		r_command = int(np.fromstring(r_msg,dtype=np.int8))
		if r_command == g.D_COMMAND['worker ready']:
			l_ready_ip.append(addr[0])
	ser.close()
	print('All workers are ready.')
	
def start_bridge(l_bridge):
	ser = ni.init_socket('admin')
	for ip in l_bridge:
		ser.sendto(np.int8(g.D_COMMAND['bridge start']).tostring(),(ip,g.BPORT))
	print('All bridges start. ADMM is running...')
	l_ready_ip = []
	while(set(l_ready_ip)!=set(l_bridge)):  
		r_msg, addr = ser.recvfrom(g.BUFSIZE)
		r_command = int(np.fromstring(r_msg,dtype=np.int8))
		if r_command == g.D_COMMAND['bridge ready']:
			l_ready_ip.append(addr[0])
	ser.close()
	print('All bridges have done.')

	