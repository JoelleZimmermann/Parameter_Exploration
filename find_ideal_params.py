__author__ = 'jzimmermann'

from fts_to_fc import add_simfc_to
import numpy as np

# todo write a test for this function
def add_corr_to(sim_results, empfc):
    for sim_result in sim_results:
        sim_result_sq = sim_result['simfc'].squeeze()
        if (empfc.size != sim_result_sq.size):
            raise Exception("empfc.size != sim_result_sq.size: empfc.size = " + str(empfc.size) + ", sim_result_sq.size=" + str(sim_result_sq.size))
        corr = np.corrcoef(np.reshape(empfc, (1,empfc.size)), np.reshape(sim_result_sq, (1,empfc.size)))[0,1] #bc corrcoef returns a matrix of corrs (2x2), we will return a single corr (top right)
        sim_result.update({'sim_emp_corr': corr})

    return sim_results

def find_max_corr(sim_results):
    the_corr_list = []
    for sim_result in sim_results:
        the_corr = sim_result['sim_emp_corr']
        the_corr_list.append(the_corr)

    max_corr = max(the_corr_list)
    return max_corr

# assume we know the max is 0.85
def find_sim_result_with_max_corr(sim_results, max_corr):
    for sim_result in sim_results:
        if sim_result['sim_emp_corr'] == max_corr:
            return sim_result

    return None # if we dont find any sim_emp_corr that == max_corr


def find_ideal_params_using_fc(sim_results, empfc): # will call functions above
    # return:          the ideal parameter values that creates best match btw sim and empirical FC
    # return example:  { K11 : 0.1, K12 : 0.2, K21 : 0.3 }

    sim_results = add_simfc_to(sim_results)                             # creates simFCs and adds the simfc key value (the third) pair to each sim_result

    sim_results = add_corr_to(sim_results, empfc)                       # updates sim_results dictionary with fourth keyval pair ('sim_emp_corr')

    max_corr = find_max_corr(sim_results)                               # go through sim_results and find max corr from the sim_emp_corr's
    sim_result = find_sim_result_with_max_corr(sim_results, max_corr)   # find the sim_result in sim_results that contains the max corr found above
    ideal_params = sim_result['params']                                 # get the param combo from the sim_result that contains the max corr

    return ideal_params
