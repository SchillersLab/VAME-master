# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:22:19 2020

@author: Jackie
"""
import os
import torch
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import torch.utils.data as Data

from vame.util.auxiliary import read_config
from vame.model.rnn_vae import RNN_VAE
from vame.model.dataloader import SEQUENCE_DATASET
    

def plot_reconstruction(filepath, test_loader, seq_len_half, model, model_name, 
                        FUTURE_DECODER, FUTURE_STEPS):
    x = test_loader.__iter__().next()
    x = x.permute(0,2,1)
    data = x[:,:seq_len_half,:].type('torch.FloatTensor').cuda()
    data_fut = x[:,seq_len_half:seq_len_half+FUTURE_STEPS,:].type('torch.FloatTensor').cuda()
    if FUTURE_DECODER:
        x_tilde, future, latent, mu, logvar = model(data)
        
        fut_orig = data_fut.cpu()
        fut_orig = fut_orig.data.numpy()
        fut = future.cpu()
        fut = fut.detach().numpy()
    
    else:
        x_tilde, latent, mu, logvar = model(data)

    data_orig = data.cpu()
    data_orig = data_orig.data.numpy()
    data_tilde = x_tilde.cpu()
    data_tilde = data_tilde.detach().numpy()
    
    if FUTURE_DECODER:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Reconstruction and future prediction of input sequence')
        ax1.plot(data_orig[1,...], color='k', label='Sequence Data')
        ax1.plot(data_tilde[1,...], color='r', linestyle='dashed', label='Sequence Reconstruction') 
        ax2.plot(fut_orig[1,...], color='k')
        ax2.plot(fut[1,...], color='r', linestyle='dashed')
        fig.savefig(filepath+'evaluate/'+'Future_Reconstruction.png') 
    
    else:
        fig, ax1 = plt.subplots(1, 1)
        fig.suptitle('Reconstruction of input sequence')
        ax1.plot(data_orig[1,...], color='k', label='Sequence Data')
        ax1.plot(data_tilde[1,...], color='r', linestyle='dashed', label='Sequence Reconstruction') 

        fig.savefig(filepath+'evaluate/'+'Reconstruction_'+model_name+'.png')
    