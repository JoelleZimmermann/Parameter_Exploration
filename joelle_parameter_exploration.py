__author__ = 'jzimmermann'

from connectivity_from_file import from_file
from Subject import Subject
from Subject_Simulation import Subject_Simulation
import numpy
from itertools import product
from Ideal_Measure import FC_Ideal_Measure, Ideal_Measure
from remove_beg_of_ts import remove_beg_of_ts
from find_ideal_params import find_ideal_params_using_fc
import pickle
from find_ideal_params import add_corr_to, add_simfc_to
# from tvb.simulator.lab import *
from tvb.simulator import monitors
from tvb.datatypes import equations

# command line: to add current dir to python path: cd /Users/jzimmermann/Documents/PHD_Thesis/Python_stuff/My_tvb/Parameter_Exploration THEN import sys THEN sys.path.append('.')

K11range = numpy.r_[.1:1:.5] # [.1:1:.3]
K12range = numpy.r_[.1:1:.5] # [.1:1:.3]
K21range = numpy.r_[.1:1:.5] # [.1:1:.3]
simulation_length_PE = 1000 # 60 sec
simulation_length_sim = 1500 #180sec
throwaway_length = 0 # 20000ms
period_length_bold = 500 # 2000 ms
period_length_subsample = 3.90625 #<-- 256Hz sampling frequency
linear_coupling = 0.00390625 * 10 ** (-3)
conduction_speed = 3.0


subject_ids = ['AA_20120815']

for subject_id in subject_ids:

    sub = Subject(id=subject_id, age=None, empsc=None, empfc=None,
                 empsc_path="/Users/jzimmermann/Documents/PHD_Thesis/Connectivity_zips/" + subject_id + "_Connectivity.zip",
                 empfc_path="/Users/jzimmermann/Documents/PHD_Thesis/Emp_FC/" + subject_id + "_FC.mat") # created from FCM3D with Creating_subFC_matfiles_from_FCM3D.m

    sub_sim = Subject_Simulation(subject = sub) # creating an instance of class Subject_Simulation = creating a new simulation

    sim_results = [] # will hold a list of all the dictionaries, each dictionary represents one param combo and results

    for (K11, K12, K21) in product(K11range, K12range, K21range):

        # what_to_watch = monitors.SubSample(period=period_length_subsample)
        what_to_watch = monitors.Bold(period=period_length_bold, hrf_kernel=equations.Gamma()) # Set hemodynamic response function (hrf) to gamma kernal rather than the voltera kernal
        sim_result = sub_sim.prepare_and_run(what_to_watch = what_to_watch, linear_coupling=linear_coupling, conduction_speed=conduction_speed,  K11=K11, K12=K12, K21=K21, simulation_length=simulation_length_PE, period_length=period_length_bold)  #calling prepare_and_run for one combo of params, result will be a big dictionary

        sim_results.append( sim_result )

    # final result of this loop will be list of dictionaries. each dictionary is a simulation with one parameter combo.

    sim_results = remove_beg_of_ts(sim_results, throwaway_length)

    #ideal_measure = FC_Ideal_Measure(sim_results = sim_results, empirical_results = sub.empfc)
    #ideal_params = ideal_measure.find_ideal_params()

    ideal_params = find_ideal_params_using_fc(sim_results, sub.empfc)
    # ideal_params = find_ideal_params_using_temp_subsample(sim_results, sub)

    what_to_watch = monitors.Bold(period=period_length_bold, hrf_kernel=equations.Gamma()) # Set hemodynamic response function (hrf) to gamma kernal rather than the voltera kernal

    # run the sim with these ideal params we have identified:
    sim_result_for_ideal_params = sub_sim.prepare_and_run(what_to_watch = what_to_watch, linear_coupling=linear_coupling, conduction_speed=conduction_speed, K11=ideal_params['K11'], K12=ideal_params['K12'], K21=ideal_params['K21'], simulation_length=simulation_length_sim, period_length=period_length_bold)

    sim_result_for_ideal_params = remove_beg_of_ts([sim_result_for_ideal_params], throwaway_length)[0]

    sim_result_for_ideal_params = add_simfc_to([sim_result_for_ideal_params])[0]                             # creates simFCs and adds the simfc key value (the third) pair to each sim_result

    sim_result_for_ideal_params = add_corr_to([sim_result_for_ideal_params], sub.empfc)[0]

    print(sim_result_for_ideal_params) # prints sim_result of the ideal params.

    # pickle.dump(sim_result_for_ideal_params,open(subject_id + '_sim_result.pickle','wb')) # saves sim_result_for_ideal_params for a subject in a file
    pickle.dump(sim_result_for_ideal_params,open(subject_id + '_sim_result_bold1500_bold2000_2.pickle','wb'))
    # b = pickle.load(open('AA_20120815_sim_result_with_corr.pickle','r'))