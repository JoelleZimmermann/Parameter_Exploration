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


    def prepare_and_run(self, what_to_watch, linear_coupling, conduction_speed, K11, K12, K21, simulation_length, period_length):

        # return: dict of parameters used in the calculation,
        #         and corresponding calculated time and series
        # return example for 10s simulation:
        # sim_result =
        #
        #   {
        #     'params' : { 'K11' : 0.1, 'K12' : 0.2, 'K21' : 0.3 , 'linear_coupling':.05, 'conduction_speed':80},
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
        oscillator = models.ReducedSetHindmarshRose(K11=K11, K12=K12, K21=K21, mu = 2.2) # Stefanescu-Jirsa


        # white_matter = connectivity.Connectivity(load_default=True)
        # white_matter = connectivity.Connectivity.from_file(source_file="/Users/jzimmermann/Documents/PHD_Thesis/Connectivity_zips/AJ_20140516_1600_Connectivity.zip", instance=None) ## source_file should be absolute path to connectivity.zip. If not, itll take the whole tvb path
        self.subject.empsc = from_file( source_file = self.subject.empsc_path, instance=None) ## source_file should be absolute path to connectivity.zip. If not, itll take the whole tvb path
        self.subject.empsc.speed = numpy.array([conduction_speed])

        empsc_coupling = coupling.Linear(a=linear_coupling) # a = 0.033


        # Initialise an Integrator
        # hiss = noise.Additive(nsig=numpy.array([2 ** -10, ])) # if i try with default value of nsig (=1.0), it overflows (nsig is D)
        hiss = noise.Additive(nsig=numpy.array([0.001]))
        heunint = integrators.HeunStochastic(noise=hiss, dt=0.05) # dt is integration step size, using default

        # Initialise a Simulator -- Model, Connectivity, Integrator, and Monitors.
        sim = simulator.Simulator(model=oscillator, connectivity=self.subject.empsc,
                                  coupling=empsc_coupling, conduction_speed=conduction_speed,
                                  integrator=heunint, monitors=what_to_watch)

        sim.configure()

        #Perform the simulation

        # bold_data = []
        # bold_time = []
        params_mapped_to_time_with_regions_data = {}
        params_mapped_to_time_with_regions_data['params'] = {'K11': K11, 'K12': K12, 'K21': K21, 'linear_coupling':linear_coupling, 'conduction_speed':conduction_speed}
        params_mapped_to_time_with_regions_data['time_with_regions_data'] = OrderedDict()

        LOG.info("Starting simulation...")
        for monitor_result in sim(simulation_length):
            if monitor_result is not None:
                # bold_time.append(monitor_result[0][0])    # TODO:The first [0] is a hack for single monitor
                # bold_data.append(monitor_result[0][1])    # TODO:The first [0] is a hack for single monitor
                monitor_result_key   = monitor_result[0][0]
                monitor_result_value = self.transform_monitor_result(monitor_result[0][1], what_to_watch)

                params_mapped_to_time_with_regions_data['time_with_regions_data'].update({monitor_result_key:monitor_result_value})

        print params_mapped_to_time_with_regions_data
        return params_mapped_to_time_with_regions_data


    def transform_monitor_result(self, monitor_result, what_to_watch):

        if isinstance(what_to_watch, monitors.Bold):
            return monitor_result
        elif isinstance(what_to_watch, monitors.SubSample):
            # tofo : pick up the first mode and first state and return
            # todo later : average all three
            # The monitor_result is is coming directly from TVB simulation at position [0][1].
            # The shape of monitor_result is like 2, 68,3 where:
            #     2 represents the variables_of_interest that were defined during the monitor creation.
            #     68 regions
            #     3 represents number of modes (what isa  mode?)
            #     belowe we sum all mode values, and average variables_of_interest
            monitor_result = np.sum(monitor_result,2)
            monitor_result = np.mean(monitor_result,0)
            return monitor_result
        else:
            raise Exception("Unprocessed monitor")


