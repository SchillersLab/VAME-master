# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 15:47:59 2021

@author: Jackie
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from vame.util.auxiliary import read_config
from pathlib import Path
import matplotlib as mpl

# load from yaml all the vids names and append to vec 
config = r'F:\AMIR_VAME_projects\NoseCentering_oneCam_plan10-Sep14-2021\config.yaml'
config_file = Path(config).resolve()
cfg = read_config(config_file)
files = []

if cfg['all_data'] == 'No':
    all_flag = input("Do you want to qunatify your entire dataset? \n"
                     "If you only want to use a specific dataset type filename: \n"
                     "yes/no/filename ")
else: 
    all_flag = 'yes'

if all_flag == 'yes' or all_flag == 'Yes':
    for file in cfg['video_sets']:
        files.append(file)  
elif all_flag == 'no' or all_flag == 'No':
    for file in cfg['video_sets']:
        use_file = input("Do you want to quantify " + file + "? yes/no: ")
        if use_file == 'yes':
            files.append(file)
        if use_file == 'no':
            continue
else:
    files.append(all_flag)

    
# load the seq-clean (smooth coor), latents and lables 
drop_coor = cfg['time_window']*0.5 # the segmantation is running unil this point
coor = []
latent = []
lables = []
n_clusters = [40]
for cluster in n_clusters: 
    for file in files:
        path_to_coor = cfg['project_path']+'data/'+file+'/'+file+'-PE-ALL-seq-clean.npy'
        path_to_label = cfg['project_path']+'results/'+file+'/VAME/'+ 'kmeans-%d'%(cluster) +'/'+'%d_km_label_%s.npy'%(cluster, file)
        path_to_latent = cfg['project_path']+'results/'+file+'/VAME/'+ 'kmeans-%d'%(cluster) +'/'+'latent_vector_%s.npy'%(file)
        
        coor_temp = np.load(path_to_coor)
        coor_temp = coor_temp.T
        # swich (0,0) down
        coor_temp[:,3] = 400 - coor_temp[:,3] # 400 or 1 
        
        labels_temp = np.load(path_to_label)
        latent_temp = np.load(path_to_latent)
        
        end_coor = int(len(coor_temp) - 2*drop_coor) 
        # end point for coor 
        
        coor.append(coor_temp[int(drop_coor):end_coor,:])# change here and check again about this really not clear thing 
        lables.append(labels_temp)
        latent.append(latent_temp)
        

                  
mat_coor = np.vstack(coor)
mat_labels = np.vstack(lables)
mat_latent = np.vstack(latent)      



# draw plot per trail
colors2 = [plt.cm.tab20(s) for s in range(0,20)]
colors1 = [plt.cm.tab20b(s) for s in range(2,20,2)]
#colors3 = [plt.cm.tab20c(s) for s in range(0,20,2)]
#colors =  colors1 + colors2 


colors = ['#696969', '#dcdcdc', "#228b22", "#7f0000", "#808000", "#483d8b",
          '#008b8b', '#cd853f', '#4682b4', '#9acd32', '#00008b', '#7f007f',
          '#8fbc8f', '#b03060', '#ff0000', '#ff8c00', '#ffff00', '#7fff00',
          '#00ff7f', '#dc143c', '#00ffff', '#0000ff', '#f08080', '#da70d6',
          '#ff00ff', '#1e90ff', "#10e68c", '#90ee90', '#ff1493', '#7b68ee',
          '#ff4081', '#cc2288', '#f0ffff', '#f8f8ff', '#72675c', '#29c876',
          '#fff68f', '#E6E6FA', '#E0FFFF', '#FFB6C1', '#FF8247', '#C6E2FF']


for cluster in n_clusters: # total number of clusters, if there are more than one group to check 
    for trail in range(len(coor)): 
        fig, ax = plt.subplots()
        plt.ylabel('y hand center coordinate')
        plt.xlabel('x hand center coordinate')
        plt.xlim([400,800]) # pay attention 400,800 and if normolized [0,1]
        plt.ylim([0,400]) # pay attention 0,400 and if normolized [0,1]
        plt.title("animal trail: %s" %(files[trail]), fontsize = 10)
        
        for lable in range(cluster):
            
            bool_lable = lables[trail] == lable
            
            
            ax.scatter(coor[trail][bool_lable,2], coor[trail][bool_lable,3], c = colors[lable], s = 8,
                       label='%d motif' % lable, edgecolors = 'k', linewidth = 0.2)
           
            ax.legend(markerscale=2, fontsize=5)
             
            # save in the folder 
        save_trail_path = cfg['project_path'] + 'results/'+ files[trail] +'/VAME/' +'kmeans-%d/'%(cluster)+'trajectory_lable.png'
        plt.savefig(save_trail_path, dpi=1400)
            
        fig.show()  
         
'''     
# draw plot per motif 




for cluster in n_clusters:
    for lable in range(cluster):
        fig, ax = plt.subplots()
        plt.ylabel('y hand center coordinate')
        plt.xlabel('x hand center coordinate')
        plt.xlim([0,1]) # pay attention 400,800
        plt.ylim([0,1]) # pay attention 0,400
        plt.title("motif number: %s" %(lable), fontsize = 10)   
        cm = plt.cm.get_cmap('Blues')
        
        for trail in range(len(coor)):
            
            bool_lable = lables[trail] == lable
            ax.scatter(coor[trail][bool_lable,0], coor[trail][bool_lable,1],
                    c= range(sum(bool_lable)),
                    #marker='.',
                    #markersize= 2,
                    #alpha = 0.5,
                    cmap = cm,
                    label='%d motif' % lable, 
                    linewidth = 1)
           

             
            # save in the folder 
        save_trail_path = cfg['project_path'] +'trajectory_lable_%d.png'%(lable)
        plt.savefig(save_trail_path, dpi=1400)            
     '''   