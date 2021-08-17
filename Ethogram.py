# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:36:10 2021

@author: Jackie
"""
import numpy as np 
import pandas as pd 
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from vame.util.auxiliary import read_config



def ethogram_writer(config_file, n_cluster = [30], cluster_method = 'kmeans'):
    cfg = read_config(config_file)
    
    for cluster in n_cluster:
        print("Ethogram is now created for cluster size %d " %cluster)
        

        for file in cfg['video_sets']:
            #string of path and .npy
            file_name = str(cluster) + '_km_label_' + file + '.npy'
            path_to_file = cfg['project_path']+'results/'+file+'/'+'VAME'+'/'+cluster_method+'-'+str(cluster)
            print("working on file: ", file_name)
            print("in the path: ", path_to_file+ "/"+ file_name)
            
            
            # load the vector 
            vector_time_lable = np.load(path_to_file + "/"+ file_name)
            df_vector_time_lable = pd. DataFrame(vector_time_lable)
            df_orig = df_vector_time_lable.copy()


            #build matrix from it
            motif_num = cluster #change to general
            for col in range(0,motif_num):
                df_vector_time_lable["%d"%(col)] = df_orig[df_orig[0] == col]
  

            #use heatmap as template for the ethogram
            fig, ax = plt.subplots(figsize=(20, 9))
            sb.heatmap(df_vector_time_lable.drop(columns= 0).transpose(), vmin=0, vmax=(motif_num-1), cmap = 'jet')
            plt.title("Ethogram_%s" %file, fontsize = 20)
            plt.xlabel('Frame#', fontsize = 15) 
            plt.ylabel('Montif', fontsize = 15) 
            #plt.show()
            plt.savefig(path_to_file+ '/' +'Ethogram_%s.png' %file)



config_file = "I:/VAME_projects/19_4_plan10-Apr19-2021/config.yaml"
n_cluster = [15, 20, 30]
ethogram_writer(config_file, n_cluster, cluster_method = 'kmeans')    













