PSF = 8 # power spectral frequency
RSF = 128 # raw data sampling frequency

user_metalabels = ['datetime', 'subject', 'test', 'phase'] # DataFrame columns that contains the labels of pre-processed data
flight_metalabels = ['datetime', 'subject', 'flight', 'flight_number', 'with_interruptions', 'event', 'phase']

pow_theta_nodes = ['POW.AF3.Theta',
 'POW.F7.Theta',
 'POW.F3.Theta',
 'POW.FC5.Theta',
 'POW.T7.Theta',
 'POW.P7.Theta',
 'POW.O1.Theta',
 'POW.O2.Theta',
 'POW.P8.Theta',
 'POW.T8.Theta',
 'POW.FC6.Theta',
 'POW.F4.Theta',
 'POW.F8.Theta',
 'POW.AF4.Theta']

pow_alpha_nodes = ['POW.AF3.Alpha',
 'POW.F7.Alpha',
 'POW.F3.Alpha',
 'POW.FC5.Alpha',
 'POW.T7.Alpha',
 'POW.P7.Alpha',
 'POW.O1.Alpha',
 'POW.O2.Alpha',
 'POW.P8.Alpha',
 'POW.T8.Alpha',
 'POW.FC6.Alpha',
 'POW.F4.Alpha',
 'POW.F8.Alpha',
 'POW.AF4.Alpha']

pow_betal_nodes = ['POW.AF3.BetaL',
 'POW.F7.BetaL',
 'POW.F3.BetaL',
 'POW.FC5.BetaL',
 'POW.T7.BetaL',
 'POW.P7.BetaL',
 'POW.O1.BetaL',
 'POW.O2.BetaL',
 'POW.P8.BetaL',
 'POW.T8.BetaL',
 'POW.FC6.BetaL',
 'POW.F4.BetaL',
 'POW.F8.BetaL',
 'POW.AF4.BetaL']

pow_betah_nodes = ['POW.AF3.BetaH',
 'POW.F7.BetaH',
 'POW.F3.BetaH',
 'POW.FC5.BetaH',
 'POW.T7.BetaH',
 'POW.P7.BetaH',
 'POW.O1.BetaH',
 'POW.O2.BetaH',
 'POW.P8.BetaH',
 'POW.T8.BetaH',
 'POW.FC6.BetaH',
 'POW.F4.BetaH',
 'POW.F8.BetaH',
 'POW.AF4.BetaH']

pow_gamma_nodes = ['POW.AF3.Gamma',
 'POW.F7.Gamma',
 'POW.F3.Gamma',
 'POW.FC5.Gamma',
 'POW.T7.Gamma',
 'POW.P7.Gamma',
 'POW.O1.Gamma',
 'POW.O2.Gamma',
 'POW.P8.Gamma',
 'POW.T8.Gamma',
 'POW.FC6.Gamma',
 'POW.F4.Gamma',
 'POW.F8.Gamma',
 'POW.AF4.Gamma']

all_pow_nodes = pow_theta_nodes + pow_alpha_nodes +  pow_betal_nodes + pow_betah_nodes + pow_gamma_nodes

dic_pow_waves = {'theta' : pow_theta_nodes,
                 'alpha' : pow_alpha_nodes,
                 'betal' : pow_betal_nodes,
                 'betah' : pow_betah_nodes,
                 'gamma' : pow_gamma_nodes,
             }

all_pow_waves = list(dic_pow_waves.keys())