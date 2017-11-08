import numpy as np

def generate_random_polynomial(x, degree=2, noise=0.5, ):
    """
        Generate random 1-D polynomial at x
        with random coefficeints and given noise.
    """
    
    # Number of data points
    n = len(x)
    
    # Random polynomial coefficients
    coeff = np.array(np.random.rand(degree+1, 1)).ravel()

    # Normally-distributed errors
    error = np.array(np.random.randn(len(x), 1) * noise).ravel() 

    # Compute polynomial at sample points x
    y = np.zeros((len(x), ))
    for i, x in enumerate(x):
        y[i] = np.sum([coeff[di] * x**d for di, d in enumerate(range(degree+1))])
        y[i] = y[i] + error[i]
    
    
    return y, coeff


if __name__ == "__main__":
    
    x = np.linspace(-3, 3, 101)
    for d, n in zip([1, 3, 5], [0.3, 2.0, 7]):
        y, coeff = generate_random_polynomial(x, degree=d, noise=n)

        fname = "data/synthetic/coefficients_d-%d.txt" % d
        np.savetxt(fname, coeff)
        
        data = np.vstack([x.ravel(), y.ravel()])
        fname = "data/synthetic/data_d-%d.txt" % d
        np.savetxt(fname, data)
        
        
