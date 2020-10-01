import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np 
import glob
import os
from scipy.stats import pearsonr

def findCSVs(csvDir, search_criteria):
    """
        Function to find .csvs which end in 'cen'
    """
    # find files that match the criteria within the directory
    CSVs = os.path.join(csvDir, search_criteria)

    # taking all the files that match and globbing together into a list
    all_CSVs = glob.glob(CSVs)
    print(len(all_CSVs),'.csv files found')
    return all_CSVs

def corrPlot(df_4_corr,ax):
    """
        Function which maps a correlation heatmap of an input
        pandas dataframe into an ax subplot
    """
    # Define colour palette
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    # Plot heatmap
    matrix = sns.heatmap(df_4_corr,cmap="RdYlGn", center=0, cbar=False, annot=False,square=True,linewidths=1, vmax=1, vmin=-1,ax=ax)
    return matrix 

# List of census .csv files to use
CSVs = findCSVs('../../Census/MALAWI/','*cen.csv')
print(CSVs)

# Open file to fill with output correlation data
file = open('./correlation_matrix.csv','w')

matrix_list = []  
for csv in CSVs:
    # For every census .csv (of each SID)
    # Open plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    print('-- Correlating clusters against',csv[20:-8],'--')
    # Read in census SID csv
    df1 = pd.read_csv(csv)
    # Read in cluster data
    df2 = pd.read_csv('../../Census/MALAWI/cluster_population.csv')
    
    # Correlate all SID variables against all clusters
    for col1 in df1.columns:
        for col2 in df2.columns:
            # Pearson's correlation coefficient
            corr,pval = pearsonr(df1[col1],df2[col2])
            # Check for significance
            if pval<0.05:
                decision = 'reject null'
            else:
                decision = 'accept null'
            # Add correlation coefficient, p-value, and null hypothesis outcome to file
            matrix_list.append(str(csv[20:-8])+','+str(col1)+','+str(col2)+','+str(corr)+','+str(pval)+','+str(decision)+'\n')
    
    # Combine SID data and cluster data into pandas dataframe for plotting
    comb = pd.concat([df1, df2], axis=1, keys=['df1', 'df2']).corr(method='pearson').loc['df2', 'df1']
    # Plot the correlation
    matrix = corrPlot(comb,ax)
    matrix.set(xticklabels=[],yticklabels=[],xticks=[],yticks=[])
    #plt.title(str(csv[20:-8]), fontname='Charter')
    plt.tight_layout()
    
    # Save correlation figure per SID
    plt.savefig('./correlaton_output_'+str(csv[20:-8])+'.png',bbox_inches='tight',dpi=350,transparent=True)
    plt.close()

# Write and save file once all correlations have been finished
file.writelines(matrix_list)
file.close()
