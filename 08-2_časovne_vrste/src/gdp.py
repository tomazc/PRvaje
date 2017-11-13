__author__ = 'martin'
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as ptc


countries = ["China", "Brazil", "Russian Federation", "India", "Sweden", "Italy", "Germany", "Japan"]
data = np.zeros((len(countries), 43))
years = range(1970, 2013)

d = open("data/Download-GDPPC-USD-countries.csv", "r", encoding="utf-8")
for line in d.readline().split("\r"):
    ctr = line.strip().split(",")[0]
    if ctr in countries:
        i = countries.index(ctr)
        for ti, t in enumerate(line.strip().split(",")[1:]):
            data[i, ti] = float(t)


print(data)
print(data.shape)

quit()

# Normalize data
datan = data / data.sum(axis=0).reshape(1, 43)

fig, ax = plt.subplots()
args = [years] + [data[j, :] for j in range(len(countries))]
stack_coll = ax.stackplot(*args)
ax.set_xlim([years[0], years[-1]])
proxy_rects = [ptc.Rectangle((0, 0), 1, 1, fc=pc.get_facecolor()[0]) for pc in stack_coll]
ax.legend(proxy_rects, countries, bbox_to_anchor=(1.45, 1))

plt.xlabel("Year")
plt.title("GDP per capita (USD)")

plt.savefig("../results/gdp.png", bbox_inches="tight", format="png")


fig, ax = plt.subplots()
args = [years] + [datan[j, :] for j in range(len(countries))]
stack_coll = ax.stackplot(*args)
ax.set_xlim([years[0], years[-1]])
ax.set_ylim([0, 1])
proxy_rects = [ptc.Rectangle((0, 0), 1, 1, fc=pc.get_facecolor()[0]) for pc in stack_coll]
ax.legend(proxy_rects, countries, bbox_to_anchor=(1.45, 1))

plt.xlabel("Year")
plt.title("GDP per capita (USD)")

plt.show()
# plt.savefig("../results/gdpn.png", bbox_inches="tight", format="png")
