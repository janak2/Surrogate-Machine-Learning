# -*- coding: utf-8 -*-
"""fit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IgoIaq-eOnlsU0fn_GtrMV5prkGvw9DB
"""

import sys
sys.path.append("/content/drive/MyDrive/Gdrive/startup/Novus Sentry/src")
from preprocess import preprocess

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

N = 5557
CURRENT_MULTIPLIER= 1000.0
I_load = 0.0123

def insert_I_neg(I_neg):
  def current_sigmoidal_1(t, A, B, C, D, I_sd):
    I_measured = I_neg*(1.0-D*np.exp(-1.0*C/t)) -2*(I_neg*(1.0-D))*(0.5-1.0/(1.0+(np.exp(t/A)**B))) + I_sd
    return I_measured
  return current_sigmoidal_1

def current_sigmoidal_2(t, A, B, C, D, I_neg, I_sd):
  I_measured = I_neg*(1.0-D*np.exp(-1.0*C/t)) -2*(I_neg*(1.0-D))*(0.5-1.0/(1.0+np.exp((t/A)**B))) - I_sd
  return I_measured

def current_sigmoidal_3(t, A, B, C, D, I_neg, I_sd):
  I_measured = (I_neg-I_sd)*(1.0-D*np.exp(-1.0*C/t)) -2*((I_neg+I_sd)*(1.0-D))*(0.5-1.0/(1.0+np.exp((t/A)**B))) - I_sd
  return I_measured

def fit(input, output):
  print(input)
  input.iloc[:,1] = input.iloc[:,1] - I_load
  N = (input.iloc[:,1]).abs().argsort()[:1].item()
  #N = 6000
  print(N)
  i_measured = input.iloc[:N,1]*CURRENT_MULTIPLIER
  
  t = input.iloc[:N,0] - input.iloc[0,0]
  t.iloc[0] = 0.001 
  print(t)
  t_all = input.iloc[:,0] - input.iloc[0,0] 
  # t = input.iloc[:N,0]
  # t_all = input.iloc[:,0]

  # I_neg = i_measured[:5].mean()
  I_neg = i_measured.min()
  
  #f = insert_I_neg(I_neg)
  f= current_sigmoidal_3
  parameters, covariance = curve_fit(f,t, i_measured, 
                                     p0=[91.0, 0.6, 1, 0.9, I_neg, -0.0001*CURRENT_MULTIPLIER], 
                                     bounds=([0,0,0,0,-np.inf,-1.0*CURRENT_MULTIPLIER],[np.inf,1.0,np.inf,1.0,0,0]),
                                     max_nfev=50000, verbose=2)

  plt.scatter(t, i_measured,color='b',s=1)
  plt.plot(t, f(t,*parameters), color='r')
  plt.show()

  plt.scatter(t_all, (input.iloc[:,1])*CURRENT_MULTIPLIER,color='b',s=1)
  plt.plot(t_all, f(t_all,*parameters), color='r')
  plt.show()
  return parameters, covariance

if __name__=="__main__":
  input, output = preprocess("Data_v1")
  p, c = fit(input[0], output[0])
  print(*p, (output[0]-I_load)*CURRENT_MULTIPLIER)

