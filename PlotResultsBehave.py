import os.path
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import cv2
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as sch
import glob


# the markov chain is p(row) = 1
def Hierarchical_clusterring(project_path, cluster_method = 'kmeans', motifs_k = 20):
    paths_transition_metrices = project_path+'/results/*/*'+'/%s-%d' %(cluster_method,motifs_k) 
    paths_transition_metrices = paths_transition_metrices+'/behavior_quantification/transition_matrix.npy'
    paths_transition_metrices = glob.glob(paths_transition_metrices)
    
    i = 0
    all_transition_matrices = np.zeros((motifs_k,motifs_k,len(paths_transition_metrices)))
    for transition_matrix in paths_transition_metrices:
        all_transition_matrices[:,:,i] = np.load(transition_matrix)
        i= i+1
        
    
    avrg_transition_matrices = (np.sum(all_transition_matrices, axis = 2))/len(paths_transition_metrices)
    ##linkage = sch.linkage(avrg_transition_matrices, method='ward')
    ##dendrogram = sch.dendrogram(linkage, labels=30) #lables are motifs..
    return avrg_transition_matrices
    



def saveVideoWithLabelsMotif(avrg_transition_matrices):
    # Python program to write
    # text on video

    cap = cv2.VideoCapture(r'C:\Users\Jackie.MEDICINE\Desktop\VAME-master\new_vi\AllTogether\EPC_M26_2017-09-24_050.avi')
    out = cv2.VideoWriter(r'C:\Users\Jackie.MEDICINE\Desktop\VAME-master\Projects\TEST_allData_timeWindow10-Nov16-2020\EPC_M26_2017-09-24_050_test2.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30.06, (800,400))

    transition_matrix = np.load(
        r'C:\Users\Jackie.MEDICINE\Desktop\VAME-master\Projects\TEST_allData_timeWindow10-Nov16-2020\results\EPC_M26_2017-09-24_050\VAME\kmeans-20\behavior_quantification\transition_matrix.npy')

    motifs = np.load(
        r'C:\Users\Jackie.MEDICINE\Desktop\VAME-master\Projects\TEST_allData_timeWindow10-Nov16-2020\results\EPC_M26_2017-09-24_050\VAME\kmeans-20\20_km_label_EPC_M26_2017-09-24_050.npy')

    labelList = range(20)

    ##dendrogram = sch.dendrogram(sch.linkage(avrg_transition_matrices, method='ward'), labels=labelList)
    #dendrogram = sch.dendrogram(transition_matrix)
    ##model = AgglomerativeClustering(n_clusters=10, affinity='euclidean', linkage='ward')
    ##model.fit(avrg_transition_matrices)
    ##labels = model.labels_

    time_window = 10

    counter = 0
    while (True):
        # Capture frames in the video
        ret, frame = cap.read()

        if not ret:
            break

        # describe the type of font
        # to be used.
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Use putText() method for
        # inserting text on video
        if (counter < time_window / 2) or counter > (len(motifs) - 1):
            frameOutput = cv2.putText(frame,
                        'NONE',
                        (50, 50),
                        font, 1,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)
        else:
            textLabel = 'motifs : %d, Label: %d' % (motifs[counter -  int(time_window/2)], labels[motifs[counter - int(time_window/2)]])
            frameOutput = cv2.putText(frame,
                        textLabel,
                        (50, 50),
                        font, 1,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)
        # Display the resulting frame
        #cv2.imshow('video', frame)

        out.write(frameOutput)

        counter += 1

    # release the cap object
    cap.release()

    out.release()

    # close all windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    project_path= "F:/Vame_projects/21_1_success_allvis_deafualtParams-Jan21-2021"
    avrg = Hierarchical_clusterring(project_path, cluster_method = 'kmeans', motifs_k = 20)   
    #saveVideoWithLabelsMotif(avrg)
