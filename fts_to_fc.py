__author__ = 'jzimmermann'
import numpy as np

def time_with_regions_data_to_fts(sim_result):
    # Input: sim_result (but will be using the time_with_regions_data value in the dict

    # sim_result =
    #
    #   {
    #     'params' : { 'K11' : 0.1, 'K12' : 0.2, 'K21' : 0.3 },
    #     'time_with_regions_data' :
    #       { <- OrderedDict
    #       0.1  : [1.1, 1.3 .. 68 regions ], <- throw away later, e.g till 0.4 - still returned
    #       ...
    #       0.4  : [1.2, 2.3 .. 68 regions ]
    #      }
    #   }

    # Output: fts which is type of np.array() (is same object as input of fts_to_fc)

    fts = np.array(sim_result['time_with_regions_data'].values()) # creates an array out of all the vals of the time_with_regions data (does not include keys (ie the time ie .1)
    return fts


def fts_to_fc(fts):
    # Input: ts of regions - ndarray(611, 68
    #        R1  R2     R68
    #       1.1, 1.3 .. 68 regions ,
    #       1.2, 2.3 .. 68 regions ,
    #       ...
    #       2.2, 2.4 .. 68 regions ,
    #

    # Output: FC matrix - same as sim_result['simfc'] - array(68x68)
    #
    #       1, 0.3 .. 68 regions
    #       ...
    #       0.3, 1 .. 68 regions
    #
    fts = np.squeeze(fts)
    fc = np.corrcoef(fts.T) # given fts, calculates fc matrix, Transpose needed bc numpy corrcoeffs works row-wise (time series in rows)

    return fc

def add_simfc_to(sim_results):

    # Input: sim_results, without simfc matrices
    # Ouput: sim_results, with simfc matrices (as third key and value)

    # Will call 2 functions above

    for sim_result in sim_results:
        fts = time_with_regions_data_to_fts(sim_result)
        simfc = fts_to_fc(fts)
        sim_result.update({'simfc': simfc})

    return sim_results
