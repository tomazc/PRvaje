class KMeans:
    
    def __init__(self, k=10, max_iter=100):
        """
        Initialize KMeans clustering model.
        
        :param k
            Number of clusters.
        :param max_iter
            Maximum number of iterations.
        """
        self.k         = k
        self.max_iter  = max_iter    
    
    def fit(self, X):
        """
        Fit the Kmeans model to data.
        
        :param X
            Numpy array of shape (n, p)
            n: number of data examples
            p: number of features (attributes)
        
        :return 
            labels: array of shape (n, ), cluster labels (0..k-1)
            centers: array of shape (p, )
        """
        
        n, p    = X.shape
        labels  = np.random.choice(range(self.k), size=n, replace=True)
        centers = np.random.rand(self.k, p)
        
        ### Your code here ###
        centers = np.min(X, axis=0) + centers * (np.max(X, axis=0) - np.min(X, axis=0)) 
        
        i = 0
        while i < self.max_iter:
            
            # Find nearest cluster
            for j, x in enumerate(X):
                ki = np.argmin(np.sum((centers - x) ** 2, axis=1))
                labels[j] = ki
                
            # Move centroid
            for ki in range(self.k):
                centers[ki] = X[labels == ki].mean(axis=0)    
            i += 1
        
        ### Your code here ###
        return labels, centers


