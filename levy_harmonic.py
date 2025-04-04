import math, random

def levy(L, N):
    x = [0.0]
    for k in range(1, N):
        x_mean = ((N - k) * x[k - 1] + L) / (1.0 + N - k)
        sigma = math.sqrt(1.0 / (1.0  + 1.0 / (N - k) ))
        x.append(random.gauss(x_mean, sigma))
    x.append(L)
    return(x)

def U(x):
    U = 0.0
    for k in range(N):
        k_minus = (k - 1) % N
        x_minus = x[k_minus] 
        if k == 0: x_minus -= L
        U += (x[k] - x_minus) ** 2 / 2.0
    return U

N = 8
L = 16
Sum_means = 0.0
Sum_mean_squares = 0.0
n_trials = 1000000
xstart, xend = 0.0, L
for step in range(n_trials):
    x = levy(L, N)
    dummy = U(x)
    Sum_means += dummy 
    Sum_mean_squares += dummy ** 2
error = math.sqrt((Sum_mean_squares / n_trials - (Sum_means / n_trials) ** 2) / n_trials)
print(Sum_means / n_trials, error)
