import pandas as pd
import numpy as np

from scipy import signal

from eeg_globals import *

def cut_signal(eeg_df, dic_cut_opts):
    """
    Cut signal into small windows with overlapping

    Return:
        A new dataframe
    """

    sample_win = int(PSF * dic_cut_opts['window'])
    sample_over = int(PSF * dic_cut_opts['overlap'])
    sample_stride = sample_win - sample_over

    # To data, add a column observation based on phase
    print('split data into observations')
    eeg_window = []
    for subject in eeg_df.subject.unique():
        print(subject)
        for test in eeg_df.test.unique():
            print('     ' + str(test))
            for phase in eeg_df.phase.unique():
                print('         ' + str(phase))

                df = eeg_df.loc[(eeg_df.subject==subject) &
                                (eeg_df.test==test) &
                                (eeg_df.phase==phase)].copy()
                df = df.reset_index(drop=True)
                n_intervals = int(np.floor(( df.shape[0] - sample_win ) / sample_stride) + 1)
                for k in range(n_intervals):
                    data = df.iloc[k * sample_stride : k * sample_stride + sample_win].copy()
                    data = data.reset_index(drop=True)
                    data['observation'] = k + 1
                    eeg_window.append(data)
                    del data
                del df

    eeg_window  = pd.concat(eeg_window, axis=0, ignore_index=True)
    print(eeg_window.shape)

    return eeg_window

def cut_signal_simulator(eeg_df, dic_cut):
    labels = list(eeg_df.columns)

    sample_win = int(PSF * dic_cut['window'])
    sample_over = int(PSF * dic_cut['overlap'])
    sample_stride = sample_win - sample_over

    # To data, add a column observation based on phase
    print('split data into observations')

    eeg_window = []
    for subject in eeg_df.subject.unique():
        print(subject)
        for flight_number in  eeg_df.flight_number.unique():
            print('     ' + str(flight_number))
            for phase in eeg_df.phase.unique():
                print('         ' + str(phase))

                df = eeg_df.loc[(eeg_df.subject==subject) &
                                (eeg_df.flight_number==flight_number) &
                                (eeg_df.phase==phase)].copy()
                df = df.reset_index(drop=True)

                n_intervals = int(np.floor(( df.shape[0] - sample_win ) / sample_stride) + 1)
                for k in range(n_intervals):
                    data = df.iloc[k * sample_stride : k * sample_stride + sample_win].copy()
                    data = data.reset_index(drop=True)
                    data['observation'] = k + 1
                    eeg_window.append(data)
                    del data
                del df

    eeg_window  = pd.concat(eeg_window, axis=0, ignore_index=True)
    return eeg_window



def filter_signal(eeg_df, iqrs, dic_filt_opts):
    """
    Filter signal

    """
    all_labels = list(eeg_df.columns)

    # check the order of labels
    label_grouped = False
    if all_labels[0].split('.')[-1] == all_labels[1].split('.')[-1]:
        label_grouped = True

    data_labels = all_pow_nodes
    meta_labels =  [lab for lab in all_labels if lab not in data_labels]

    eeg_pow_filt  = []
    for phase in eeg_df.phase.unique():
        print('\t',phase)

        sub = eeg_df.loc[ (eeg_df.phase == phase), :].copy()
        sub = sub.reset_index(drop=True)

        meta = sub[meta_labels].values # [N, ]
        data = sub[data_labels].values # always [N,70]

        if dic_filt_opts['per_phases']:
            th_up_all = iqrs[(dic_filt_opts['datafiltset'], phase)] # OLDER ORDER
        else:
            th_up_all = iqrs[(dic_filt_opts['datafiltset'], dic_filt_opts['setphase'])] # OLDER ORDER


        if label_grouped:
            th_up_all = iqr_by_group(th_up_all) # group iqrs
            print('\tFiltering --> nodes are grouped')

        m_thresh = np.repeat([np.array(th_up_all)], data.shape[0], axis=0)
        mask = data > m_thresh
        data[mask] = m_thresh[mask] / 2.

        # median filter applying
        for rr in range(data.shape[1]): # by colums (70 cols = 14 channesl * 5 waves)
            data[:, rr] = signal.medfilt(data[:, rr], kernel_size=3)

        df = pd.DataFrame(np.concatenate((data, meta), axis=1), columns=data_labels + meta_labels)
        eeg_pow_filt.append(df)
        del df

    eeg_pow_filt  = pd.concat(eeg_pow_filt, axis=0, ignore_index=True)

    return eeg_pow_filt

