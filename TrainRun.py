import vame
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as sch
import numpy

if __name__ == "__main__":
    config = "F:/AMIR_VAME_projects/AMIR_plan2_OneHand_nonNormalized-Aug28-2021/config.yaml"
    #vame.create_trainset(config, cut_frames = True)
    #vame.rnn_model(config, model_name='VAME', pretrained_weights=False, pretrained_model=None)
    #vame.evaluate_model(config, model_name='VAME')
    #vame.behavior_segmentation(config, model_name='VAME', cluster_method='kmeans', n_cluster=[10,15,20,30])
    n_cluster= [30]
    #for k in n_cluster:
     #vame.behavior_quantification(config, model_name='VAME', cluster_method='kmeans', n_cluster=k)
    vame.motif_videos(config, model_name='VAME', cluster_method="kmeans", n_cluster=n_cluster)
    

    