#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 09:15:28 2017

@author: nico
"""

import numpy as np

import ot,time


def wgw(G, C1, C2, p, q, loss_fun, epsilon,alpha,
                       max_iter=1000, tol=1e-9, verbose=False, log=False):

    allstar=time.time()
    C1 = np.asarray(C1, dtype=np.float64)
    C2 = np.asarray(C2, dtype=np.float64)

    #T = np.outer(p, q)  # Initialization
    T = np.eye(len(p), len(q))

    cpt = 0
    err = 1

    if loss_fun == 'square_loss':
        def f1(a):
            return (a**2) 
        def f2(b):
            return (b**2)    
        def h1(a):
            return a    
        def h2(b):
            return 2*b
    elif loss_fun == 'kl_loss':
        def f1(a):
            return a * np.log(a + 1e-15) - a    
        def f2(b):
            return b    
        def h1(a):
            return a    
        def h2(b):
            return np.log(b + 1e-15)

    start=time.time()      
    constC1=np.dot(np.dot(f1(C1),p.reshape(-1,1)),np.ones(len(q)).reshape(1,-1))
    constC2=np.dot(np.ones(len(p)).reshape(-1,1),np.dot(q.reshape(1,-1),f2(C2).T))
    constC=constC1+constC2
    hC1 = h1(C1)
    hC2 = h2(C2)
    end=time.time()
        
    log_struct={}
    log_struct['err']=[]
    log_struct['GW_dist']=[]
    log_struct['tens']=[]
    log_struct['sinkhorn']=[]
    log_struct['cpt']=0
    log_struct['const']=end-start

    while (err > tol and cpt < max_iter):
        A=-np.dot(hC1, T).dot(hC2.T)
        tens = constC+A
        log_struct['tens'].append(tens)
        B=alpha*tens
        if alpha==0:
            Cost = G
        elif alpha==1:
            Cost=tens
        else:
            Cost=G+B
        start=time.time()        
        T = ot.sinkhorn(p, q, Cost, epsilon,numItermax=500)
        end=time.time()
        log_struct['sinkhorn'].append(end-start)

        log_struct['GW_dist'].append(np.sum(T*Cost))
        if cpt>1:
            err = (log_struct['GW_dist'][-1]-log_struct['GW_dist'][-2])**2
        
            if log:
                log_struct['err'].append(err)
                log_struct['cpt']=cpt

            if verbose:
                print('{:5d}|{:8e}|'.format(cpt, err))

        cpt += 1

    endall=time.time()
    log_struct['all']=endall-allstar
    if log:
        return T, log_struct
    else:
        return T