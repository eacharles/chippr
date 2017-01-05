import numpy as np
import sys

import chippr
from chippr import utils as u

class gmix(object):

    def __init__(self, amps, means, sigmas, limits=(-1./u.eps, 1./u.eps)):
        """
        Object to define a Gaussian mixture probability distribution

        Parameters
        ----------
        amps: ndarray, float
            array with one relative amplitude per component
        means: ndarray, float
            array with one mean per component
        sigmas: ndarray, float
            array with one standard deviation per component
        limits: tuple or list or numpy.ndarray, float, optional
            minimum and maximum sample values to return
        """

        self.amps = amps/np.sum(amps)
        self.cumamps = np.cumsum(self.amps)
        self.means = means
        self.sigmas = sigmas
        self.n_comps = len(self.amps)

        self.funcs = [chippr.gauss(self.means[c], self.sigmas[c]**2) for c in range(self.n_comps)]

        self.min_x = limits[0]
        self.max_x = limits[1]

    def evaluate(self, xs):
        """
        Function to evaluate the Gaussian mixture probability distribution at many points

        Parameters
        ----------
        xs: ndarray, float
            values at which to evaluate Gaussian mixture probability distribution

        Returns
        -------
        ps: ndarray, float
            values of Gaussian mixture probability distribution at xs
        """
        ps = np.zeros_like(xs)
        for c in range(self.n_comps):
            ps += self.amps[c] * self.funcs[c].evaluate(xs)
        return ps

    def sample_one(self):
        """
        Function to sample a single value from Gaussian mixture probability distribution

        Returns
        -------
        x: float
            a single point sampled from the Gaussian mixture probability distribution
        """

        x = -1.
        while x < self.min_x or x > self.max_x:
            r = np.random.uniform(0., self.cumamps[-1])
            c = 0
            for k in range(1, self.n_comps):
                if r > self.cumamps[k-1]:
                    c = k
            x = self.funcs[c].sample_one()
        return x

    def sample(self, n_samps):
        """
        Function to take samples from Gaussian mixture probability distribution

        Parameters
        ----------
        n_samps: int
            number of samples to take

        Returns
        -------
        xs: ndarray, float
            array of points sampled from the Gaussian mixture probability distribution
        """
        xs = np.array([self.sample_one() for n in range(n_samps)])
        return xs
