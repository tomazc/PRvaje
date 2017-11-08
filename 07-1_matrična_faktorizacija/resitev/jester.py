import numpy as np
import matplotlib.pyplot as plt

def load_jester(p=0.05):
    """
    :param p: Probability of rating appearing in the training set.
    :return
        X training grades (retining with probability p)
        Y test grades (whole dataset) 
    """

    Y = np.genfromtxt("jester-data.csv", delimiter=",", dtype=float, )
    Y = Y[:, 1:]
    Y[Y == 99] = 0 
    Y[Y != 0]  = Y[Y!=0] + abs(Y[Y!=0].min())

    # Separate data in test/train with probability p
    M = np.random.rand(*Y.shape) 
    M_tr = M < p
    M_te = M > p
    X = Y * M_tr
    Y = Y * M_te

    return X, Y

from nmf import NMF
X, Y = load_jester(p=0.5)

X = X[:1000, :]
Y = Y[:1000, :]

print("X, Nonzeros:", np.sum(X>0), "Total:", X.shape[0]*X.shape[1])
print("Y, Nonzeros:", np.sum(Y>0), "Total:", Y.shape[0]*Y.shape[1])

# model = NMF(rank=10, eta=0.001, max_iter=200) # 20% expl variance
model = NMF(rank=15, eta=0.001, max_iter=200)   # 24% expl variance
model.fit(X)

Yp       = model.predict_all()
expl_var = (np.var(Y[Y>0]) - np.var(Y[Y>0] - Yp[Y>0])) / np.var(Y[Y>0])
print("Explained variance: ", expl_var)

plt.figure()
plt.plot(model.error)
plt.xlabel("Iteration")
plt.ylabel("J value")
plt.savefig("nmf-error.png")
plt.close()

fig, ax = plt.subplots(nrows=1, ncols=2)
ax[0].pcolor(Y[:500, :][:, :500])
ax[0].set_title("Data")

ax[1].pcolor(model.predict_all()[:500, :][:, :500])
ax[1].set_title("Model")
plt.savefig("nmf-model.png")
plt.close()
