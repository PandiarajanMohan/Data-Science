class univariate():
    
    def quanqual(dataset):
        quan = []
        qual = []
        for columnname in dataset.columns:
            if dataset[columnname].dtype == 'O':
                qual.append(columnname)
            else:
                quan.append(columnname)
        return quan, qual