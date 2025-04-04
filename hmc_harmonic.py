import math, cmath, random

def levy(L, N):
    x = [0.0]
    for k in range(1, N):        # loop over internal slices
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

def grad_U(x, k):
    k_plus = (k + 1) % N
    k_minus = (k - 1) % N
    x_plus = x[k_plus] 
    if k == N - 1: x_plus += L
    x_minus = x[k_minus] 
    if k == 0: x_minus -= L
    return 2.0 * x[k] - x_minus - x_plus

def LeapFrog(x, p, epsilon, I):
    p = [p[k] - epsilon * grad_U(x, k) / 2.0 for k in range(N)]
    for iter in range(I):
        x = [x[k] + epsilon * p[k] for k in range(N)]
        if iter != I - 1: p = [p[k] - epsilon * grad_U(x, k) for k in range(N)]
    p = [p[k] - epsilon * grad_U(x, k) / 2.0 for k in range(N)]
    return x, p

N = 8
L = 16
epsilon = 0.1
Sum_means = 0.0
Sum_mean_squares = 0.0
n_trials = 10
I = int(0.25 * N / epsilon)
n_steps = 100000
for Iter in range(n_trials):
    x = levy(L, N)
    U_old = U(x)
    U_mean = 0.0
    for step in range(n_steps):
        U_mean += U_old
        p = [random.gauss(0.0, 1.0) for k in range(N)]
        K_old = sum([y ** 2 / 2.0 for y in p])
        x_new, p_new = LeapFrog(x, p, epsilon, I) 
        U_new = U(x_new)
        K_new = sum([y ** 2 / 2.0 for y in p_new])
        if random.uniform(0.0, 1.0)  < math.exp(- U_new + U_old - K_new + K_old):
            x = x_new[:]
            U_old = U_new
    U_mean = U_mean / n_steps
    Sum_means += U_mean
    Sum_mean_squares += U_mean ** 2
error = math.sqrt((Sum_mean_squares / n_trials - (Sum_means / n_trials) ** 2) / n_trials)
print(Sum_means / n_trials, error)
