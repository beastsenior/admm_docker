import networkx as nx
import numpy as np

import globle as g

def save(d_data, mode_i=-1, ip=g.IP_ADMIN, problem='Lasso'):
	for name in d_data:
		file_name = g.DATA_DIR+str(name)+'_'+str(mode_i)+'_'+ip+'_'+problem
		if name == 'G':
			nx.write_gpickle(d_data[name], file_name)
		else:
			np.save(file_name, d_data[name])

def load(l_data, mode_i=-1, ip=g.IP_ADMIN, problem='Lasso'):
	l_return = []
	for name in l_data:
		file_name = g.DATA_DIR+str(name)+'_'+str(mode_i)+'_'+ip+'_'+problem
		if name == 'G':
			l_return.append(nx.read_gpickle(file_name))
		else:
			l_return.append(np.load(file_name+'.npy'))
	return l_return
