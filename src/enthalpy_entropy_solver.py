import numpy as np 
import mutationpp as mpp
import rebuilding_setup as setup
import scipy
from scipy.optimize import minimize

class enthalpy_entropy_solver:

    def __init__(self,resmin,h,s,mix):
        self.resmin = resmin
        self.h = h
        self.s = s
        self.mix = mix

    def set_resmin(self,resmin):
        self.resmin = resmin

    def func_minimize(self,var):
        ## Setting positivity constraints ## Ideally this is done by the optimization method but I don't have latest scipy with my python distribution
        if var[0]<0:
            var[0] = 300.0
        elif var[1]<0:
            var[1] = 5.0

        setup.mixture_states(self.mix)["reservoir"].equilibrate(var[0],var[1])
        if self.v0 !=0.:
            self.v0 = setup.mixture_states(self.mix)["reservoir"].equilibriumSoundSpeed()
        
        h_0 = setup.mixture_states(self.mix)["reservoir"].mixtureHMass() + 0.5*(self.v0**2)
        s_0 = setup.mixture_states(self.mix)["reservoir"].mixtureSMass()

        residual = [self.h-h_0, self.s-s_0]
        metric = np.linalg.norm(residual)
        return metric

    def solution(self,T,p,v_0=0.):

        ## Initial conditions ##
        T_0 = T
        p_0 = p
        var = [T_0,p_0]
        self.v0=v_0

        ## Conserved variables ##
        setup.mixture_states(self.mix)["free_stream"].equilibrate(T,p)

        result = scipy.optimize.minimize(self.func_minimize,var,method='Nelder-Mead',tol=self.resmin)

        if self.v0 !=0.:
            setup.mixture_states(self.mix)["reservoir"].equilibrate(result.x[0],result.x[1])
            self.v0 = setup.mixture_states(self.mix)["reservoir"].equilibriumSoundSpeed()

        return result.x[0],result.x[1],self.v0