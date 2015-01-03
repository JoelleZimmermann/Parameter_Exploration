__author__ = 'jzimmermann'

from connectivity_from_file import from_file
from Subject import Subject
from Subject_Simulation import Subject_Simulation
import numpy
from itertools import product
from Ideal_Measure import FC_Ideal_Measure, Ideal_Measure
from remove_beg_of_ts import remove_beg_of_ts
from find_ideal_params import find_ideal_params_using_fc

# command line: to add current dir to python path: cd /Users/jzimmermann/Documents/PHD_Thesis/Python_stuff/My_tvb/Parameter_Exploration THEN import sys THEN sys.path.append('.')

'''
Usage for one subject
--------
'''

aa = Subject(id=None, age=None, empsc=None, empfc=None,
             empsc_path="/Users/jzimmermann/Documents/PHD_Thesis/Connectivity_zips/AA_20120815_Connectivity.zip",
             empfc_path="/Users/jzimmermann/Documents/PHD_Thesis/Emp_FC/AA_20120815_FC.mat") # created from FCM3D with Creating_subFC_matfiles_from_FCM3D.m

sub_sim = Subject_Simulation(subject = aa) # creating an instance of class Subject_Simulation = creating a new simulation

sim_results = [] # will hold a list of all the dictionaries, each dictionary represents one param combo and results

K11range = numpy.r_[.5:1:.5]
K12range = numpy.r_[0:1:1]
K21range = numpy.r_[1:2:1]
simulation_length_PE = 1500
simulation_length_sim = 2500
throwaway_length = 0

for (K11, K12, K21) in product(K11range, K12range, K21range):

    sim_result = sub_sim.prepare_and_run(K11=K11, K12=K12, K21=K21, simulation_length=simulation_length_PE)  #calling prepare_and_run for one combo of params, result will be a big dictionary

    sim_results.append( sim_result )

# final result of this loop will be list of dictionaries. each dictionary is a simulation with one parameter combo.

sim_results = remove_beg_of_ts(sim_results, throwaway_length)

#ideal_measure = FC_Ideal_Measure(sim_results = sim_results, empirical_results = aa.empfc)
#ideal_params = ideal_measure.find_ideal_params()

ideal_params = find_ideal_params_using_fc(sim_results, aa.empfc)

# run the sim with these ideal params we have identified:
sim_result_for_ideal_params = sub_sim.prepare_and_run(K11=ideal_params['K11'], K12=ideal_params['K12'], K21=ideal_params['K21'], simulation_length=simulation_length_sim)

print(sim_result_for_ideal_params) # prints sim_result of the ideal params.
