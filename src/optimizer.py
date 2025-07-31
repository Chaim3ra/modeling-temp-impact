import cvxpy as cp
import numpy as np



def optimal_schedule(S, N, eta, gamma):
    x = cp.Variable(N, nonneg=True)

    
    objective = cp.sum(eta * x + 0.5 * gamma * cp.square(x))
    constraints = [cp.sum(x) == S]

    problem = cp.Problem(cp.Minimize(objective), constraints=constraints)
    problem.solve()

    return x.value


if __name__ == "__main__":
    S, N = 50000, 25
    # taking param values from power-law model
    eta, gamma = 0.000125, 0.314410
    schedule = optimal_schedule(S, N, eta=eta, gamma=gamma)
    print("Optimal x_i:", schedule)