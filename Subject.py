__author__ = 'jzimmermann'

import scipy.io as scipy_io

class Subject(object):
    # Holder of subject's name, empirical FC and SC matrix, age, does everything for that subject, it calls all other classes

    def __init__(self, id, age, empsc, empfc, empsc_path, empfc_path):
        self.id = id
        self.age = age
        self.empsc = empsc
        self.empfc = empfc
        self.empsc_path = empsc_path
        self.empfc_path = empfc_path

        # Convert paths to FC and SC instances.
        # coneverting a mat file, with FC_cc a FC matrix, into ndarray
        self.empfc = scipy_io.loadmat(self.empfc_path)['ind_fc']
        print self.empfc





