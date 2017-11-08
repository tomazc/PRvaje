plt.figure(figsize=(6, 8))

for si, sport in enumerate(sports):
    
    xs = heights_by_sport[sport]    # x os
    ys = [si for x in xs]           # y os je v visini sporta
    zs = weights_by_sport[sport]    # velikost točke je premosorazmerna s tezo
    
    for x, y, z in zip(xs, ys, zs): # rišemo točko po točko
        plt.plot(x, y, "m.", alpha=0.5, markersize=z/5)
            
plt.yticks(range(len(sports)))
plt.ylim(-0.5, len(sports)-0.5)
plt.gca().set_yticklabels(sports)
        
plt.xlabel("Višina (cm)")
plt.ylabel("Šport")
plt.show()
