__author__ = 'jzimmermann'

from find_ideal_params import add_corr_to

import numpy as np
# input:

sim_result1 = {'params' : { 'K11' : 0.1, 'K12' : 0.2, 'K21' : 0.3 }, 'simfc': np.array([[1,5,3],[6,3,1],[9,4,2]])}
sim_result2 = {'params' : { 'K11' : 0.4, 'K12' : 0.5, 'K21' : 0.6 }, 'simfc': np.array([[99,5,2],[10,300,11],[90,42,211]])}
sim_result3 = {'params' : { 'K11' : 0.7, 'K12' : 0.8, 'K21' : 0.9 }, 'simfc': np.array([[2,2,5],[1,8,13],[9,42,21]])}
sim_results = [sim_result1, sim_result2, sim_result3]

empfc = np.array([[1,5,3],[6,3,1],[9,4,2]])


# output: was tested in matlab

sim_result1_out = {'params' : { 'K11' : 0.1, 'K12' : 0.2, 'K21' : 0.3 }, 'sim_emp_corr': 1.0}
sim_result2_out = {'params' : { 'K11' : 0.4, 'K12' : 0.5, 'K21' : 0.6 }, 'sim_emp_corr': -0.18729456105224754}
sim_result3_out = {'params' : { 'K11' : 0.7, 'K12' : 0.8, 'K21' : 0.9 }, 'sim_emp_corr': -0.10362087703138334}

updated_sim_results = add_corr_to(sim_results, empfc)
print updated_sim_results

