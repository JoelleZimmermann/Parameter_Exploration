__author__ = 'jzimmermann'

import unittest
from find_ideal_params import find_max_corr, find_sim_result_with_max_corr

sim_result1 = {'params' : { 'K11' : 0.1, 'K12' : 0.2, 'K21' : 0.3 }, 'sim_emp_corr': .65}
sim_result2 = {'params' : { 'K11' : 0.4, 'K12' : 0.5, 'K21' : 0.6 }, 'sim_emp_corr': .85}
sim_result3 = {'params' : { 'K11' : 0.7, 'K12' : 0.8, 'K21' : 0.9 }, 'sim_emp_corr': .75}

sim_results = [sim_result1, sim_result2, sim_result3]

max_corr = find_max_corr(sim_results)
sim_result = find_sim_result_with_max_corr(sim_results, max_corr)
ideal_params = sim_result['params']
print ideal_params

# def test_return_ideal_params():
#     max_corr = find_max_corr()
#     sim_result = find_sim_result_with_max_corr(max_corr)
#     ideal_params = return_ideal_params(sim_result)
#     unittest.TestCase().assertEqual(ideal_params, { 'K11' : 0.4, 'K12' : 0.5, 'K21' : 0.6 })

# test_return_ideal_params()
