import time 

import data
import globle as g
import admm as ad
import topology as tp
import result 
import environment as env

env.init_environment('admin')
tp.init_topology()
data.init_data('Lasso')
for mode_i in range(len(g.L_MODE)):
	start_time=time.time()
	print('\nmode_i=%d (%s): start...'%(mode_i,str(g.L_MODE[mode_i])))
	
	tp.topology(mode_i)
	data.data(mode_i)
	ad.admm(mode_i)
	
	end_time=time.time()
	print('mode_i=%d (%s): done! (%f s)'%(mode_i,str(g.L_MODE[mode_i]),end_time-start_time))
	#input('press Enter to continue...')
result.result('Lasso')

	