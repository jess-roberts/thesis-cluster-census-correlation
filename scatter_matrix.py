import seaborn as sns
import os
import glob
import matplotlib.pyplot as plt 
import pandas as pd

def findCSVs(csvDir):
    # criteria to find the geotiffs
    search_criteria = '*cen.csv'
    CSVs = os.path.join(csvDir, search_criteria)

    # taking all the files that match and globbing together
    all_CSVs = glob.glob(CSVs)
    print(len(all_CSVs),'.csv files found')
    return all_CSVs

CSVs = findCSVs('../../Census/MALAWI/')
print(CSVs)

sns.set_palette('husl') # colour pallate
for csv in CSVs:
    # set up figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    print('-- Correlating clusters against',csv[20:-8],'--')
    # read in data
    df1 = pd.read_csv(csv) # SID data
    df2 = pd.read_csv('../../Census/MALAWI/cluster_4_scatter.csv') # cluster data
    # define variables for matrix
    variables = list(df1.columns.values.tolist())
    clusters = list(df2.columns.values.tolist())
    # remove the 'regions' column
    only_clusters = clusters[:-1]
    # add dataframes together
    comb = pd.concat([df1, df2], axis=1)
    # plot dataframes
    matrix = sns.pairplot(comb,hue='District Type', y_vars=variables, kind='reg',plot_kws={'ci':None,'fit_reg':False},x_vars=only_clusters)
    
    # format matrix
    matrix.set(ylim=(100, None))
    matrix.set(xlim=(100, None))
    matrix.set(yscale="log")
    matrix.set(xscale="log")
    # export
    plt.savefig('./scatter_output_'+str(csv[20:-8])+'.png',dpi=400,bbox_inches='tight',transparent=False)
    print('Figure saved')
    plt.close()



