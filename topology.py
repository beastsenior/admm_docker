import numpy as np
import networkx as nx

import database as db
import globle as g


#create topology
def init_topology():
	flag = False
	while(flag==False):
		#G = nx.gnp_random_graph(g.NN, g.POC, seed=g.SEED)	
		G = nx.gnp_random_graph(g.NN, g.POC)	
		flag = nx.is_connected(G) 
	nx.relabel_nodes(G, g.D_IP, False)
	for edge in G.edges():
		G.edges[edge]['weight'] = np.random.rand()
	db.save({'G':G}) 
	print('Init topology...done!')

def topology(mode_i):
	G, = db.load(['G'])
	if g.L_MODE[mode_i][0] == 'Lasso':
		if g.L_MODE[mode_i][1] == 'SingleADMM':
			db.save({'G':G},mode_i)
		elif g.L_MODE[mode_i][1] == 'StarADMM':
			if g.L_MODE[mode_i][2] == 'random':
				#star cluster graph: the weights of edges are based on the shortest path of G
				Gstar = nx.star_graph(g.NN-1) 
				Gstar = Gstar.to_directed()
				nx.relabel_nodes(Gstar, g.D_IP, False)
				Gstar.remove_edges_from(tuple(Gstar.in_edges([g.L_IP[0]])))	
				for edge in Gstar.edges():
					Gstar.edges[edge]['weight'] = nx.shortest_path_length(G, g.L_IP[0], edge[1], weight='weight')
				#make selfloops 
				Gstar.add_edges_from([(g.L_IP[0],g.L_IP[0], {'weight': 0.0})])
				db.save({'G':Gstar},mode_i)
		elif g.L_MODE[mode_i][1] == 'BridgeADMM':
			if g.L_MODE[mode_i][2] == 'complete':
				Gd = G.to_directed()	
				#make selfloops 
				l_nodes=list(Gd.nodes())
				d_w=[{'weight':0.0}]*nx.number_of_nodes(Gd)
				l_loops=zip(l_nodes,l_nodes,d_w)
				Gd.add_edges_from(l_loops)
				db.save({'G':Gd},mode_i)

#get all bridges and workers	
def get_bridges_workers(G):  
	l_bridge = []
	for edge in G.edges():
		l_bridge.append(edge[0])					
	l_worker = list(G.nodes())
	#remove repetition
	l_bridge = list(set(l_bridge))
	l_worker = list(set(l_worker))	
	return l_bridge, l_worker
	
#get own workers of ip
def get_ow(G, ip): 
	l_tmp = list(G.successors(ip))
	return l_tmp, len(l_tmp)
					
#get own bridges of ip
def get_ob(G, ip): 
	l_tmp = list(G.predecessors(ip))
	return l_tmp, len(l_tmp)	