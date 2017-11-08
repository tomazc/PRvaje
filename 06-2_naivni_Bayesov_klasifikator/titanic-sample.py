from Orange.data import Table
from numpy.random import shuffle

data = Table("titanic")
inxs = list(range(len(data)))
n = len(inxs)

shuffle(inxs)

data_training = data[inxs[:n//2]]
data_test     = data[inxs[n//2:]]

data_training.save("titanic-training.tab")
data_test.save("titanic-test.tab")
