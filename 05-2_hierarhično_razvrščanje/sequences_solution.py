from itertools import product
def seq_to_kmer_count(seq, k=4):
    ktuples = list(zip(*[seq[i:] for i in range(k)]))     # razbijemo niz na k-terke
    kmers   = list(product(*(k*[["A", "C", "T", "G"]])))  # vse mozne k-terke
    
    x = np.zeros((len(kmers), ))
    
    for ki, kmer in enumerate(kmers):
        x[ki] = ktuples.count(kmer)
    return x

# ...k = 4
keys = sequences.keys()
X    = np.zeros((len(keys), 4**k))
for ki, ky in enumerate(keys):
    seq    = sequences[ky]
    X[ki]  = seq_to_kmer_count(seq, k=k)

print(X)
print(X.shape)
H = sch.linkage(X)
D = sch.dendrogram(H, labels=list(sequences.keys()), leaf_rotation=90)
plt.ylabel("Razdalja")
plt.show()
