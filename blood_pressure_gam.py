# OFFICIAL BP GAM #

import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pygam import LinearGAM
from statistics import mean
import matplotlib.pyplot as plt
import statistics

def calculate_percentage_less_than(arr, value):
    count = 0
    total = len(arr)
    for element in arr:
        if element < value:
            count += 1
    percentage = (count / total) * 100
    return percentage

def calculate_absolute_error(array1, array2):
    # Check if the arrays have the same shape
    if array1.shape != array2.shape:
        raise ValueError("Arrays must have the same shape.")

    # Compute the absolute difference between corresponding elements
    absolute_diff = np.abs(array1 - array2)

    # Calculate absolute error for each column
    absolute_error_column1 = absolute_diff[:, 0]
    absolute_error_column2 = absolute_diff[:, 1]

    return absolute_error_column1, absolute_error_column2

if __name__ == "__main__":
   
    data = pd.read_csv('./blood_pressure_mean_std.csv')
    predictors = ['mean_std', 'ms_mean']
    outcome = ['SBP', 'DBP']
    
    X = data[predictors].values
    y_D_BP = data['DBP'].values
    y_S_BP = data['SBP'].values
    
    n_features = len(predictors)
    
    abs_dbp = []
    abs_sbp = []
    mae_dbp_5 = []
    mae_sbp_5 = []
    mae_dbp_10 = []
    mae_sbp_10 = []
    mae_dbp_15 = []
    mae_sbp_15 = []
  
    lams = np.random.rand(100, n_features)
    lams = lams * n_features - 3
    lams = np.exp(lams)
    
    gam_D_BP = LinearGAM(n_splines=7).gridsearch(X, y_D_BP, lam=lams, progress=False)
    gam_S_BP = LinearGAM(n_splines=7).gridsearch(X, y_S_BP, lam=lams, progress=False)
    
    y_hat_D_BP = gam_D_BP.predict(X)
    y_hat_S_BP = gam_S_BP.predict(X)
    
    abs_dbp.append(np.abs(y_hat_D_BP - y_D_BP))
    abs_sbp.append(np.abs(y_hat_S_BP - y_S_BP))
    
    mae_dbp_5.append(calculate_percentage_less_than(np.abs(y_hat_D_BP - y_D_BP), 5/norm_param))
    mae_sbp_5.append(calculate_percentage_less_than(np.abs(y_hat_S_BP - y_S_BP), 5/norm_param))
    
    mae_dbp_10.append(calculate_percentage_less_than(np.abs(y_hat_D_BP - y_D_BP), 10/norm_param))
    mae_sbp_10.append(calculate_percentage_less_than(np.abs(y_hat_S_BP - y_S_BP), 10/norm_param))
    
    mae_dbp_15.append(calculate_percentage_less_than(np.abs(y_hat_D_BP - y_D_BP), 15/norm_param))
    mae_sbp_15.append(calculate_percentage_less_than(np.abs(y_hat_S_BP - y_S_BP), 15/norm_param))

    print("BHS Protocol")
    print("SPB - Less than 5 mmHg: %.3f - Less than 10 mmHg: %.3f - Less than 15 mmHg: %.3f" %(mean(mae_sbp_5), mean(mae_sbp_10), mean(mae_sbp_15)))
    print("DPB - Less than 5 mmHg: %.3f - Less than 10 mmHg: %.3f - Less than 15 mmHg: %.3f" %(mean(mae_dbp_5), mean(mae_dbp_10), mean(mae_dbp_15)))
    print("AAMI Protocol")
    print("Mean Difference - SBP: ", np.mean(np.array(abs_sbp)))
    print("Mean Difference - DBP: ", np.mean(np.array(abs_dbp)))
    print("Standard Deviation - SBP: ", np.std(np.array(abs_sbp)))
    print("Standard Deviation - DBP: ", np.std(np.array(abs_dbp)))
    
    # PLOT
    
    #fig, ax = plt.subplots(figsize=(10, 8))
    
    #XX = gam_D_BP.generate_X_grid(term=0)
    #plt.plot(XX, gam_D_BP.predict(XX), 'r--')
    #plt.plot(XX, gam_D_BP.prediction_intervals(XX, width=.95), color='b', ls='--')
    #plt.scatter(X, y_D_BP, facecolor='gray', edgecolors='none')
    #plt.xlabel('ms', fontsize=14)
    #plt.ylabel('SBP(top) & DBP(bottom)', fontsize=14)
    #plt.title('Splines = {}'.format(i), fontsize=20)
    
    #XX = gam_S_BP.generate_X_grid(term=0)
    #plt.plot(XX, gam_S_BP.predict(XX), 'r--')
    #plt.plot(XX, gam_S_BP.prediction_intervals(XX, width=.95), color='b', ls='--')
    #plt.scatter(X, y_S_BP, facecolor='gray', edgecolors='none')
    #plt.xlabel('ms', fontsize=14)
    #plt.ylabel('SBP(top) & DBP(bottom)', fontsize=14)
    #plt.title('Splines = {}'.format(i), fontsize=20)
    
    #titles = data.columns[0:n_features]
    #plt.figure()
    #fig, axs = plt.subplots(1,n_features,figsize=(40, 8))
    #for i, ax in enumerate(axs):
    # 	XX = gam_D_BP.generate_X_grid(term=i)
    # 	ax.plot(XX[:, i], gam_D_BP.partial_dependence(term=i, X=XX))
    # 	ax.plot(XX[:, i], gam_D_BP.partial_dependence(term=i, X=XX,   width=.95)[1], c='b', ls='--')
    # 	if i == 0:
    # 		ax.set_ylim(-30,30)
    # 	ax.set_title(titles[i])
