#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:26:39 2020

@author: zebarjn1, zhangj4, haakanaJ2
"""
import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.io import read_raw_fif, read_raw_bti
from mne.preprocessing import ICA
#from mne.preprocessing import create_eog_epochs
#from mne.preprocessing import create_ecg_epochs
from mne.time_frequency import tfr_morlet

# read, plot and filter raw data
input_path = '/u/63/zebarjn1/unix/Documents/python_scripts/summer2020_poject/summer_data/subjects/para47-meg/'
output_path = '/u/63/zebarjn1/unix/Documents/python_scripts/summer2020_poject/summer_data/subjects/para47-meg/'
subj = 'c,rfhp0.1Hz'
fname = input_path + subj
config_fname = input_path+'config'
head_shape_fname = input_path+'hs_file'

raw = read_raw_bti(fname,config_fname= config_fname , rename_channels=False, 
                   head_shape_fname=head_shape_fname, preload=True)
fig1 = raw.plot(n_channels = 10, title='raw Signal')
# trig =raw['TRIGGER']
# plt.figure()
# plt.plot(trig[1],trig[0].T) # plot trigger signal
sampling_freq = np.round(1/np.mean(np.diff(raw['TRIGGER'][1])),decimals=1)  #sampling frequency
bad_channel = ['A17']
picks = mne.pick_types(raw.info, meg=True, eeg=False, eog=False, stim=False, 
                        exclude=bad_channel)
reject=dict(mag=5e-12)
raw.filter(.3, 40, picks= picks, fir_design='firwin',n_jobs=2)
raw.crop(tmin=0,tmax=500.0) #pre 
#raw.crop(tmin=1600.0,tmax=2050.0) #post
 
#Event detection
event_id = {'false_p':200, 'true_p':202, 'false_c':204, 'true_c':206}
e1 = mne.find_events(raw, stim_channel='TRIGGER', min_duration = 0.005)
diff=np.concatenate(([0], np.diff(e1[:,2]))) 
e2 = e1[diff!=0,:]
e3 = e2[(e2[:,2]!=256) & (e2[:,2]!=278),:] 
e3[:,2] -= 256
mne.viz.plot_events(e3, show=False)
overlap_value = 0.5
stumuli_length_pre = [11, 14, 11, 12, 14, 15, 14, 8, 11, 11, 15, 12, 10, 11, 11, 11, 10, 15, 11, 15, 12, 8, 13, 13]  #pre
#stumuli_length_post = [13, 16, 13, 16, 10, 14, 14, 8, 16, 11, 16, 6, 13, 10, 12, 12, 15, 15, 13, 11, 13, 11, 12, 8] #post
events = []
for i in range(len(e3[:,2])):
    onset = e3[:,0][i]
    offset = int(stumuli_length_pre[i] * sampling_freq + onset)
    e_vector = np.array(list(np.arange(onset, offset, overlap_value*sampling_freq)))
    e_array = np.stack((e_vector.astype(int), 
                             np.repeat(e3[:,1][i], len(e_vector)), 
                             np.repeat(e3[:,2][i], len(e_vector))), axis=1)
    events.append(e_array)
events = np.vstack(events)
mne.viz.plot_events(events, show=False)

# #epochs creation
baseline = (0,0)
#baseline = (-0.5, -0.05)
epochs = mne.Epochs(raw, events, event_id = event_id, tmin = 0 ,
                    tmax = 1, picks=picks, reject=reject, preload=True, baseline =baseline) 
#epochs.save(output_path + subj + '-epo.fif', overwrite=True)

#create ICA object
ica = ICA(n_components=25, random_state=23, method='fastica')
ica.fit(raw, picks=picks, decim=3,reject=reject)
fig2 = ica.plot_components(title='ICA components')
ica.plot_sources(raw, title='ICA sources')
n_max_ecg, n_max_eog = 3, 2
title = 'Sources related to %s artifacts'

eog_inds = [0,1] 
ecg_inds = [2]
merged_inds = []
merged_inds.extend(ecg_inds)
merged_inds.extend(eog_inds)
ica.exclude = merged_inds
ica.apply(epochs)

# epochs.apply_baseline((-0.5, -0.05))    # baseline correction
epochs_false_p = epochs['false_p']
epochs_true_p = epochs['true_p']
epochs_false_c = epochs['false_c']
epochs_true_c = epochs['true_c']

#Time_Frequency Representation

freqs = np.arange(4, 40, 2) # freq 4-40Hz, steps of 2Hz
n_cycles = freqs / 2. 
vmin_TFR= -float('3.0e-24')  
vmax_TFR = float('3.0e-24')
mean_power_false_p = tfr_morlet(epochs_false_p, freqs=freqs, n_cycles=n_cycles,
                average=True, return_itc=False)
mean_power_true_p = tfr_morlet(epochs_true_p, freqs=freqs, n_cycles=n_cycles,
                average=True, return_itc=False)
mean_power_false_c = tfr_morlet(epochs_false_c, freqs=freqs, n_cycles=n_cycles,
                average=True, return_itc=False)
mean_power_true_c = tfr_morlet(epochs_true_c, freqs=freqs, n_cycles=n_cycles,
                average=True, return_itc=False)

#tfr_plots

mean_power_false_p.plot([0], baseline=baseline, mode='mean', vmin=vmin_TFR, vmax=vmax_TFR,
                  title='Mean power false p') 
mean_power_true_p.plot([0], baseline=baseline, mode='mean', vmin=vmin_TFR, vmax=vmax_TFR,
                  title='Mean power true p')
mean_power_false_c.plot([0], baseline=baseline, mode='mean', vmin=vmin_TFR, vmax=vmax_TFR,
                  title='Mean power false c') 
mean_power_true_c.plot([0], baseline=baseline, mode='mean', vmin=vmin_TFR, vmax=vmax_TFR,
                  title='Mean power true c')

# #Topoplot

# vmin= -float('5.0e-25')
# vmax = float('5.0e-25')
# tmin = 0.4
# tmax = 0.9
fmin = 8
fmax = 12

fig3, axis = plt.subplots(1, 2, figsize=(7, 4))
mne.viz.plot_tfr_topomap(mean_power_false_p, fmin=fmin, fmax=fmax, ch_type=None,
                         baseline=baseline, mode='mean', title='Alpha_false p', 
                         axes=axis[0], show=False)
mne.viz.plot_tfr_topomap(mean_power_true_p,  fmin=fmin, fmax=fmax, ch_type=None,
                         baseline=baseline, mode='mean', title='Alpha_true p',
                         axes=axis[1], show=False)

fig4, axis = plt.subplots(1, 2, figsize=(7, 4))
mne.viz.plot_tfr_topomap(mean_power_false_c, fmin=fmin, fmax=fmax, ch_type=None,
                         baseline=baseline, mode='mean', title='Alpha_false c',
                         axes=axis[0], show=False)
mne.viz.plot_tfr_topomap(mean_power_true_c, fmin=fmin, fmax=fmax, ch_type=None, 
                         baseline=baseline, mode='mean', title='Alpha_true c', 
                         axes=axis[1], show=False)
