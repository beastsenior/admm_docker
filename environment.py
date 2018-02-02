import os

import globle as g

#kill and mkdir
def init_environment(role):
	if role == 'admin':
		pida=os.popen("netstat -nlp | grep "+str(g.APORT)+" | awk '{print $6}' | awk -F'/' '{ print $1 }'")
		pid=pida.read()
		if len(pid) > 0: 
			os.popen('kill ' + pid)
		if os.path.isdir(g.DATA_DIR)!=True:
			os.mkdir(g.DATA_DIR)
		else:
			os.system('rm -r ./data')
			os.mkdir(g.DATA_DIR)	
	elif role == 'node':
		pidb=os.popen("netstat -nlp | grep "+str(g.BPORT)+" | awk '{print $6}' | awk -F'/' '{ print $1 }'")
		pidw=os.popen("netstat -nlp | grep "+str(g.WPORT)+" | awk '{print $6}' | awk -F'/' '{ print $1 }'")
		pid=pidb.read()+' '+pidw.read()
		if len(pid) > 1: 
			os.popen('kill ' + pid)
	else:
		print('Error: wrong environment role.')
		input()		
	print('Init environment...done!')
