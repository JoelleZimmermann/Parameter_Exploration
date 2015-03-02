import numpy
import matplotlib.pylab as plt
import pickle
import pandas as pd
numpy.set_printoptions(threshold=numpy.nan)
# Use this to visualize - need to fix to be generic

b = pickle.load(open('AA_20120815_sim_result_petras_lc14_cs80.pickle','r'))
arr = b['simfc']

# m = [[0.0, 1.47, 2.43, 3.44, 1.08, 2.83, 1.08, 2.13, 2.11, 3.7], [1.47, 0.0, 1.5,     2.39, 2.11, 2.4, 2.11, 1.1, 1.1, 3.21], [2.43, 1.5, 0.0, 1.22, 2.69, 1.33, 3.39, 2.15, 2.12, 1.87], [3.44, 2.39, 1.22, 0.0, 3.45, 2.22, 4.34, 2.54, 3.04, 2.28], [1.08, 2.11, 2.69, 3.45, 0.0, 3.13, 1.76, 2.46, 3.02, 3.85], [2.83, 2.4, 1.33, 2.22, 3.13, 0.0, 3.83, 3.32, 2.73, 0.95], [1.08, 2.11, 3.39, 4.34, 1.76, 3.83, 0.0, 2.47, 2.44, 4.74], [2.13, 1.1, 2.15, 2.54, 2.46, 3.32, 2.47, 0.0, 1.78, 4.01], [2.11, 1.1, 2.12, 3.04, 3.02, 2.73, 2.44, 1.78, 0.0, 3.57], [3.7, 3.21, 1.87, 2.28, 3.85, 0.95, 4.74, 4.01, 3.57, 0.0]]
m = [[0.0, 1.47, 2.43],[3.44, 1.08, 2.83],[ 1.08, 2.13, 2.11]]
# matrix = numpy.matrix(m)
# arr = numpy.array(m)

#df = pd.DataFrame(arr,index=['aa', 'bb', 'cc'],columns=['aa', 'bb', 'cc']) # array to dataframe

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_aspect('equal')

ax.tick_params(axis='both', direction='out')
# ax.set_xticks([0, 1, 2])
# ax.set_xticklabels(['aa', 'bb', 'cc'])
# ax.set_yticks([0, 1, 2])
# ax.set_yticklabels(['aa', 'bb', 'cc'])

ax.set_xticks(range(1,69)) # This is the size of your matrix!
ax.set_xticklabels(['BSTSL', 'CaudACinL', 'CaudMidFL', 'CunL', 'EntL', 'FusL', 'InfParL', 'ITL', 'IsthCinL', 'LOL', 'LOrbFL', 'LinL', 'MedOrbFL', 'MidTL', 'PHL', 'PCL', 'ParsOpL', 'ParsOrL', 'ParsTriL', 'PerCalL', 'PostCenL', 'PostCinL', 'PreCL', 'PreCunL', 'RAntCinL', 'RMidFL', 'SupFL', 'SupPL', 'SupTL', 'SupMarL', 'FPoleL', 'TPoleL', 'TranTL', 'InsL', 'BSTSR', 'CaudACinR', 'CaudMidFR', 'CunLR', 'EntR', 'FusR', 'InfParR', 'ITR', 'IsthCinR', 'LOR', 'LOrbFR', 'LinR', 'MedOrbFR', 'MidTR', 'PHR', 'PCR', 'ParsOpR', 'ParsOrR', 'ParsTriR', 'PerCalR', 'PostCenR', 'PostCinR', 'PreCR', 'PreCunR', 'RAntCinR', 'RMidFR', 'SupFR', 'SupPR', 'SupTR', 'SupMarR', 'FPoleR', 'TPoleR', 'TranTR', 'InsR'], rotation='vertical', fontsize='x-small')
ax.set_yticks(range(1,69))
ax.set_yticklabels(['BSTSL', 'CaudACinL', 'CaudMidFL', 'CunL', 'EntL', 'FusL', 'InfParL', 'ITL', 'IsthCinL', 'LOL', 'LOrbFL', 'LinL', 'MedOrbFL', 'MidTL', 'PHL', 'PCL', 'ParsOpL', 'ParsOrL', 'ParsTriL', 'PerCalL', 'PostCenL', 'PostCinL', 'PreCL', 'PreCunL', 'RAntCinL', 'RMidFL', 'SupFL', 'SupPL', 'SupTL', 'SupMarL', 'FPoleL', 'TPoleL', 'TranTL', 'InsL', 'BSTSR', 'CaudACinR', 'CaudMidFR', 'CunLR', 'EntR', 'FusR', 'InfParR', 'ITR', 'IsthCinR', 'LOR', 'LOrbFR', 'LinR', 'MedOrbFR', 'MidTR', 'PHR', 'PCR', 'ParsOpR', 'ParsOrR', 'ParsTriR', 'PerCalR', 'PostCenR', 'PostCinR', 'PreCR', 'PreCunR', 'RAntCinR', 'RMidFR', 'SupFR', 'SupPR', 'SupTR', 'SupMarR', 'FPoleR', 'TPoleR', 'TranTR', 'InsR'], fontsize='x-small')

plt.imshow(arr, interpolation='nearest', cmap=plt.cm.ocean)
plt.colorbar()
plt.show()