def input_features(eeg_df, start_col='subject'):
    """
    Organize the eeg_df dataframe into a numpy structure ready to feed to
    the model

    start_col : is the column where the metadata starts

    Returns
    -------
    data_x : numpy
        data of signals [n_samples, n_waves, n_nodes, timesteps]

    data_y : numpy
        metadata of signals [n_samples, subject...]

    """
    labels = list(eeg_df.columns)
    power_nodes = [i for i in labels if i.startswith('POW')]
    pos_subject = labels.index(start_col)

    if len(power_nodes) != 70: # 14 electrodes * 5 waves
        print('The number of nodes does not match the Emotiv 14 headset')
        return

    # data and labels are into separated files
    data_x = []
    data_y = []
    for subject in eeg_df.subject.unique():
            print(subject)
            for test in eeg_df.test.unique():
                print('     ' + str(test))
                for phase in eeg_df.phase.unique():
                    print('         ' + str(phase))

                    signal_arr = []
                    target_arr = ''
                    for idx, wave in enumerate(all_pow_waves):

                        data_labels = dic_pow_waves[wave]
                        meta_labels = labels[pos_subject : ]  # [70 : ]
                        labels_sel = data_labels + meta_labels

                        df = eeg_df.loc[(eeg_df.subject==subject) &
                                             (eeg_df.test==test) &
                                             (eeg_df.phase==phase), labels_sel].copy()
                        df = df.reset_index(drop=True)

                        signal = []
                        target = []
                        for obs in df.observation.unique():
                            x = df.loc[df.observation == obs].values[:, :len(labels_sel) - len(meta_labels)].T  # data
                            y = df.loc[df.observation == obs].values[0 , len(labels_sel) - len(meta_labels) : ] # metadata
                            signal.append(x)
                            target.append(y)
                            del x, y
                        del df

                        signal_arr.append(np.array(signal))
                        if idx == 0:
                            target_arr = np.array(target) # save labels from only the first passing
                        del signal, target

                    # stack signals [signals, wave, n_nodes, timesteps]
                    signal_arr = np.stack((signal_arr), axis=1)
                    if signal_arr.ndim == 4:
                        data_x.append(signal_arr)
                        data_y.append(target_arr)
                    del signal_arr, target_arr

    # concatenate along the rows axis
    data_x = np.concatenate(data_x, axis=0) # (n_samples, n_waves, n_nodes, time_step)
    data_x = data_x.astype(np.float32)
    data_y = np.concatenate(data_y, axis=0) # (n_samples, ...)
    return data_x, data_y


def input_features_simulator(eeg_df, start_col='subject'):
    """
    Organize the eeg_df dataframe into a numpy structure ready to feed to
    the model

    start_col : is the column where the metadata starts

    Returns
    -------
    data_x : numpy
        data of signals [n_samples, n_waves, n_nodes, timesteps]

    data_y : numpy
        metadata of signals [n_samples, subject...]

    """
    labels = list(eeg_df.columns)
    power_nodes = [i for i in labels if i.startswith('POW')]
    pos_subject = labels.index(start_col)

    if len(power_nodes) != 70: # 14 electrodes * 5 waves
        print('The number of nodes does not match the Emotiv 14 headset')
        return

    # data and labels are into separated files
    data_x = []
    data_y = []
    for subject in eeg_df.subject.unique():
        print(subject)
        for flight_number in  eeg_df.flight_number.unique():
            print('     ' + str(flight_number))
            for phase in eeg_df.phase.unique():
                print('         ' + str(phase))

                signal_arr = []
                target_arr = ''
                for idx, wave in enumerate(all_pow_waves):

                    data_labels = dic_pow_waves[wave]
                    meta_labels = labels[pos_subject : ]  # [70 : ]
                    labels_sel = data_labels + meta_labels


                    df = eeg_df.loc[(eeg_df.subject==subject) &
                            (eeg_df.flight_number==flight_number) &
                            (eeg_df.phase==phase), labels_sel].copy()
                    df = df.reset_index(drop=True)

                    signal = []
                    target = []
                    for obs in df.observation.unique():
                        x = df.loc[df.observation == obs].values[:, :len(labels_sel) - len(meta_labels)].T  # data
                        y = df.loc[df.observation == obs].values[0 , len(labels_sel) - len(meta_labels) : ] # metadata
                        signal.append(x)
                        target.append(y)
                        del x, y
                    del df

                    signal_arr.append(np.array(signal))
                    if idx == 0:
                        target_arr = np.array(target) # save labels from only the first passing
                    del signal, target

                # stack signals [signals, wave, n_nodes, timesteps]
                signal_arr = np.stack((signal_arr), axis=1)
                if signal_arr.ndim == 4:
                    data_x.append(signal_arr)
                    data_y.append(target_arr)
                del signal_arr, target_arr

    # concatenate along the rows axis
    data_x = np.concatenate(data_x, axis=0) # (n_samples, n_waves, n_nodes, time_step)
    data_x = data_x.astype(np.float32)
    data_y = np.concatenate(data_y, axis=0) # (n_samples, ...)
    return data_x, data_y


def iqr_load_precomputed(dic_filt_opts):
    """
    Load precomputed IQR dictonary

    NOTICES: IT follows the RAW NODE ORDER

    """

    if dic_filt_opts['IQRtype'] == 'old':
        print('IQR OLD')
        iqr_file = './IQR/'+ 'IQR'
        iqrs = pd.read_pickle(iqr_file)

    elif dic_filt_opts['IQRtype'] == 'new':
        print('IQR NEW')
        iqr_file = './IQR/'+ 'IQR_' + str(int(dic_filt_opts['q']*100))
        iqrs = pd.read_pickle(iqr_file)
        iqrs = iqrs[dic_filt_opts['IQRTh']]
    return iqrs


def iqr_by_group(th_up_all):
    """
    Since IQR was computed by node-wave, reorder by group of waves
    """
    iqr_new = []
    for i in range(5):
        iqr_new.extend(th_up_all[i * 0 : -1 : 5])
    return iqr_new