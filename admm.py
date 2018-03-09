import numpy as np
import time 

import globle as g
import database as db
import command as c
import topology as tp

#soft thresholding operator, boyd paper P32
def sthresh(a, k):
    return np.sign(a) * np.maximum(0, np.absolute(a) - k)

def admm(mode_i):
	G, = db.load(['G'],mode_i)
	if g.L_MODE[mode_i][0] == 'Lasso':
		if g.L_MODE[mode_i][1] == 'SingleADMM':
			c.single_admm(mode_i)
			
		elif g.L_MODE[mode_i][1] == 'StarADMM' or g.L_MODE[mode_i][1] == 'BridgeADMM':
			#get bridges and workers
			l_bridge, l_worker = tp.get_bridges_workers(G)
			#send command to bridges and workers
			c.init_bridge(l_bridge,mode_i)  #init bridge frist to stop the last compute
			c.init_worker(l_worker,mode_i)
			c.start_bridge(l_bridge)
			all_Lmin = np.zeros([g.ITER])
			all_t = np.zeros([g.ITER])
			d_Lmin = {}
			d_t = {}
			for ip in l_bridge:
				d_Lmin[ip], d_t[ip] = db.load(['Lmin','t'],mode_i,ip)
				all_Lmin = all_Lmin + d_Lmin[ip]
				all_t = all_t + d_t[ip]
			mean_Lmin = all_Lmin/len(l_bridge)
			mean_t = all_t/len(l_bridge)
			db.save({'Lmin':mean_Lmin,'t':mean_t},mode_i)
		
		else:
			print('Error: out of L_MODE.')
			input()

#compute Lagrangian function value (equation (5) in paper 'Asynchronous Distributed ADMM for Large-Scale Optimization—Part I' )
def get_Lmin(xu,z,A,b,l_row):
	L = 0.0
	for ip in l_row:
		L = L + 0.5*(np.array((np.square(np.dot(A[ip], xu[ip][0])-b[ip]))).sum()) + g.RHO*np.dot(xu[ip][1].T,(xu[ip][0]-z))+0.5*g.RHO*(np.array((np.square(xu[ip][0]-z))).sum())
	L = L + g.THETA*np.linalg.norm(z,ord = 1)
	return L
			
def get_z(xu, l_row, nrow):
	sum = np.zeros([g.DD,1]) 
	for ip in l_row:
		sum = sum + xu[ip][0] + xu[ip][1]
	a = sum/nrow
	k = g.THETA/(g.RHO*nrow)
	return sthresh(a,k)	
	
def get_xu(x,u,z,l_rob,Q,Atb):
	sum = np.zeros([g.DD,1])
	for ip in l_rob:
		u[ip] = u[ip] + x - z[ip]
		sum = sum + z[ip] - u[ip]
	x = Q.dot(Atb + g.RHO * sum)
	xu = {}
	for ip in l_rob:
		xu[ip]=np.array([x,u[ip]])
	return x,u,xu

