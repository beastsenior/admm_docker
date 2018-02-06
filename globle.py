import numpy as np
import math

#random seed
SEED = 1
# SEED = np.random.randint(50)
np.random.seed(SEED)

#topology parameter
POC = 0.3667 #probability of connection between two nodes

#admm parameter
ITER = 200
THETA = 0.1
RHO = 500.0
DD = 200  #dimension of data
ND = 100  #number of data
PNZ = 0.05  # percent of non zeros
# R = 0
L_TAU = [1,3,10,50]

#mode of admm, single machine, star cluster, multiple bridge. As mode_i send as int8 over socket, len(L_MODE) should less than 128.
# L_MODE = [\
# ['Lasso','SingleADMM'],\
# ['Lasso','StarADMM','random',L_TAU[0]],\
# ['Lasso','StarADMM','random',L_TAU[1]],\
# ['Lasso','StarADMM','random',L_TAU[2]],\
# ['Lasso','StarADMM','random',L_TAU[3]],\
# ['Lasso','BridgeADMM','complete',L_TAU[0]],\
# ]
L_MODE = [\
['Lasso','SingleADMM','all_batch'],\
['Lasso','SingleADMM','one_batch'],\
['Lasso','StarADMM','random',L_TAU[0]],\
['Lasso','BridgeADMM','complete',L_TAU[0]],\
]
#direction for saving data
DATA_DIR = './data/'

#command (0 -> 127 use to mode_i, -1 -> -128 use to command)
#for example: 
#sending np.int8(2).tostring to worker 7, means the command 'mode_i in worker 7 change to 2'
#sending np.int8(-2).tostring to bridge 10, means the command 'bridge 10 start'
D_COMMAND={'bridge reset':-1,'bridge start':-2,'bridge ready':-3,'worker ready':-4}

#network interface parameter
APORT=31500  #port of admin
BPORT=31501  #port of bridge
WPORT=31502  #port of worker

TOTAL_BUF=DD*8*2  #sending u and x with dtype=float64 needs DD*8*2 buffer
BUFSIZE = 512 #recvfrom(bufsize). The max value is about 64000.
NP=int((TOTAL_BUF+BUFSIZE-1)/BUFSIZE)  #number of packet
print('+++NP=', NP)

#ip list. (admin ip is 172.17.0.1, which is not in the list)
L_IP = [\
'172.17.0.2',  '172.17.0.3',  '172.17.0.4',  '172.17.0.5',  '172.17.0.6',  \
'172.17.0.7',  '172.17.0.8',  '172.17.0.9',  '172.17.0.10', '172.17.0.11', \
'172.17.0.12', '172.17.0.13', '172.17.0.14', '172.17.0.15', '172.17.0.16', \
'172.17.0.17']
IP_ADMIN = '172.17.0.1'  #admin machine IP
NN = len(L_IP)  # number of node
#ip dict. {0:'172.17.0.2,1:'172.17.0.3'...}
def ipdict():  #iplist to ipdict
	keys=range(NN)
	return dict(zip(keys, L_IP))
D_IP = ipdict()  

