#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 13:52:04 2020
@author: luxemk
"""

import numpy as np
import pandas as pd
import glob

def runnerAllCSV():
    folderCSVPAth = glob.glob(r"\\192.114.20.177\f\videos\Final_data_set\*.csv")
    projectVEMAPath = r"I:\VAME_projects\19_4_plan10-Apr19-2021\data"
   

    selectCamera = 'L'
    i =1 

    for file in (folderCSVPAth):

        experimant_name = (file.split('\\'))[-1]
        print(experimant_name)
        experimant_name = str.replace(experimant_name, '.csv', '')
        print(experimant_name)
         
        outputPath = '%s/%s/%s-PE-seq.npy' % (projectVEMAPath, experimant_name, experimant_name)
        outputPath = outputPath.replace("\\","/")
        csv_to_numpy(file, outputPath, selectCamera, minmax_bool = 1, cut_frames = 1, interpolate = 0)
        print(str(i))
                
        ##### FOR ALL FRAMES BACK FOR SEGMENTATION ######
        outputPath_2 = '%s/%s/%s-ALL_FRAMES-seq.npy' % (projectVEMAPath, experimant_name, experimant_name)
        outputPath_2 = outputPath_2.replace("\\","/")
        csv_to_numpy(file, outputPath_2, selectCamera, minmax_bool = 1, cut_frames = 0, interpolate = 1)
        i = i +1



def csv_to_numpy(fileName, outputPath, selectCamera, minmax_bool = [0], cut_frames = [0], interpolate = [0]):
    """
    This is a demo function to show how a conversion from the resulting pose-estimation.csv file
    to a numpy array can be implemented.
    Note that this code is only useful for data which is a priori egocentric, i.e. head-fixed
    or otherwise restrained animals.
    """

    # Read in your .csv file, skip the first two rows and create a numpy array
    data = pd.read_csv(fileName)
    matching = [s for s in range(len(data.values[0])) if ('R' in data.values[0][s])] # or 'L' in data.values[0][s]

    #matching.remove(1)
    #matching.remove(2)
    #matching.remove(3)
    #matching.remove(4)
    #matching.remove(5)
    #matching.remove(6)
    #matching.remove(7)
    #matching.remove(8)
    #matching.remove(9)

    data_mat = data.values[2:len(data), matching]
    data_mat = data_mat.astype(np.float)

    # get the number of bodyparts, their x,y-position and the confidence from DeepLabCut
    bodyparts = int(np.size(data_mat[0, :]) / 3)
    positions = []
    confidence = []
    idx = 0
    for i in range(bodyparts):
        positions.append(data_mat[:, idx:idx + 2])
        confidence.append(data_mat[:, idx + 2])
        idx += 3

    body_position = np.concatenate(positions, axis=1)
    con_arr = np.array(confidence)

    # find low confidence and set them to NaN (vame.create_trainset(config) will interpolate these NaNs)
    # we will a
    body_position_nan = []
    idx = -1
    for i in range(bodyparts * 2):
        if i % 2 == 0:
            idx += 1
        seq = body_position[:, i]
        seq[con_arr[idx, :] < .8] = np.NaN
        body_position_nan.append(seq)

    final_positions = np.array(body_position_nan)
    
    ##CANGE TO RELEVENT FRAMES FOR LEARNING####
    if cut_frames:
        final_positions = final_positions[:, 600:1800]
        
    if interpolate:
        
        seq_inter = np.zeros((final_positions.shape[0],final_positions.shape[1]))
        for s in range(final_positions.shape[0]):
            seq_temp = final_positions[s,:]
            seq_pd = pd.Series(seq_temp)
            if np.isnan(seq_pd[0]):
                seq_pd[0] = next(x for x in seq_pd if not np.isnan(x))
            seq_pd_inter = seq_pd.interpolate(method="linear", order=None) # we can change it to 'time' or other tech, ducumanted at pd series interpolate
            seq_inter[s,:] = seq_pd_inter
        final_positions =   seq_inter
    
    # min_max transform for 0-1 range
    minmax_tranform_positions = min_max(final_positions)
    #minmax_tranform_positions = min_max_quantile(final_positions)
    
    # save the final_positions array with np.save()
    if (minmax_bool):
        np.save(outputPath, minmax_tranform_positions)
    else:
        np.save(outputPath, final_positions)
        

    
def min_max(final_positions):
    
    devider = np.nanmax(final_positions, axis = 1) - np.nanmin(final_positions, axis = 1)
    uper = (final_positions.T - np.nanmin(final_positions, axis = 1))
    minmax_tranform_positions = uper/devider
    minmax_tranform_positions = minmax_tranform_positions.T
    
    return minmax_tranform_positions
                               
def min_max_quantile(final_positions):
    
    devider = np.nanquantile(final_positions, q = 0.98, axis = 1) - np.nanquantile(final_positions, q= 0.02, axis = 1)
    uper = (final_positions.T - np.nanquantile(final_positions, q= 0.02, axis = 1))
    minmax_tranform_positions = uper/devider
    minmax_tranform_positions = minmax_tranform_positions.T
    
    return minmax_tranform_positions

    

if __name__ == "__main__":
    runnerAllCSV()
