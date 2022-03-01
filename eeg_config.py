# What is the prefix of the dataset  to be processed?

# dataset   = 'selected'
# dataset   = 'seriousgame'
# dataset   = 'sabadell'
dataset = 'fram260721'

dic_filt_opts = {
    'filtered'  : True, # Will dataset be filtererd?

    'per_phases': False, # can be True and filter each phase by the corresponding phase or False and compute all the signals by a simple IQR computed on a phase
    'datafiltset':'aslogic', # dataset on which IQR is computed. If there is no filtering, change by 'none'
    'setphase'  : 2, # phase on which IQR is computed
    'q'         : 0.01, # percentile used to compute IQR
    'IQRtype'   : 'new', #'new','old'
    'IQRTh'     : 'iqr', # qup o iqr
    }

dic_cut_opts = {'window'    : 10, # window size in seconds
                'overlap'   : 0, # overlapping in seconds
                }
