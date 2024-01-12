# Infrared-BP

The dataset used for the "Non-Contact Blood Pressure Estimation using infrared motion magnified facial video" [publication](https://utopia.duth.gr/nmitiano/pdf/CNNA_2023_1.pdf). The code developed is to fit the data to the reference Blood Pressure values. The code used for Eulerian Video Magnification was available from [here](http://people.csail.mit.edu/mrub/evm/#code). The dataset can be viewed and downloaded through this [link](https://mega.nz/folder/KdhlnSjB#vX4uepisNf2s_P4sMHsqjA).

# Steps
- Collect your data: You'll need videos captured by an infrared camera. In these videos, the forehead and the upper palm need to be clearly visible. Also you'll need an RGB screenshot of each volunteer, before you start recording with the infrared camera.
- Feed this RGB screenshot to the face and hand detection program that will return the coordinates for the regions of interests (in MATLAB's format)
- Crop each ROI from the original videostream using MATLAB
- Apply Eulerian Video Magnification
- Run PTT estimation program to produce the "blood_pressure_mean_std.csv"
- Feed "blood_pressure_mean_std.csv" to "blood_pressure_gam.py" and "regressors_bp_2.py"
