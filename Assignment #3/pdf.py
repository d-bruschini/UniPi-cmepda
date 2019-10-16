import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from matplotlib import pyplot as plt
from numpy import diff



class ProbabilityDensityFunction(InterpolatedUnivariateSpline):

    """Class describing a probability density function.
    """

    def __init__(self, x, y, k=3):
        """Constructor.
        """
        InterpolatedUnivariateSpline.__init__(self, x, y, None, [None]*2, k)
        ycdf = np.array([self.integral(min(x), xcdf) for xcdf in x])
        self.cdf = InterpolatedUnivariateSpline(x, ycdf)
        mask=diff(ycdf) > 0.0
        mask=np.append(mask,False)
        print(mask)
        print(ycdf[mask])
        self.ppf = InterpolatedUnivariateSpline(ycdf[mask], x[mask])

    def prob(self, x1, x2):
        """Return the probability for the random variable to be included 
        between x1 and x2.
        """
        return self.cdf(x2) - self.cdf(x1)

    def rnd(self, size=1000):
        """Return an array of random values from the pdf.
        """
        return self.ppf(np.random.uniform(size=size))
    



if __name__ == '__main__':
    x = np.linspace(-3., 3., 40)
    y = 1./np.sqrt(np.pi)*np.exp(-(x**2))
    pdf = ProbabilityDensityFunction(x, y)
    a = np.array([0.2, 0.6])
    print(pdf(a))

    array_=np.linspace(-3.,3.,500)

    plt.figure('pdf')
    plt.plot(array_, pdf(array_))
    plt.xlabel('x')
    plt.ylabel('pdf(x)')

    plt.figure('cdf')
    plt.plot(array_, pdf.cdf(array_))
    plt.xlabel('x')
    plt.ylabel('cdf(x)')


    z=np.linspace(0.,1.,300)
    plt.figure('ppf')
    plt.plot(z, pdf.ppf(z))
    plt.xlabel('x')
    plt.ylabel('ppf(x)')

    plt.figure('Sampling')
    rnd = pdf.rnd(1000000)
    plt.hist(rnd, bins=200)
    
    print(pdf.prob(0.2,0.8))

    pdf = ProbabilityDensityFunction(x, y, 1)
    a = np.array([0.2, 0.6])
    print(pdf(a))

    plt.figure('pdf2')
    plt.plot(array_, pdf(array_))
    plt.xlabel('x')
    plt.ylabel('pdf(x)')

    plt.figure('cdf2')
    plt.plot(array_, pdf.cdf(array_))
    plt.xlabel('x')
    plt.ylabel('cdf(x)')


    z=np.linspace(0.,1.,300)
    plt.figure('ppf2')
    plt.plot(z, pdf.ppf(z))
    plt.xlabel('x')
    plt.ylabel('ppf(x)')

    plt.figure('Sampling2')
    rnd = pdf.rnd(1000000)
    plt.hist(rnd, bins=200)
    
    print(pdf.prob(0.2,0.8))

    plt.show()
