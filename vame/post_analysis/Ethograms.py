# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 13:44:58 2021

@author: Jackie
"""
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import os
from sklearn.cluster import KMeans
import seaborn as sb
import matplotlib.pyplot as plt




# main def
def ethograms(config):
    dict_load = load_data_toTestAndTrain(config)
    df_labels_kmeans = PCA_Kmeans(config, dict_load, components = 0.95)
    
    
    return dict_load, df_labels_kmeans

# load data of train and of test 
def load_data_toTestAndTrain(config):
    path = config.split(sep = 'config.yaml')[0] + '\\data\\train'
    train, test = np.transpose(np.load(path+ '\\train_seq.npy')), np.transpose(np.load(path+ '\\test_seq.npy'))
    print('len of train_seq = %s\nlen of test_seq = %s' %(train.shape[0], test.shape[0]))
    train, test = pd.DataFrame(train), pd.DataFrame(test)
    
    # all data together with index naming
    header_train, header_test = np.load(path+ '\\train_files.npy'),np.load(path+ '\\test_files.npy') 
    all_header = np.concatenate([header_train, header_test])
    len_vid = (len(train) + len(test))/len(all_header)
    all_header_per_frame = all_header.repeat(len_vid)
    all_data = pd.concat([train, test])
    all_data.index = all_header_per_frame
    
    dict_load = {'train': train, 'test': test, 'all_data': all_data, 'len_vid': len_vid, 'all_header': all_header}
    
    return dict_load
    
# PCA-> Kmeans analysis for comparison of the results 
def PCA_Kmeans(config, dict_load, components = 0.95, n_clusters = 15):
    
    test = dict_load['test']
    train = dict_load['train']
    all_data = dict_load['all_data']
    len_vid = dict_load['len_vid']
    all_header = dict_load['all_header']
    
    pca = PCA(components) 
    principalComponents_train, principalComponents_test = pca.fit_transform(train), pca.transform(test) # projection
    principalComponents_all_data = pca.transform(all_data)
    print('The number of component was reduced to: %s'%principalComponents_train.shape[1])
    print('Explained varience by comp for training: %s' %(pca.explained_variance_ratio_))
    print('The total explained varience for trainig = %s' %sum(pca.explained_variance_ratio_))
    
    kmeans = KMeans(n_clusters=n_clusters) # creat instans, we have 6 clusters labled, therefor this is constant
    kmeans.fit(principalComponents_all_data)
    lables_kmeans = kmeans.predict(principalComponents_all_data) # array of 1Xtotal_frames
    df_labels_kmeans = pd.DataFrame(lables_kmeans, index = all_data.index)
    return pd.DataFrame(np.reshape(df_labels_kmeans.values, (-1, int(len_vid))), index =all_header)



def get_lable_list(dict_load, cluster = [15]):
    config = dict_load['config']
    label_array = np.array([])
    files = os.listdir(config + '\\results')
    for file in files:     
        temp_array = np.load(config +'\\results\\' +file+ '\\VAME\\kmeans-%s\\%s_km_label_%s.npy' %(cluster,cluster,file))
        temp = np.array([file, temp_array])
        label_array = np.append(label_array, temp, axis = 0)
        
    label_array = np.reshape(label_array, (len(files),2))      
    return label_array    


# ethogram across

# ethogram per each dir
config = "F:/Vame_projects/2_3_success_allAMIR_deafualtParams-Mar2-2021/config.yaml"
dict_load, df_labels_kmeans = ethograms(config)
