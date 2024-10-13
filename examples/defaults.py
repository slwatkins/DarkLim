import numpy as np
from darklim import constants

class Defaults:
    
    def __init__(self):
        
        self.results_dir = './results/'
        self.max_cpus = 24

        self.nexp = 1000
        self.t_days = 1 / 3600 / 24.

        self.target = 'Si'
        self.volume_cm3 = 0.1

        self.n_sensors = 1
        self.coincidence = 1
        self.window_s = 1e-6
        self.nsigma = 5
        
        self.baseline_res_eV = 0.2
        
        self.masses_GeV = [3e-3, 2e1, 24]

        self.sigma0 = 1e-35

        self.elf_params_NR = {}
        self.elf_params_electron = {'mediator': 'massless', 'kcut': 0, 'method': 'grid', 'withscreening': True, 'suppress_darkelf_output': False}
        self.elf_params_phonon = {'mediator': 'massive', 'suppress_darkelf_output': False, 'dark_photon': False}
