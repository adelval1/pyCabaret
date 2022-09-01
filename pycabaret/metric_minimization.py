import numpy as np


def metric(var, func, constraints, args):
    for i in range(len(var)):
        if var[i] < constraints[i][0] or var[i] > constraints[i][1]:
            if len(var) == 1:
                return 1.0e16
            else:
                return [1.0e16] * len(var)

    feval = func(var, args)

    residual = [feval[i] for i in range(len(var))]
    metric = [np.linalg.norm(residual[i]) for i in range(len(residual))]

    if len(metric) == 1:
        return metric[0]
    else:
        return metric
