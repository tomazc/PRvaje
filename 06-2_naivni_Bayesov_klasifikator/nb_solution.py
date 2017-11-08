class NaiveBayes:
    
    
    """
    Naive Bayes classifier.
    

    :attribute self.probabilities
        Dictionary that stores
            - prior class probabilities P(Y)
            - attribute probabilities conditional on class P(X|Y)
    
    :attribute self.class_values
        All possible values of the class.
        
    :attribute self.variables
        Variables in the data. 
    
    :attribute self.trained
        Set to True after fit is called.
    """
    
    def __init__(self):
        self.trained       = False
        self.probabilities = dict()   
    
    
    def fit(self, data):
        """
        Fit a NaiveBayes classifier.
        
        :param data
            Orange data Table.        
        """
        class_variable      = data.domain.class_var    # class variable (Y) 
        self.class_values   = class_variable.values    # possible class values
        self.variables      = data.domain.variables    # all other variables (X)
        
        n = len(data) # number of all data points
        
        # Compute P(Y)
        for y in self.class_values:

            # A not too smart guess (INCORRECT)
            self.probabilities[y] = 1/len(self.class_values)
            
            # <your code here>
            # Compute class probabilities and correctly fill
            #   probabilities[y] = ... 
            # Select all examples (rows) with class = y
            filt = SameValue(data.domain.class_var, y)
            data_subset = filt(data)
            m = len(data_subset)
        
            self.probabilities[y] = m/n
            # </your code here>
        
        # Compute P(X|Y)
        for y in self.class_values:
            
            # Select all examples (rows) with class = y
            filty = SameValue(class_variable, y)
            
            for variable in self.variables:
                for x in variable.values:
                    
                    # A not too smart guess (INCORRECT)
                    p = 1 / (len(self.variables) * len(variable.values) * len(self.class_values))
                    self.probabilities[variable, x, y] = p
                    
                
                    # <your code here>
                    # Compute correct conditional class probability
                    #   probabilities[x, value, c] = ... 
                    # 
                    # Select all examples with class == y AND 
                    # variable x == value
                    # Hint: use SameValue filter twice
                    filtx = SameValue(variable, x)
                    data_subset = filtx(filty(data))
                    m = len(data_subset)
                    
                    data_subset = filty(data)
                    p = len(data_subset)
                    
                    self.probabilities[variable, x, y] = m/p
                    # </your code here>
    
        self.trained = True
        
    
    def predict_instance(self, row):
        """
        Predict a class value for one row.
        
        :param row
            Orange data Instance.
        :return 
            Class prediction.
        """
        curr_p = float("-inf")   # Current highest "probability" (unnormalized)
        curr_c = None            # Current most probable class
        
        for y in self.class_values:
            p = np.log(self.probabilities[y])
            for x in self.variables:
                p = p + np.log(self.probabilities[x, row[x].value, y])
            
            if p > curr_p:
                curr_p = p
                curr_c = y
                
        return curr_c, curr_p
        
   

    def predict(self, data):
        """
        Predict class labels for all rows in data.
        
        :param data
            Orange data Table.       
        :return y
            NumPy vector with predicted classes.
        """
        
        n = len(data)
        predictions = list()
        confidences = np.zeros((n, ))
        
        for i, row in enumerate(data):
            pred, cf = self.predict_instance(row)
            predictions.append(pred)
            confidences[i] = cf
    
        return predictions, confidences
