import numpy as np 
import mutationpp as mpp
import rebuilding_setup as setup
import scipy
from scipy.optimize import minimize

class enthalpy_entropy_solver:

    def __init__(self,resmin,h,s,mix,state,name):
        self.resmin = resmin
        self.h = h
        self.s = s
        self.mix = mix
        self.state = state
        self.name = name

    def set_resmin(self,resmin):
        self.resmin = resmin

    def func_minimize(self,var,T,p,resini,constraint_type,constraints):

        real = [var[0]*T,var[1]*p]
        # real = [T,p]

        setup.mixture_states(self.mix)[self.state].equilibrate(real[0],real[1])
        if self.v0 !=0.:
            self.v0 = setup.mixture_states(self.mix)[self.state].equilibriumSoundSpeed()
        
        h_0 = setup.mixture_states(self.mix)[self.state].mixtureHMass() + (0.5*(self.v0**2))
        s_0 = setup.mixture_states(self.mix)[self.state].mixtureSMass()

        residual = [(h_0-self.h)/self.h, (s_0-self.s)/self.s]
        metric = np.linalg.norm(residual)/resini
        # metric = ((residual[0]**2)+(residual[0]**2))/resini
        return metric

    def solution(self,T,p,constraint_type,constraints,v_0=0.):

        ## Initial conditions ##
        var = [1.,1.]
        # var = [T,p]
        self.v0=v_0
        resini = 1.0
        resini = self.func_minimize(var,T,p,resini,constraint_type,constraints)

        bnds = ((0.01, None), (0.01, None))
        # bnds = ((T, None), (p, None))
        options={'maxiter': None}
        result = scipy.optimize.minimize(self.func_minimize,var,args=(T,p,resini,constraint_type,constraints),method='Nelder-Mead',bounds=bnds,tol=self.resmin,options=options)
        if result.nit == 400:
            print("Number of maximum iterations reached. Convergence not guaranteed for"+' '+self.name)
            exit(0)

        if self.v0 !=0.:
            setup.mixture_states(self.mix)[self.state].equilibrate(result.x[0]*T,result.x[1]*p)
            self.v0 = setup.mixture_states(self.mix)[self.state].equilibriumSoundSpeed()

        return result.x[0]*T,result.x[1]*p,self.v0