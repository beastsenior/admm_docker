import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

import database as db
import globle as g

def get_ac(Lmin, min):
	ac = np.zeros([g.ITER])
	for k in range(g.ITER):
		ac[k]=abs(Lmin[k]-min)/min
	return ac

def result(problem):
	print('\nResult:')
	if problem == 'Lasso':
		NORMx0, = db.load(['NORMx0'])
		print('NORMx0=',NORMx0)		

		d_Lmin = {}
		d_ac = {}
		d_t = {}
		for mode_i in range(len(g.L_MODE)):
			d_Lmin[mode_i], d_t[mode_i] = db.load(['Lmin','t'], mode_i)
			d_ac[mode_i] = get_ac(d_Lmin[mode_i], d_Lmin[0][g.ITER-1])
			print('mode_i :',mode_i)
			print('Lmin =',d_Lmin[mode_i][g.ITER-1])
			print('t =',d_t[mode_i][0],'--',d_t[mode_i][g.ITER-1])
			print('ac =',d_ac[mode_i][g.ITER-1])		
		
		fig = plt.figure()
		
		#Lmin vs. iter
		axes_Lmin = plt.subplot(221)
		axes_Lmin.cla()
		#plt.ylim(1.0e-16, 1.0e+16)
		plt.yscale('log')
		plt.xlim(-5, g.ITER+5)
		lineX = np.linspace(0, g.ITER, g.ITER)		
		for mode_i in range(len(g.L_MODE)):
			plt.plot(lineX, d_Lmin[mode_i], label=str(mode_i))
		plt.legend()
		
		#ac vs. iter
		axes_ac = plt.subplot(222)
		axes_ac.cla()
		plt.yscale('log')
		plt.xlim(-5, g.ITER+5)
		for mode_i in range(len(g.L_MODE)):
			plt.plot(lineX, d_ac[mode_i], label=str(mode_i))
		plt.legend()

		#Lmin vs. time
		axes_Lmin = plt.subplot(223)
		axes_Lmin.cla()
		plt.yscale('log')
		for mode_i in range(len(g.L_MODE)):
			lineX = d_t[mode_i]
			plt.plot(lineX, d_Lmin[mode_i], label=str(mode_i))
		plt.legend()
		
		plt.show()
