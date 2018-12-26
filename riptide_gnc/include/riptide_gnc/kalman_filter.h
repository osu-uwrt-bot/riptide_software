#ifndef KALMAN_FILTER
#define KALMAN_FILTER

#include "eigen3/Eigen/Dense"

using namespace Eigen;

class KalmanFilter // Basic Kalman Filter
{
public:
    float m, n; // m = # measurements, n = # states
    VectorXf Xhat; // State Vector
    MatrixXf A; // State-transition Matrix
    MatrixXf H; // Measurement Matrix
    MatrixXf K; // Kalman Gain
    MatrixXf P; // Error Covariance Matrix
    MatrixXf Q; // Process Noise Covariance Matrix
    MatrixXf R; // Measurement Noise Covariance Matrix
    MatrixXf I; // Identity Matrix
    bool init;
private:
    KalmanFilter(MatrixXf Ao, MatrixXf Ho, MatrixXf Qo, MatrixXf Ro);
    void InitKF(VectorXf Xo);
    void UpdateKF(VectorXf Z);
    void UpdateKFOverride(VectorXf Xpredict, Vector Xf Z, MatrixXf Anew, Matrix Hnew);
};

#endif