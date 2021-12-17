#!/usr/bin/env python
# coding: utf-8

# # 1. Morphing Setup for $W^{\pm}(\ell^{\pm}\nu_{\ell})H(b\bar{b})$

# Here we set up the morphing basis for $W^{\pm}(\ell^{\pm}\nu_{\ell})H(b\bar{b})$ with all the relevant operators both in the gauge boson couplings and the gauge-fermion couplings:
# 
# $C_{H\square}$, $C_{HD}$, $C_{HW}$, and $C^{(3)}_{Hq}$
# 
# We omit the operator $C_{dH}$ which appears in the bottom-yukawa coupling, modifying the $H \to b\bar{b}$ decay, as it is poorly constrained by this process and well measured elsewhere.
# 
# As can be seen analytically, the operators $C_{HD}$ and $C_{H\square}$ only change $W^{\pm}H$ production by an overall rescaling of the couplings, and always enter in the combination 
# 
# $$C_{H\square} - \frac{1}{4} C_{HD}.$$
# 
# As an extra cross check of our procedure, we'll consider all four operators, then rotate the resulting $4 \times 4$ Fisher Information to explicitly remove the inherent flat direction, and do most of our analysis on the resulting $3 \times 3$ matrix.
# 
# This setup is used for both $W^+H$ and $W^-H$ production, though they must be generated and analyzed seprately (the same is true for the $W$ decays).

# ### Setup

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


# ## 1. Setup Morphing Basis

# Here we add the parameters to the morphing setup. Note that we rescale the $C_{HW}$ and $C_{Hq}^{(3)}$ coefficients, so that all the Fisher Information entries will be roughly the same size. This helps with numerical aspects later in the analysis.

# In[3]:


miner = MadMiner()

miner.add_parameter(
    lha_block='smeft',
    lha_id=4,
    parameter_name='cHbox',
    morphing_max_power=2,
    parameter_range=(-10.,10.)
)
miner.add_parameter(
    lha_block='smeft',
    lha_id=5,
    parameter_name='cHDD',
    morphing_max_power=2,
    parameter_range=(-10.,10.)
)
miner.add_parameter(
    lha_block='smeft',
    lha_id=7,
    parameter_name='cHW',
    morphing_max_power=2,
    param_card_transform='0.1*theta',
    parameter_range=(-10.,10.)
)
miner.add_parameter(
    lha_block='smeft',
    lha_id=25,
    parameter_name='cHq3',
    morphing_max_power=2,
    param_card_transform='0.01*theta',
    parameter_range=(-10.,10.)
)


# For now, we'll only add one benchmark manually at the SM, and let the morphing take care of the rest:

# In[4]:


miner.add_benchmark(
    {'cHbox':0., 'cHDD':0., 'cHW':0., 'cHq3':0.},
    'sm'
)


# Now we set the rest of the benchmarks automatically. To try and reduce any possibility of morphing error, we'll run a number of trials and tests to ensure a decent spread of the weights.

# In[5]:


miner.set_morphing(
    include_existing_benchmarks=True,
    max_overall_power=2,
    n_trials=1000,
    n_test_thetas=1000
)


# ## Setup Systematics

# Here we add scale and PDF systematics.
# 
# For scale uncertainties, we vary both $\mu_R$ and $\mu_F$ independently by a factor of $1/2$ and $2$.
# 
# For the PDF variations, we run over all the eigenvectors of the `PDF4LHC15_nlo_30` set.

# In[6]:


miner.set_systematics(
    scale_variation=(0.5,1,2),
    scales='independent',
    pdf_variation='90900'
)


# ### Save Setup
# 
# And finally, save the setup to a `.h5` file. Since the basis is well optimized, we should just use the same setup for all our later $WH$ runs.

# In[7]:


miner.save('data/wh_smeft_setup.h5')

