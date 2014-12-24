# -*- coding: utf-8 -*-
#
#
#  TheVirtualBrain-Scientific Package. This package holds all simulators, and 
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2013, Baycrest Centre for Geriatric Care ("Baycrest")
#
# This program is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License version 2 as published by the Free
# Software Foundation. This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details. You should have received a copy of the GNU General 
# Public License along with this program; if not, you can download it here
# http://www.gnu.org/licenses/old-licenses/gpl-2.0
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#   The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

"""
Generate 16 seconds of 2048Hz data at the region level, stochastic integration.

``Run time``: approximately 4 minutes (workstation circa 2010)

``Memory requirement``: < 1GB
``Storage requirement``: ~ 19MB

.. moduleauthor:: Stuart A. Knock <stuart.knock@gmail.com>

"""

from tvb.simulator.lab import *
from tvb.basic.readers import ZipReader, try_get_absolute_path
from itertools import product
import numpy

# From connectivity.Connectivity - copied here and modified to match filesnames of Berlin connectivity .txts in connectivity.zip (ie orientation.txt rather than average_orientations.txt)
def from_file(source_file="nonexistent.zip", instance=None):

    if instance is None:
        result = connectivity.Connectivity()
    else:
        result = instance

    source_full_path = try_get_absolute_path("tvb_data.connectivity", source_file)

    reader = ZipReader(source_full_path)

    result.areas         = reader.read_array_from_file("area")
    result.region_labels = reader.read_array_from_file("centres", dtype=numpy.str, use_cols=(0,))
    result.centres       = reader.read_array_from_file("centres", use_cols=(1, 2, 3))
    result.cortical      = reader.read_array_from_file("cortical", dtype=numpy.bool)
    result.hemispheres   = reader.read_array_from_file("hemisphere", dtype=numpy.bool)
    result.orientations  = reader.read_array_from_file("orientation")
    result.tract_lengths = reader.read_array_from_file("tract")
    result.weights       = reader.read_array_from_file("weights")

    return result

##----------------------------------------------------------------------------##
##-                      Perform the simulation                              -##
##----------------------------------------------------------------------------##

LOG.info("Configuring...")

## DEFINE A RANGE OF PARAMETERS AND LOOP THROUGH EVERY COMBO. RUN THE SIMULATION EACH TIME.

K11 = numpy.r_[0:1:.5]
K12 = numpy.r_[0:2:1]
K21 = numpy.r_[0:2:1]

pp = product(K11,K12,K21)

a = 1

for (K11i, K12i, K21i) in product(K11,K12,K21):

    print "#################################################"
    print "Starting simulation with K11i=", K11i, " K12i=", K12i, " K21i=", K21i

    # oscillator = models.Generic2dOscillator(**pars) #change to SJ3D
    # oscillator = models.ReducedSetHindmarshRose(K11=0.1, K12=0.1,K21=0.1) # if running not inside loop
    oscillator = models.ReducedSetHindmarshRose(K11=K11i, K12=K12i, K21=K21i) # Stefanescu-Jirsa


    #white_matter = connectivity.Connectivity(load_default=True)
    # white_matter = connectivity.Connectivity.from_file(source_file="/Users/jzimmermann/Documents/PHD_Thesis/Connectivity_zips/AJ_20140516_1600_Connectivity.zip", instance=None) ## source_file should be absolute path to connectivity.zip. If not, itll take the whole tvb path
    white_matter = from_file(source_file="/Users/jzimmermann/Documents/PHD_Thesis/Connectivity_zips/AA_20120815_Connectivity.zip", instance=None) ## source_file should be absolute path to connectivity.zip. If not, itll take the whole tvb path

    # testing git only

    white_matter.speed = numpy.array([4.0])
    white_matter_coupling = coupling.Linear(a=0.033)

    #Initialise an Integrator
    hiss = noise.Additive(nsig=numpy.array([2 ** -10, ])) # if i try with default value of nsig (=1.0), it overflows (nsig is D)
    heunint = integrators.HeunStochastic(dt=0.06103515625, noise=hiss) #dt is integration step size

    #Initialise a Monitor with period in physical time
    # what_to_watch = monitors.TemporalAverage(period=0.48828125)     # 2048Hz => period=1000.0/2048.0
    # what_to_watch = monitors.Bold(period=500)  # The default BOLD hrf kernal is voltera kernal.
    what_to_watch = monitors.Bold(period=500, hrf_kernel=equations.Gamma()) # Set hemodynamic response function (hrf) to gamma kernal rather than the voltera kernal

    #Initialise a Simulator -- Model, Connectivity, Integrator, and Monitors.
    sim = simulator.Simulator(model=oscillator, connectivity=white_matter,
                              coupling=white_matter_coupling,
                              integrator=heunint, monitors=what_to_watch)

    sim.configure()

    #Perform the simulation
    bold_data = []
    bold_time = []
    LOG.info("Starting simulation...")
    for bold in sim(simulation_length=1500):
        if bold is not None:
            bold_time.append(bold[0][0])    # TODO:The first [0] is a hack for single monitor
            bold_data.append(bold[0][1])    # TODO:The first [0] is a hack for single monitor

    LOG.info("Finished simulation.")


    ##----------------------------------------------------------------------------##
    ##-                     Save the data to a file                              -##
    ##----------------------------------------------------------------------------##

    #Make the list a numpy.array.
    LOG.info("Converting result to array...")
    TBOLD = numpy.array(bold_data)

    #Save it
    # FILE_NAME = "demo_data_region_16s_2048Hz.npy"
    FILE_NAME = "jo-demo-sj3d-bold.npy"
    LOG.info("Saving array to %s..." % FILE_NAME)
    numpy.save(FILE_NAME, TBOLD)

    # LOG.info("Done simulating K11i=", K11i, " K12i=", K12i, " ")

###EoF###
