import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from Experiment1_datapreperation import dataobject, get_optimal_data


''' 
DISCRETIZED ONE DIMENSIONAL LINEAR ADVECTION-DIFFUSION EQUATION

Experiment 1:
    Here we fix the highest acceptable error (2-norm/inf-norm) for the solution
    of the linear advection-diffusion equantion and look at all datapoints
    for which an integrator satisfies:
        - The maximal integration error is small enough 
        - The costs (matrix-vector multiplication) are minimal
    
    The integrators are
        - rk2... Runge-Kutta method of order 2
        - rk4... Runge-Kutta method of order 4
        - crankn... Crank-Nicolson method of order 2
        - expeuler... Exponential euler method of order 2, in this case EXACT
        
Note: We write expeuler, even though we only compute the matrix exponential
    function of the discretized matrix using expleja with single precision
    and fixed step size.
''' 

'''
Global plot parameters
'''
SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 16

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=MEDIUM_SIZE)  # fontsize of the figure title
plt.rcParams['lines.linewidth'] = 3

''' 
Load data
'''
with pd.HDFStore('Experiment1.h5') as hdf:
    keys = hdf.keys()
    dataobjdict = {key:dataobject(key) for key in keys}
#keys = [keys[k] for k in [2,3,1,0]] # Rearrange

''' 
CONFIG 
'''
maxerror = '1e-8'
errortype = 'rel_error_inf' #abs_error_2 rel_error_2, abs_error_inf
adv = 1e0 # Should be <= 1
dif = 1e0 # Should be <= 1
 
save = False # Flag: If true, figures will be saved as pdf
save_path = 'figures' + os.sep + 'Experiment1' + os.sep 

suptitle = r'Pe$\cdot\Delta x = $' + str(adv/dif)
#suptitle = 'Advection: ' + str(adv) + ', Diffusion: ' + str(dif)

def savefig(number, save=False):
    if save:
        plt.savefig(save_path + str(number) + ',err=' + maxerror
                    +',adv='+str(adv) + ',dif='+str(dif) + ".pdf"
                    , format='pdf', bbox_inches='tight', transparent=True)
        plt.close()

for key in keys:
    get_optimal_data(dataobjdict[key], float(maxerror), errortype, adv, dif)

'''
1.1 Plot matrix dimension (Nx) vs matrix-vector multiplications (mv)
'''
fig, ax = plt.subplots()
fig.suptitle(suptitle)
for key in keys:
    df = dataobjdict[key].optimaldata
    df.plot('Nx','mv', label=key[1:], ax=ax)
ax.set_title('Minimal costs for which error < ' + maxerror + ' is satisfied')
ax.set_xlabel('N')
ax.set_ylabel('Matrix-vector multiplications')
#ax.set_ylim([5e2,1.5e5])
ax.set_yscale('log')

savefig(1, save)


'''
1.2 Plot matrix dimension (Nx) vs optimal time step size (tau)
'''
fig, ax = plt.subplots()
fig.suptitle(suptitle)
for key in keys:
    df = dataobjdict[key].optimaldata
    df.plot('Nx','tau', label=key[1:], ax=ax)
CFLA = (1./np.array(df.Nx))*adv
CFLD = (1./np.array(df.Nx))**2/dif
ax.plot(df.Nx, CFLA, label="Adv. CFL",linestyle='--')
ax.plot(df.Nx, CFLD, label="Diff. CFL",linestyle='--')

ax.set_title('Optimal time step for which error < ' + maxerror + ' is satisfied')
ax.legend()
ax.set_xlabel('N')
ax.set_ylabel('Optimal time step')
ax.set_yscale('log')

savefig(2, save)
'''
1.3 Plot Matrix-vector multiplications (Nx) vs optimal time step size (tau)
'''
fig, ax = plt.subplots()
fig.suptitle(suptitle)
for key in keys:
    df = dataobjdict[key].optimaldata
    df.plot('mv','tau', marker = 'o', label=key[1:], ax=ax)
    for i,j in df.Nx.items():
        if j in [50,200,400]:
            ax.annotate('N=' + str(j), xy=(df.mv[i], df.tau[i]))


ax.set_title('Parameter for which error < ' + maxerror + ' is satisfied')
ax.legend()
ax.set_xlabel('Matrix-vector multiplications')
ax.set_ylabel('Optimal time step')
ax.set_ylim([1e-6,9.1e-2])
ax.set_xscale('log')
ax.set_yscale('log')

savefig(3, save)

'''
Experiment 1.4 (Bonus): 

Compute the error of the expleja method for varying matrix dimensions NxN.
Normally this would result would be almost exact, but in this case we fix the
number of substeps and assume single accuracy.
'''
fig, ax = plt.subplots(1, 1, sharex=True)
fig.suptitle(suptitle + '\n Single precision expleja')

data = dataobjdict['/expeuler'].data
data = data.loc[(data['adv'] == adv) & (data['dif'] == dif)
                & (data[errortype] <= 1)] 

for label, df in data.groupby('Nx'):
    if label%100 == 0:
        df.plot('Nt',errortype, ax=ax, label='N = ' + str(label))
ax.set_xlabel('Number of substeps')
if errortype == 'rel_error_inf':
    ax.set_ylabel('Relative error in maximum norm')
ax.set_xscale('log')
ax.set_yscale('log')

plt.subplots_adjust(hspace=0)

savefig(4, save)

'''
1.5 Plot matrix dimension (Nx) vs matrix-vector multiplications (mv)
'''
'''
fig, ax = plt.subplots()
fig.suptitle(suptitle)
for key in keys:
    df = dataobjdict[key].optimaldata
    df.plot('Nx','m', label=key[1:], ax=ax)
ax.set_title('Minimal costs for which error < ' + maxerror + ' is satisfied')
ax.set_xlabel('N')
ax.set_ylabel('Matrix-vector multiplications per timestep')
ax.set_ylim([0,100])

savefig(5, save)
'''