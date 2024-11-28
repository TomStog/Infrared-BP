# Linear Regression Algorithms
from sklearn.linear_model import LinearRegression

import pandas as pd
from pandas import read_csv
from sklearn.metrics import r2_score
import numpy as np
import time
import psutil

from sklearn.preprocessing import PolynomialFeatures

def calculate_percentage_less_than(arr, value):
    count = 0
    total = len(arr)
    for element in arr:
        if element < value:
            count += 1
    percentage = (count / total) * 100
    return percentage


if __name__ == "__main__":

    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"Memory used by the script: {memory_info.rss} bytes")

    start = time.time()

    """LOAD DATA"""

    data = pd.read_csv('./blood_pressure_mean_std.csv')
    #predictors = ['mean_std']
    predictors = ['mean_std', 'ms_mean']
    outcome = ['SBP', 'DBP']

    X = data[predictors].values
    y_D_BP = data['DBP'].values
    y_S_BP = data['SBP'].values

    norm_param = 1

    abs_dbp = []
    abs_sbp = []
    mae_dbp_5 = []
    mae_sbp_5 = []
    mae_dbp_10 = []
    mae_sbp_10 = []
    mae_dbp_15 = []
    mae_sbp_15 = []
    r2_dbp = []
    r2_sbp = []

    polynomial_features= PolynomialFeatures(degree=2)   # 1 = Linear Regression / 2 = Quadratic Regression / 3 = Cubic Regression #
    x_poly = polynomial_features.fit_transform(X)

    # Insert Regression Algorithm
    model_S_BP = LinearRegression()
    model_D_BP = LinearRegression()
    model_S_BP.fit(x_poly, y_S_BP)
    model_D_BP.fit(x_poly, y_D_BP)

    # Predict
    y_hat_D_BP = model_D_BP.predict(x_poly)
    y_hat_S_BP = model_S_BP.predict(x_poly)

    abs_dbp.append(np.abs(y_hat_D_BP - y_D_BP) * norm_param)
    abs_sbp.append(np.abs(y_hat_S_BP - y_S_BP) * norm_param)

    mae_dbp_5.append(calculate_percentage_less_than(np.abs(y_hat_D_BP - y_D_BP), 5/norm_param))
    mae_sbp_5.append(calculate_percentage_less_than(np.abs(y_hat_S_BP - y_S_BP), 5/norm_param))

    mae_dbp_10.append(calculate_percentage_less_than(np.abs(y_hat_D_BP - y_D_BP), 10/norm_param))
    mae_sbp_10.append(calculate_percentage_less_than(np.abs(y_hat_S_BP - y_S_BP), 10/norm_param))

    mae_dbp_15.append(calculate_percentage_less_than(np.abs(y_hat_D_BP - y_D_BP), 15/norm_param))
    mae_sbp_15.append(calculate_percentage_less_than(np.abs(y_hat_S_BP - y_S_BP), 15/norm_param))

    r2_dbp.append(r2_score(y_D_BP, y_hat_D_BP))
    r2_sbp.append(r2_score(y_S_BP, y_hat_S_BP))

    end = time.time()

    print("Time consumed in working: ",(end - start)*1000, "milliseconds.")
    
    print("*BHS Protocol*")
    print("SPB - Less than 5 mmHg: %.3f - Less than 10 mmHg: %.3f - Less than 15 mmHg: %.3f" %(np.mean(mae_sbp_5), np.mean(mae_sbp_10), np.mean(mae_sbp_15)))
    print("DPB - Less than 5 mmHg: %.3f - Less than 10 mmHg: %.3f - Less than 15 mmHg: %.3f" %(np.mean(mae_dbp_5), np.mean(mae_dbp_10), np.mean(mae_dbp_15)))
    print("*AAMI Protocol*")
    print("Mean Difference - SBP: ", np.mean(np.array(abs_sbp)))
    print("Mean Difference - DBP: ", np.mean(np.array(abs_dbp)))
    print("Standard Deviation - SBP: ", np.std(np.array(abs_sbp)))
    print("Standard Deviation - DBP: ", np.std(np.array(abs_dbp)))
    print("R2 Score - SBP: ", np.mean(np.array(r2_sbp)))
    print("R2 Score - DBP: ", np.mean(np.array(r2_dbp)))
