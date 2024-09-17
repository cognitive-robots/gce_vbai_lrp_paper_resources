# Data

## Quantitative Experiments
Output data related to the quantitative experiments.

## Parameters

### SimCARSv2
* Action Diff. Threshold ($\lambda_{a}$): { $0.0$, $0.1$, $0.2$, $0.3$, $0.4$, $0.5$, $0.6$, $0.7$, $0.8$, $0.9$, $1.0$ }
* Action & Outcome Diff. Scale Factors:
    - Action Diff. Scale Factor ($\alpha_{a}$): 0.1
    - Lane Goal Value Diff. Scale Factor ($\alpha_{v_l}$): 10
    - Outcome Diff. Scale Factor ($\alpha_{o}$): 0.1
    - Lane Transition Diff. Scale Factor ($\alpha_{lt}$): 100
    - Final Speed Diff. Scale Factor ($\alpha_{fs}$): 1
    - Distance Headway Diff. Scale Factor ($\alpha_{dh}$): 0.1
    - Max. Env. Force Mag. Diff. Scale Factor ($\alpha_{ef}$): 0.01
    - Action Done Diff. Scale Factor ($\alpha_{ad}$): 100
* Action Extraction Parameters:
    - Time Interval: $0.5\ s$
    - Action Min. Duration: $2.5\ s$
    - Action Min. Longitudinal Linear Acceleration: $0.1\ m/s^2$
    - Action Min. Longitudinal Linear Velocity Diff.: $1.0\ m/s$
    - Lane Min. Duration: $0.5\ s$
* Vehicle / Controller Parameters:
    - Cars / Trucks / Other (Based off Toyota Ascent Sport (Hybrid), 1.8L datasheet)
        + Width (w): Determined from data
        + Length (l): Determined from data
        + Approx. Height (h): $0.806 w\ m$
        + Approx. Mass: $116 w l h\ kg$
        + Approx. Axel Dist.: $0.292 l\ m$
        + Approx. Wheel Radius: $0.19\ m$
    - Motorcycles / Bicycles (Based off Honda Super Cub C125 2022 datasheet)
        + Width (w): $0.72\ m$
        + Length (l): $1.915\ m$
        + Approx. Height (h): $1\ m$
        + Approx. Mass: $110\ kg$
        + Approx. Axel Dist.: $0.6225\ m$
        + Approx. Wheel Radius: $0.17\ m$
    - Approx. Drag Area: $0.616\ m^2$
    - Cornering Stiffness: $49675$
    - Max. Slip Angle Value: $0.5 \pi$
    - Max. Motor Torque: $3260\ Nm$
    - Min. Motor Torque: $-3260\ Nm$
* Planner Parameters:
    - Simulation Action Done Speed Threshold: $1\ m/s$
    - Speed Limit: $31.3\ m/s$
    - Distance Headway Braking Time: $2\ s$
    - Env. Force Mag. Limit: $1000\ N$
    - Min. Action Speed Goal Value: $0\ m/s$
    - Max. Action Speed Goal Value: $45\ m/s$
    - Action Speed Goal Value Interval: $2.5\ m/s$
    - Max. Action Goal Time Horizon: $5\ s$
    - Action Goal Time Interval: $2.5\ s$

### SimCARSv1
* Reward Diff. Threshold: { $0.1$, $0.2$, $0.3$, $0.4$, $0.5$, $0.6$, $0.7$, $0.8$, $0.9$, $1.0$ }
* Action Extraction Parameters:
    - Time Interval: $0.04\ s$
    - Action Min. Duration: $1.0\ s$
    - Action Min. Longitudinal Linear Acceleration: $0.2\ m/s^2$
    - Action Min. Longitudinal Linear Velocity Diff.: $1.0\ m/s$
    - Lane Min. Duration: $2.5\ s$
* Controller Parameters:
    - Steering Look-Ahead Steps: $10$
    - Max. Longitudinal Acceleration: $3.5\ m/s^2$
    - Min. Longitudinal Acceleration: $-6.56\ m/s^2$

### Multi-Variage Granger Causality
* Significance Alpha: { $0.001$, $0.01$, $0.05$, $0.1$, $0.2$, $0.3$, $0.4$, $0.5$, $0.6$, $0.7$, $0.8$, $0.9$, $1.0$ }
* Statistical Test: Chi-Squared
* Multiple Hypothesis Test Correction: Benjamini-Hochberg False Discovery Rate
* VAR Model Estimation Regression Mode: Ordinary Least Squares
* Information Criteria Regression Mode: Locally Weighted Regression
* Model Order: Akaike Information Criterion
* Maximum Time Lag: $25$ / $1.0\ s$
* Maximum Autocovariance Lags: $1000$
* Random Seed: Undefined

### TiMINo
* Significance Alpha: { $0.001$, $0.01$, $0.05$, $0.1$, $0.2$, $0.3$, $0.4$, $0.5$, $0.6$, $0.7$, $0.8$, $0.9$, $1.0$ }
* Maximum Time Lag: $25$ / $1.0\ s$
* Assumed Time Series Model: Linear
* Independence Test: Cross Covariance
* Include Instant Effects: False
* Check for Confounders: False

### DYNOTEARS
* Threshold for W: $0.01$
* Threshold for A: $0.01$
* Regularisation Constant for W: $0.05$
* Regularisation Constant for A: $0.05$
* Maximum Time Lag: $25$ / $1.0\ s$
* Maximum Number of Iterations: $100$
* Acyclicity Tolerance: $1.0 \times 10^{-8}$

## System Specifications

### Hardware
* CPU: AMD Ryzen 9 3950X
* GPU: Nvidia GeForce RTX 2070 SUPER
* Storage: Samsung Electronics 970 EVO Plus NVMe M.2 Internal SSD

### Software
* Kernel: Linux version 5.15.0-119-generic
* OS: Ubuntu 22.04.4 LTS ``Jammy"
* CMake: 3.22.1
* C++ Standard: 20
* G++: 11.4.0
* Libraries:
    - Eigen: 3.4.0
    - RapidJSON: 1.1.0
    - Qt: 5.15.3 (Components: Widgets)
    - SFML: 2.5.1 (Components: graphics)
    - Magic Enum: 0.9.5
    - RapidCSV: 8.82
