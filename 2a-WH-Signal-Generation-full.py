#!/usr/bin/env python
# coding: utf-8

# # 2. Signal Generation

# Here we set up the signal generation processes for both $W^+H$ and $W^-H$ separately, so that they can later be analyzed.

# In[1]:


from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import os

import logging
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')

from madminer.core import MadMiner
from madminer.lhe import LHEReader
from madminer.sampling import SampleAugmenter, combine_and_shuffle
from madminer.plotting import plot_distributions

from scipy.optimize import curve_fit

import madminer.__version__
print( 'MadMiner version: {}'.format(madminer.__version__) )


# In[2]:


# MadMiner output
logging.basicConfig(
    format='%(asctime)-5.5s %(name)-20.20s %(levelname)-7.7s %(message)s',
    datefmt='%H:%M',
    level=logging.INFO
)

# Output of all other modules (e.g. matplotlib)
for key in logging.Logger.manager.loggerDict:
    if "madminer" not in key:
        logging.getLogger(key).setLevel(logging.WARNING)


# In[3]:


mg_dir = './MG5_aMC_v2_6_7'


# We load the MadMiner morphing setup created in the previous section, which includes morphing benchmarks to span the full parameter space of $(C_{H\square}, C_{HD}, C_{HW}, C_{Hq}^{(3)})$.

# In[4]:


miner = MadMiner()
miner.load('data/wh_smeft_setup.h5')


# We'll generate a number of samples simulataneously using MadMiner.run_multiple().
# 
# A quick summary of what's in the cards used for the generation:

# `cards/signal_processes/proc_card_wph_mu_smeftsim.dat`:
# 
#     import model SMEFTsim
#     generate p p > w+ h > mu+ vm b b~ QCD=0 QED=99 NP=1
# 
# 
# `cards/run_card_wh_parton.dat`:
# 
#     50000 = nevents
#     6500.0   = ebeam1
#     6500.0   = ebeam2`
#     35.0 = ptb
#     10.0 = ptl
#     25.0 = misset
#     30.0 = ptjmax
#     2.5 = etab
#     2.5 = etal
#     80.0 = mmbb
#     160.0 = mmbbmax
#     0.4 = drbb
#     0.4 = drbl
#     True = cut_decays

# We generate the events in a number of small batches, using the SM benchmark for sampling.

# In[5]:


nrun = 40


# ## 1. $W^+(\mu^+ \nu_{\mu})H(b\bar{b})$

# In[6]:


miner.run_multiple(
    mg_directory=mg_dir,
    log_directory='logs/wph_mu_smeftsim',
    mg_process_directory='./signal_samples/wph_mu_smeftsim',
    proc_card_file='./cards/signal_processes/proc_card_wph_mu_smeftsim.dat',
    param_card_template_file='./cards/param_card_template_smeftsim.dat',
    run_card_files=['./cards/run_card_wh_parton.dat' for i in range(nrun)],
    sample_benchmarks=['sm'],
    initial_command=None
)


# ## 2. $W^+(e^+\nu_{e})H(b\bar{b})$

# In[7]:


miner.run_multiple(
    mg_directory=mg_dir,
    log_directory='logs/wph_e_smeftsim',
    mg_process_directory='./signal_samples/wph_e_smeftsim',
    proc_card_file='./cards/signal_processes/proc_card_wph_e_smeftsim.dat',
    param_card_template_file='./cards/param_card_template_smeftsim.dat',
    run_card_files=['./cards/run_card_wh_parton.dat' for i in range(nrun)],
    sample_benchmarks=['sm'],
    initial_command=None
)


# ## 3. $W^-(\mu^-\bar{\nu}_{\mu})H(b\bar{b})$

# In[8]:


miner.run_multiple(
    mg_directory=mg_dir,
    log_directory='logs/wmh_mu_smeftsim',
    mg_process_directory='./signal_samples/wmh_mu_smeftsim',
    proc_card_file='./cards/signal_processes/proc_card_wmh_mu_smeftsim.dat',
    param_card_template_file='./cards/param_card_template_smeftsim.dat',
    run_card_files=['./cards/run_card_wh_parton.dat' for i in range(nrun)],
    sample_benchmarks=['sm'],
    initial_command=None
)


# ## 4. $W^-(e^-\bar{\nu}_{e})H(b\bar{b})$

# In[9]:


miner.run_multiple(
    mg_directory=mg_dir,
    log_directory='logs/wmh_e_smeftsim',
    mg_process_directory='./signal_samples/wmh_e_smeftsim',
    proc_card_file='./cards/signal_processes/proc_card_wmh_e_smeftsim.dat',
    param_card_template_file='./cards/param_card_template_smeftsim.dat',
    run_card_files=['./cards/run_card_wh_parton.dat' for i in range(nrun)],
    sample_benchmarks=['sm'],
    initial_command=None
)

