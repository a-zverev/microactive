#! /usr/bin/env python

from sys import argv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu as man
import biom
import pandas
import h5py
import re

inp = argv[1]
ID = argv[2]

def del_singltones(inp):
    otu_table = biom.load_table(inp)
    a = [i for i in otu_table.iter_data(axis="observation")]
    b = [i for i in a if sum(i)>5]

def ratiometr(ftable, ilist):  
    left = [i for i in ftable.columns.values if i.startswith(ilist[0])]
    right = [i for i in ftable.columns.values if i.startswith(ilist[1])]
    tableleft = ftable.groupby(left)
    tableright = ftable.groupby(right)
    sum1 = tableleft.sum().sum().sum()
    sum2 = tableright.sum().sum().sum()
    rtableleft = ftable[left].apply(lambda row: row/sum1)
    rtableright = ftable[right].apply(lambda row: row/sum2)
    table = pandas.concat([rtableleft, rtableright], axis=1, join='inner')
    return left, right, table

def ratfilt(left, right, table):
    table1s = table[left].apply(lambda row: sum(row)/len(row),axis=1)
    table2s = table[right].apply(lambda row: sum(row)/len(row),axis=1)
    tables = pandas.concat([table1s, table2s], axis=1, join='inner')
    tables_d = tables[0 and 1] >=0.005
    return tables_d


def man_y(rttable,tf_table, left, right):
    ftable = rttable.loc[tf_table]
    print(rttable)
    print(ftable)
    def m(row,left,right):
        x = man((row[left], row[right]))[1]
        return x
    rttable['pvalue'] = rttable.apply(lambda x: m(x ,left,right),axis=1 )
    print(rttable)
    return man_table


  

def filter_otu(inp, idfs):
    '''
    Filter biom table by sample Id from mapping txt file.
    '''
    otu_table = biom.load_table(inp)
    al_l =[line.rstrip() for line in idfs.split("\t")]
    al_ll = []
    for a in al_l:
        if re.search(r'\D\Z',a):
            sample_list = otu_table.ids(axis='sample')
            for i in sample_list: 
                if i.startswith(a):
                    al_ll.append(i)
        else:
            al_ll.append(a)
    
    new_table = otu_table.filter(al_ll,axis='sample', inplace=False)
    return new_table

def main(inp, ID):
    # del_singltones(inp)
    with open(ID, "r") as idfile:
        idf = idfile.readlines()
        for i in idf:
            nonn_line = i.rstrip()
            ilist = nonn_line.split("\t")
            print(ilist)
            ftable = filter_otu(inp, i)
            np.float64 == np.dtype(float).type
            datatable = ftable.to_dataframe()
            left, right, rttable = ratiometr(datatable, ilist)
            tf_table = ratfilt(left, right, rttable)
            man_table = man_y(rttable, tf_table, left, right)


if __name__ == "__main__":
    main(inp, ID)