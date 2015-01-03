__author__ = 'jzimmermann'

class Ideal_Measure(object):

    def __init__(self, sim_results, empirical_results):

        # expected format: list of result of Subject_Simulation.prepare_and_run() - for example, { params: {...}, { time1: simulated_FC_at_time1 } }
        self.sim_results = sim_results
        # expected format: equivalent to the simulated results in the previous argument - for example, empirical_FC
        self.empirical_results = empirical_results

    def find_ideal_params(self):
        #This def is just here to show that every subclass of Ideal_Measure (ie FC_Ideal_Measure), must have this definition
        # finds the sim data that represents the best match to empirical data
        # return:  Parameters that represent the best simulated/emptirical match
        # example: { K11: 0.1, K12: 0.2, K21 = 9.8 }

        return None

class FC_Ideal_Measure(Ideal_Measure):

    def find_ideal_params(self):
        # return: the ideal parameter values that creates best match btw sim and empirical FC
        #         Example:  { K11 : 0.1, K12 : 0.2, K21 : 0.3 }
        # TODO: RETRUN THE parameter values (ieK12 = 1; K21 = 2) KEY NOT THE VALUE (MATRIX)
        # return corr(param_with_sim_results.values() , empirical_results).abs().max()

        self.sim_results = add_simfc_to(self.sim_results)

        return self.sim_results[0]['params']