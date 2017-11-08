from nmf import NMF
import numpy as np
import matplotlib.pyplot as plt

m    = 100
n    = 80
rank = 14
error = 0.1
A = np.random.rand(m, 15)
B = np.random.rand(n, 15)
X = A.dot(B.T) + error * np.random.rand(m, n)

# Odstrani 30% podatkov
X[np.random.rand(m, n) < 0.3] = 0


model = NMF(rank=15, max_iter=20, eta=0.001)
model.fit(X)


plt.figure()
plt.plot(model.error)
plt.xlabel("Iteration")
plt.ylabel("J value")
plt.savefig("nmf-error.png")
plt.close()

fig, ax = plt.subplots(nrows=1, ncols=2)
ax[0].pcolor(X)
ax[0].set_title("Original")

ax[1].pcolor(model.predict_all())
ax[1].set_title("Model")
plt.savefig("nmf-model.png")
plt.close()
