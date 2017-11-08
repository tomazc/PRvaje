from generate_data import generate_random_polynomial

x = np.linspace(-3, 3, 101)
for name, d, n in zip(["A", "B", "C", "D", "E"], 
                      [1, 2, 3, 5, 6], 
                      [0.2, 0.6, 2.0, 4, 7]):
    y, coeff = generate_random_polynomial(x, degree=d, noise=n)
    
    fname = "data/synthetic/coefficients_%s.txt" % name
    np.savetxt(fname, coeff)

    data = np.hstack([x.reshape((len(x), 1)), y.reshape((len(y), 1))])
    fname = "data/synthetic/data_%s.txt" % name
    np.savetxt(fname, data)
    
print("OK.")
