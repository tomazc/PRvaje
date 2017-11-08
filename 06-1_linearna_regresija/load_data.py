from pickle import load
from os.path import join

def load_data(dset):
    data = dict()

    indir = "data/%s/" % dset

    for name in "data", "target", "data_test", "target_test":
        fname = join(indir, name + ".pkl")
        data[name] = load(open(fname, "rb"))

        fname = join(indir, "features.txt")
        fp = open(fname, "rt")
        data["features"] = list(map(lambda l: l.strip(), fp.readlines()))

    return data


data = load_data("books")
