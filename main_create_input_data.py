"""
main data loader generator

Use this script to process the EEG data of the N-back test or the Heath-The-Chair Game

Updated 2022/06/10

"""


import os
import sys
import time
import pandas as pd
import numpy as np

from sklearn import preprocessing
from sklearn import model_selection
from sklearn import metrics

from eeg_globals import *
from eeg_config import *
from eeg_functions import *


filename = dataset + '.parquet'
eeg_df = pd.read_parquet('./data/' +  filename)
print('processing ', filename)


print('Step 1. Get power spectral and contact quality channels, parquet loaded ', eeg_df.shape)
selected_cols = all_pow_nodes + user_metalabels # to filter just the selected columns


eeg_df = eeg_df[selected_cols]
eeg_df = eeg_df.dropna()  # Drop  NaN because PS samples are shorter than the in raw_data
eeg_df = eeg_df.reset_index(drop=True)  # reset index


print('Step 2. Split data into small windows and compute on them a quality index, parquet loaded ', eeg_df.shape)
eeg_df = cut_signal(eeg_df, dic_cut_opts) # replace by a new version of Aura


print('Step 3. Filtering data, parquet loaded ', eeg_df.shape)
filename_new = filename.split('.')[0] + '_power_filt_'

if dic_filt_opts['filtered']:
    iqrs = iqr_load_precomputed(dic_filt_opts)
    eeg_df = filter_signal(eeg_df, iqrs, dic_filt_opts)

    filename_new +=  dic_filt_opts['datafiltset']
    if dic_filt_opts['per_phases']:
            filename += '_per_phase'
    else:
        filename_new += '_phase_' + str(dic_filt_opts['setphase'])
    filename_new += '_IQR_' + dic_filt_opts['IQRtype']

    if dic_filt_opts['IQRtype'] == 'new':
        filename_new += '_' + dic_filt_opts['IQRTh']
else:
    filename_new += 'none'
    print('\tNo filtering dataset')

print('Step 4. Create input features, parquet loaded ', eeg_df.shape)

filename_new += '_window_' + str(dic_cut_opts['window']) + '_' + str(dic_cut_opts['overlap'])

data_x, data_y = input_features(eeg_df)
file_data_x = filename_new + '_data_x.npy'
file_data_y = filename_new + '_data_y.npy'

np.save(os.path.join('./input_features/', file_data_x), data_x)
np.save(os.path.join('./input_features/', file_data_y), data_y)
del data_x, data_y, eeg_df
print('file saved')
