import math, cmath, random

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
n_trials = 10
b = 2.0 
n_steps = 100000
for Iter in range(n_trials):
    x = levy(L, N)
    k = random.randint(0, N - 1)
    k_non_per = k
    time_interval = N
    time_to_go = time_interval
    time = 0.0
    U_mean = 0.0
    NData = 0
    while NData < n_steps:
        k_plus = (k + 1) % N
        k_minus = (k - 1) % N
        x_plus = x[k_plus] 
        if k == N - 1: x_plus += L
        x_minus = x[k_minus] 
        if k == 0: x_minus -= L
        Upsilon_h_plus = -2.0 * math.log(random.uniform(0.0, 1.0))
        Upsilon_h_minus = -2.0 * math.log(random.uniform(0.0, 1.0))
        Upsilon_f_plus = - math.log(random.uniform(0.0, 1.0))
#
#   forward factor (harmonic and factor-field)
#
        if x[k] < x_plus: Del_h_plus = (x_plus - x[k]) + math.sqrt(Upsilon_h_plus)
        else: Del_h_plus = x_plus - x[k] + math.sqrt(Upsilon_h_plus + (x[k] - x_plus) ** 2) 
        Del_f_plus = Upsilon_f_plus / b
        Del_plus = min(Del_h_plus, Del_f_plus)
#
#   backward factor (harmonic only)
#
        if x[k] < x_minus: 
             Del_minus = (x_minus - x[k]) + math.sqrt(Upsilon_h_minus)
        else: 
            Del_minus = x_minus - x[k] + math.sqrt(Upsilon_h_minus + (x[k] - x_minus) ** 2) 
            
        if time_to_go < min(Del_plus, Del_minus): # sampling at regular intervals 
            time += time_interval 
            x[k] += time_to_go
            time_to_go = time_interval
            U_mean += U(x)
            NData += 1
        elif Del_plus < Del_minus:
            x[k]  = x[k] + Del_plus
            time_to_go -= Del_plus
            k_non_per = k_non_per + 1
            k = k_plus
        else:
            x[k] = x[k] + Del_minus
            time_to_go -= Del_minus
            k_non_per = k_non_per - 1
            k = k_minus

    U_mean = U_mean / NData
    Sum_means += U_mean
    Sum_mean_squares += U_mean ** 2
error = math.sqrt((Sum_mean_squares / n_trials - (Sum_means / n_trials) ** 2) / n_trials)
print(Sum_means / n_trials, error)
