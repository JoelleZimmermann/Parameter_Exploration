__author__ = 'jzimmermann'
from collections import OrderedDict

def remove_beg_of_ts(sim_results, throwaway_length):

    for sim_result in sim_results:
        time_with_regions_data_dict = sim_result['time_with_regions_data']
        time_with_regions_data_truncated = OrderedDict()
        for key in time_with_regions_data_dict:
            if (key > throwaway_length):
                time_with_regions_data_truncated.update({key : time_with_regions_data_dict[key]})

        sim_result['time_with_regions_data'] = time_with_regions_data_truncated

    return sim_results # return the truncated version
