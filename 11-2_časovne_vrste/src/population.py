# from geopy import geocoders
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import math
import numpy as np
import time
import pickle
import os
import mlpy
import scipy.cluster.hierarchy as sch

f = open("../data/prebivalstvo_slovenija.px", "r", )
data = np.zeros((177, 800)) # Spol, UE, polletje, starost
regions = list()
sexes = ["Both", "M", "F"]
times = list()
ages = list()
bool_reg = False
bool_data = False
bool_age = False
bool_time = False
replacements = {"\x9a":"s", "\xe8":"c", "\x9e":"z", "\xc8":"C", "\x8a":"S", "\x8e":"Z"}
line = f.readline()

c = 0
while line:
    if any([line.startswith(i) for i in ["VALUES", "CODES"]]):
        bool_reg = False
        bool_data = False
        bool_age = False
        bool_time = False

    if line.startswith("VALUES(\"UPRAVNA ENOTA\")=") or bool_reg:
        bool_reg = True
        temp = line.replace("VALUES(\"UPRAVNA ENOTA\")=", "").replace("\"", "").replace(";", "").strip()
        for key, rep in replacements.iteritems():
            temp = temp.replace(key, rep)
        regions.extend([s for s in temp.split(",") if s])

    if line.startswith("CODES(\"POLLETJE\")=") or bool_time:
        bool_time = True
        temp = line.strip().replace("CODES(\"POLLETJE\")=", "").replace("\"", "").replace(";","")
        times.extend([s for s in temp.split(",") if s])

    if line.startswith("VALUES(\"STAROST\")") or bool_age:
        bool_age = True
        temp = line.strip().replace("VALUES(\"STAROST\")=", "").replace("\"", "").replace(";","")
        ages.extend([s for s in temp.split(",") if s])

    if line.startswith("DATA="):
        bool_data = True

    elif bool_data:
        d = line.replace(";","").strip().split(" ")
        v = [int(di) for di in d]
        data[c, :] = v
        c += 1

    line = f.readline()

# reshape
ages = ages[:-2]
data = data.reshape((3, 59, 32, 25))

# Get region coordinates
if False:
    g = geocoders.GoogleV3()

    coords = dict()
    try:
        coords = pickle.load(open("data/coords.pkl"))
    except:
        for ue in regions:
            place, (lat, lng) = g.geocode("%s %s" % (ue, "Slovenija"), exactly_one=False)[0]
            time.sleep(2)
            coords[ue] = (lat, lng)
        pickle.dump(coords, open("data/coords.pkl", "w"))


    max_size = 300.0

i = 0
l = 0


if False:
    x = list()
    y = list()
    for ai, a in enumerate(ages):
        norm = data[0, 0, 0, ai]
        for ki, k in enumerate(times):
            plt.figure()
            for ui, ue in enumerate(regions):
                j = ui
                if ue == "SLOVENIJA":
                    continue
                # lat, lng = coords[ue]
                # size = data[i, j, ki, l] / data[i, 0, ki, l].astype(float) * max_size
                size = data[i, j, ki, ai] / norm * max_size
                x.append(lat)
                y.append(lng)
                plt.plot(lng, lat, "go", markersize=size)
                # plt.text(lng, lat, ue)
                plt.xlabel("Longitude")
                plt.ylabel("Latitude")
                plt.title(k)
            try: os.makedirs("../results/%s/" % a)
            except: pass
            plt.savefig("../results/%s/prebivalstvo_%s.png" % (a,k))
            plt.close("all")


# Compare regions using Dynamic Time Warping
for ai, a in enumerate(ages):
    reg_dtw = dict()
    for ui, ue in enumerate(regions):
        x = data[0, ui, :, ai]
        
        print(ue)
        fname = "../data/ages/%s_starost-%s.txt" % (ue.replace("/", "_"), a)
        fname = fname.replace(" ", "_")
        np.savetxt(fname, x)

        for vi, ve in enumerate(regions):
            if (ue, ve) in reg_dtw.keys():
                continue
            elif ue == ve:
                reg_dtw[(ue, ve)] = 0
            else:
                y = data[0, vi, :, ai]

                dist, cost, path = mlpy.dtw_std(x, y, dist_only=False)
                reg_dtw[(ue, ve)] = dist


    # Output distances between regions
    f = open("../results/primerjava_%s.txt" % a, "w",)
    for pair, d in sorted(reg_dtw.iteritems(), key=lambda e: e[1]):
        if d > 0:
            f.write("%s %s \n" % (pair, str(d)))
    f.close()

    # Plot top match
    fname = "../results/primerjava_%s.png" % a
    for pair, d in sorted(reg_dtw.iteritems(), key=lambda e: e[1]):
        if d > 0:
            plt.figure()
            plt.title("Prebivalstvo, starost: " + a)
            plt.plot(data[0, regions.index(pair[0]), :, ai])
            plt.plot(data[0, regions.index(pair[1]), :, ai])
            plt.legend([pair[0], pair[1]])
            plt.savefig(fname, format="png")
            break





