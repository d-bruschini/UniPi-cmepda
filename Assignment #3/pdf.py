import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from matplotlib import pyplot as plt
from numpy import diff
from scipy.stats import chisquare



class ProbabilityDensityFunction(InterpolatedUnivariateSpline):

    """Class describing a probability density function.
    """

    def __init__(self, x, y, k=3):
        """Constructor.
        """
        InterpolatedUnivariateSpline.__init__(self, x, y, None, [None]*2, k)
        ycdf = np.array([self.integral(x[0], xcdf) for xcdf in x])
        self.cdf = InterpolatedUnivariateSpline(x, ycdf)
        mask=diff(ycdf) > 0.0
        mask=np.append(mask,False)
        #print(mask)
        #print(ycdf[mask])
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
    
def distribution(x):
    return 1./np.sqrt(np.pi)*np.exp(-(x**2))


if __name__ == '__main__':
    x = np.linspace(-3., 3., 40)
    y = distribution(x)
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
    random_numbers=1000000
    rnd = pdf.rnd(random_numbers)
    bins=200
    occurrences, binning, = plt.hist(rnd, bins)
    binning2=0.5 * (binning[1:] + binning[:-1])
    bin_chi2=random_numbers*distribution(binning2)*(binning[len(binning)-1]-binning[0])/bins
    chi2,p_value=chisquare(occurrences,bin_chi2)
    string="Chi2 = {}, p-value = {}"
    print(string.format(chi2,p_value))    

    print(pdf.prob(0.2,0.8))
"""
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
    random_numbers=1000000
    rnd = pdf.rnd(random_numbers)
    bins=200
    occurrences,binning,patches=plt.hist(rnd, bins)
    binning2=np.array([(binning[i]+binning[i+1])/2 for i in range(0,len(binning)-1)])
    bin_chi2=random_numbers*distribution(binning2)*(binning[len(binning)-1]-binning[0])/bins
    chi2,p_value=chisquare(occurrences,bin_chi2)
    print(string.format(chi2,p_value))    
    
    print(pdf.prob(0.2,0.8))"""

    plt.show()
