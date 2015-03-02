__author__ = 'jzimmermann'

from tvb.simulator.lab import *

from tvb.basic.readers import ZipReader, try_get_absolute_path

def from_file(source_file="nonexistent.zip", instance=None):
    '''
    Borrowed from connectivity.Connectivity - copied here and modified to match filesnames of Berlin connectivity .txts in connectivity.zip (ie orientation.txt rather than average_orientations.txt)
    :param source_file:
    :param instance:
    :return: Connectivity object from source_file.
    '''

    if instance is None:
        result = connectivity.Connectivity()
    else:
        result = instance

    source_full_path = try_get_absolute_path("tvb_data.connectivity", source_file)

    reader = ZipReader(source_full_path)

    # Working with original files from Petra.
    # result.areas         = reader.read_array_from_file("area")
    # result.region_labels = reader.read_array_from_file("centres", dtype=numpy.str, use_cols=(0,))
    # result.centres       = reader.read_array_from_file("centres", use_cols=(1, 2, 3))
    # result.cortical      = reader.read_array_from_file("cortical", dtype=numpy.bool)
    # result.hemispheres   = reader.read_array_from_file("hemisphere", dtype=numpy.bool)
    # result.orientations  = reader.read_array_from_file("orientation")
    # result.tract_lengths = reader.read_array_from_file("tract")
    # result.weights       = reader.read_array_from_file("weights")

    # Working with Pauls files (Feb 20
    # result.areas         = reader.read_array_from_file("area")
    # result.region_labels = reader.read_array_from_file("centres", dtype=numpy.str, use_cols=(0,))
    # result.centres       = reader.read_array_from_file("centres", use_cols=(1, 2, 3))
    # result.cortical      = reader.read_array_from_file("cortical", dtype=numpy.bool)
    # result.hemispheres   = reader.read_array_from_file("hemisphere", dtype=numpy.bool)
    # result.orientations  = reader.read_array_from_file("orientation")
    result.tract_lengths = reader.read_array_from_file("tract_lengths")
    result.weights       = reader.read_array_from_file("weights")

    return result