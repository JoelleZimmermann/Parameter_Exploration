__author__ = 'jzimmermann'

from connectivity_from_file import from_file
from tvb.simulator.lab import *
import numpy
from collections import OrderedDict

class Subject_Simulation(object):

    # Simulation of one subject

    def __init__(self, subject):

        self.subject = subject

    # has functions to: runs simulations, comput FC from time series

    def prepare_and_run(self, what_to_watch, K11, K12, K21, simulation_length, period_length):

        # return: dict of parameters used in the calculation,
        #         and corresponding calculated time and series
        # return example for 10s simulation:
        # sim_result =
        #
        #   {
        #     'params' : { 'K11' : 0.1, 'K12' : 0.2, 'K21' : 0.3 },
        #     'time_with_regions_data' :
        #       { <- OrderedDict()
        #       500  : [1.1, 2.1 .. 68 regions ], <- throw away later, e.g till 0.4 - still returned
        #       ...
        #       1000  : [1.4, 2.4 .. 68 regions ], <- throw away later, e.g till 0.4 - still returned
        #
        #       1500  : [1.5, 2.5 .. 68 regions ], <- first returned
        #       2000  : [1.6, 2.6 .. 68 regions ],
        #       ...
        #       10000 : [1.10, 2.10 .. 68 regions ],
        #       },
        #     'simfc' :  array(    <- 68x68 # this third key val pair is added later in add_simfc_to
        #          0.2, 0.3 .. 68 regions]
        #          ...
        #          0.3, 0.4 .. 68 regions]
        #       ),
        #     'sim_emp_corr': .65
        #   }


        print "#################################################"
        print "Starting simulation with K11=", K11, " K12=", K12, " K21=", K21

        # oscillator = models.Generic2dOscillator(**pars) #change to SJ3D
        # oscillator = models.ReducedSetHindmarshRose(K11=0.1, K12=0.1,K21=0.1) # if running not inside loop
        oscillator = models.ReducedSetHindmarshRose(K11=K11, K12=K12, K21=K21) # Stefanescu-Jirsa


        # white_matter = connectivity.Connectivity(load_default=True)
        # white_matter = connectivity.Connectivity.from_file(source_file="/Users/jzimmermann/Documents/PHD_Thesis/Connectivity_zips/AJ_20140516_1600_Connectivity.zip", instance=None) ## source_file should be absolute path to connectivity.zip. If not, itll take the whole tvb path
        self.subject.empsc = from_file( source_file = self.subject.empsc_path, instance=None) ## source_file should be absolute path to connectivity.zip. If not, itll take the whole tvb path
        self.subject.empsc.speed = numpy.array([4.0])

        empsc_coupling = coupling.Linear(a=0.00390625 * 10 ** (-3)) #a = 0.033

        # Initialise an Integrator
        hiss = noise.Additive(nsig=numpy.array([2 ** -10, ])) # if i try with default value of nsig (=1.0), it overflows (nsig is D)
        heunint = integrators.HeunStochastic(dt=0.06103515625, noise=hiss) #dt is integration step size


        # Initialise a Simulator -- Model, Connectivity, Integrator, and Monitors.
        sim = simulator.Simulator(model=oscillator, connectivity=self.subject.empsc,
                                  coupling=empsc_coupling,
                                  integrator=heunint, monitors=what_to_watch)

        sim.configure()

        #Perform the simulation

        # bold_data = []
        # bold_time = []
        params_mapped_to_time_with_regions_data = {}
        params_mapped_to_time_with_regions_data['params'] = {'K11': K11, 'K12': K12, 'K21': K21}
        params_mapped_to_time_with_regions_data['time_with_regions_data'] = OrderedDict()

        LOG.info("Starting simulation...")
        for bold in sim(simulation_length):
            if bold is not None:
                # bold_time.append(bold[0][0])    # TODO:The first [0] is a hack for single monitor
                # bold_data.append(bold[0][1])    # TODO:The first [0] is a hack for single monitor
                params_mapped_to_time_with_regions_data['time_with_regions_data'].update({bold[0][0]:bold[0][1]})


        print params_mapped_to_time_with_regions_data
        return params_mapped_to_time_with_regions_data

