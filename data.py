import numpy as np

import globle as g
import database as db

#create data and save data to database
def init_data(problem):
	if problem == 'Lasso':
		#create
		x0 = np.zeros([g.DD,1])
		num_non_zeros = int(g.PNZ * g.DD)   
		positions = np.random.randint(0, g.DD, num_non_zeros)
		for i in positions:
			#x[i] = np.random.random()* (1.0e+7)
			x0[i] = np.random.random()
		A = np.random.normal(0.0, 1.0, [g.NN*g.ND, g.DD])
		b = A.dot(x0) + np.random.normal(0.0, 0.1, [g.NN*g.ND,1])
		#b = A.dot(x0)
		
		#compute theta*|x0|_1
		NORMx0 = g.THETA * np.linalg.norm(x0, ord=1)
				
		#save A and b to database
		db.save({'NORMx0':NORMx0,'x0':x0,'A':A,'b':b})

		print('Non zeros data in x0: ')
		for i in positions:
			print('x0[%d]=%f'%(i,x0[i]))
	print('Init data...done! (%s)'%(problem))

def data(mode_i):
	if g.L_MODE[mode_i][0] == 'Lasso':
		if g.L_MODE[mode_i][1] == 'SingleADMM':
			A, b = db.load(['A','b'])
			db.save({'A':A,'b':b},mode_i)

		elif g.L_MODE[mode_i][1] == 'StarADMM' or g.L_MODE[mode_i][1] == 'BridgeADMM':			
			A, b = db.load(['A','b'])
			Ar=A.reshape([g.NN, g.ND, g.DD])
			br=b.reshape([g.NN, g.ND, 1])
			#save distributed A and b to database
			i = 0
			for ip in g.L_IP:
				db.save({'A':Ar[i], 'b':br[i]}, mode_i, ip)
				i+=1
