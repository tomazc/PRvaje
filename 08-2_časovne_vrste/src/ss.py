import numpy as np
D = np.array([
        [0, 1, 3, 4],
        [4, 5, 0, 2],
        [2, 1, 3, 5], 
    ])

nz = D.nonzero()
print D
print nz
print
ratings = D[nz]


print ratings
classes = ratings > 3
print classes
print

from sklearn.cross_validation import StratifiedShuffleSplit

ss = StratifiedShuffleSplit(classes, n_iter=5, test_size=0.5)
for tr, te in ss:
    print
    print "Training:", tr, classes[tr]
    print "Test:", te, classes[te]
    print ratings[te]

    quit()
    D_ucna = D.copy()
    for i in te: 
        D_ucna[nz[0][i], nz[1][i]] = 0


# W, H = nmf(D_ucna)
for i in te: 
    napoved = W[nz[0][i], :].dot(H[:, nz[1][i]])




