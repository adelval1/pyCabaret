import numpy as np 
import mutationpp as mpp
import rebuilding_setup as setup
import scipy
from scipy.optimize import minimize
from scipy import misc

class enthalpy_entropy_solver:

    def __init__(self,resmin,h,s,mix,state,name,options):
        self.resmin = resmin
        self.h = h
        self.s = s
        self.mix = mix
        self.state = state
        self.name = name
        self.options = options

    def set_resmin(self,resmin):
        self.resmin = resmin

    def func_minimize(self,var,T,p,resini,constraint_type,constraints):
        for i in range(len(var)):
            if var[i]<0.0:
                return 1.0e+16

        real = [var[0]*T,var[1]*p]

        setup.mixture_states(self.mix)[self.state].equilibrate(real[0],real[1])
        if self.v0 !=0.:
            self.v0 = setup.mixture_states(self.mix)[self.state].equilibriumSoundSpeed()
        
        h_0 = setup.mixture_states(self.mix)[self.state].mixtureHMass() + (0.5*(self.v0**2))
        s_0 = setup.mixture_states(self.mix)[self.state].mixtureSMass()

        residual = [(h_0-self.h)/self.h, (s_0-self.s)/self.s]
        metric = np.linalg.norm(residual)/resini
        return metric

    def vect_func_minimize(self,var,T,p,resini,constraint_type,constraints):
        for i in range(len(var)):
            if var[i]<0.0:
                return [1.0e+16]*len(var)

        real = [var[0]*T,var[1]*p]

        setup.mixture_states(self.mix)[self.state].equilibrate(real[0],real[1])
        if self.v0 !=0.:
            self.v0 = setup.mixture_states(self.mix)[self.state].equilibriumSoundSpeed()
        
        h_0 = setup.mixture_states(self.mix)[self.state].mixtureHMass() + (0.5*(self.v0**2))
        s_0 = setup.mixture_states(self.mix)[self.state].mixtureSMass()

        residual = [(h_0-self.h)/self.h, (s_0-self.s)/self.s]
        metric = [np.linalg.norm(residual[i]) for i in range(len(residual))]
        return metric

    def jacobian(self,var,T,p,resini,constraint_type,constraints):
        jacob = scipy.optimize.approx_fprime(var,self.func_minimize,1.0e-10,T,p,resini,constraint_type,constraints)
        return jacob

    def solution(self,T,p,constraint_type,constraints,v_0=0.):

        ## Initial conditions ##
        var =[self.options["temperature"],self.options["pressure"]] #[10.,100.]
        self.v0=v_0
        resini = 1.0
        resini = self.func_minimize(var,T,p,resini,constraint_type,constraints)

        bnds = ((1.0, None), (1.0, None)) 
        options={'maxiter': None}
        if self.options["robust"] == "Yes":
            result = scipy.optimize.minimize(self.func_minimize,var,args=(T,p,resini,constraint_type,constraints),method='Powell',tol=self.resmin,bounds=bnds,options=options)

            if result.success == False:
                print("Warning: convergence not guaranteed for"+' '+self.name)

        else:
            result = scipy.optimize.root(self.vect_func_minimize,var,args=(T,p,resini,constraint_type,constraints),tol=self.resmin)

            if result.success == False:
                print("Warning: convergence not guaranteed for"+' '+self.name)

        if self.v0 !=0.:
            setup.mixture_states(self.mix)[self.state].equilibrate(result.x[0]*T,result.x[1]*p)
            self.v0 = setup.mixture_states(self.mix)[self.state].equilibriumSoundSpeed()

        return result.x[0]*T,result.x[1]*p,self.v0