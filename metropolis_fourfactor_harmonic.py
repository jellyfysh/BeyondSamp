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
b = 2.0
delta = 1.0
Sum_means = 0.0
Sum_mean_squares = 0.0
n_steps = 1000000
n_trials = 10

for trials in range(n_trials):
    x = levy(L, N)
    U_mean = 0.0
    for step in range(n_steps):
        k = random.randint(0, N - 1)
        k_plus = (k + 1) % N
        k_minus = (k - 1) % N
        x_plus = x[k_plus]
        if k == N - 1: x_plus += L
        if k_plus == N: x_plus = x[0] + L
        x_minus = x[k_minus]
        if k == 0: x_minus -= L
        x_new = x[k] + random.uniform(-delta, delta)
        U_k_plus = (x_plus - x[k]) ** 2 / 2.0
        U_k_minus = (x[k] - x_minus) ** 2 / 2.0 
        U_k_prime_plus = (x_plus - x_new) ** 2 / 2.0
        U_k_prime_minus = (x_new - x_minus) ** 2 / 2.0
        U_f_plus = -b * (x_plus - x[k])
        U_f_minus = -b * (x[k] - x_minus)
        U_f_prime_plus = -b * (x_plus - x_new)
        U_f_prime_minus = -b * (x_new - x_minus)

        Upsilon_k_plus = random.uniform(0.0, 1.0)
        Upsilon_k_minus = random.uniform(0.0, 1.0)
        Upsilon_f_plus = random.uniform(0.0, 1.0)
        Upsilon_f_minus = random.uniform(0.0, 1.0)
        if Upsilon_k_plus < math.exp(- (U_k_prime_plus - U_k_plus)) and \
               Upsilon_k_minus < math.exp(- (U_k_prime_minus - U_k_minus)) and  \
               Upsilon_f_plus < math.exp(- (U_f_prime_plus - U_f_plus)) and  \
               Upsilon_f_minus < math.exp(- (U_f_prime_minus - U_f_minus)): 
            x[k] = x_new
        U_mean += U(x)
    U_mean = U_mean / n_steps
    Sum_means += U_mean
    Sum_mean_squares += U_mean ** 2
error = math.sqrt((Sum_mean_squares / n_trials - (Sum_means / n_trials) ** 2) / n_trials)
print(Sum_means / n_trials, error)
