import mlpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm


x = [0,0,0,0,1,1,2,2,3,2,1,1,0,0,0,0]
y = [0,0,1,1,2,2,3,3,3,3,2,2,1,1,0,0]



dist, cost, path = mlpy.dtw_std(x, y, dist_only=False)

fig0 = plt.figure(1)
plt.plot(x, "b")
plt.plot(y, "r")

fig = plt.figure(2)
ax = fig.add_subplot(111)
plot1 = plt.imshow(cost.T, origin='lower', cmap=cm.gray, interpolation='nearest')
plot2 = plt.plot(path[0], path[1], 'w')
xlim = ax.set_xlim((-0.5, cost.shape[0]-0.5))
ylim = ax.set_ylim((-0.5, cost.shape[1]-0.5))
plt.show()
