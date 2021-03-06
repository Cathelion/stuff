#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:11:58 2021

@author: flo


My implementation of the Hungarian Algorithm
Probably super slow and not optimized but working so far
I am using some fishy way to get the arrangements, that could be improved, I guess.

using : 
http://www.universalteacherpublications.com/univ/ebooks/or/Ch6/hungalgo.htm
https://stackoverflow.com/questions/4527299/hungarian-algorithm-assign-systematically

"""
import numpy as np

# main algorithm
# takes in a matrix and returns tuple (i,j) of pairing
def hungarian(inputM):
    M = np.copy(inputM)   # need copy to not change original
    n = np.shape(M)[0]
    
    # Step 1 and 2: subtract smallest element from each row and then each column
    for r in range(n):
        M[r,:] = M[r,:] - np.min(M[r,:])
    for c in range(n):
        M[:,c] = M[:,c] - np.min(M[:,c])
    
    for k in range(0,5):
        # Step 3: assign cells
        zero_dict = makeZeroDict(M)
        
        # Step 4: check if already solution is possible
        numAssCells, mRows, mCols = findLines(M, zero_dict)
        if numAssCells==n:
            print("Done")
            print(inputM,"\n",M)
            res = findArangement(M)   # picking out a possible arrangement
            print("Arrangement", res)
            return res
        # if not enough lines, change acc. to algorithm
        else:
            changeM(M, mRows, mCols)
    else:
        print("could not update and repeat properly")


"""Idea: search for zero that is alone in its row or column.
Then it has to be in the assignment. Add that index into list.
Then set all zeros in the corresponding row/column to zero. 
That is like chanceling out row and column.
Now continue for next zero.
If no lonely zero can be found, just pick the first one, there are 
multiple possibilities."""
def findArangement(inputM):
    M = np.sign(np.copy(inputM))
    indexList = []
    n = np.shape(M)[0]
    
    for k in range(n):   # need to find n zeros
        flag = False
        # search for lonely zero
        for i in range(n):
            if flag: break
            for j in range(n):
                if flag: break
                
                if M[i,j]==0:
                    M[i,j]=1   # makes product possible
                    if (np.prod(M[:,j]==1) or np.prod(M[i,:])==1):
                        indexList.append((i,j))
                        M[:,j]=np.ones(n)
                        M[i,:]=np.ones(n)
                        flag = True
                    else:
                        M[i,j]=0   # change back to original
        
        # if no lonely zero, take first zero in matrix
        if not flag: 
            # find first zero
            for i in range(n):
                if flag: break
                for j in range(n):
                    if flag: break
                    if M[i,j]==0:
                        indexList.append((i,j))
                        M[:,j]=np.ones(n)
                        M[i,:]=np.ones(n)
                        flag=True
    return indexList
    

# assigns and crosses out zeros
def makeZeroDict(inputM):
    n = np.shape(inputM)[0]
    zero_dict = {}
    
    # fill zero dictionary
    for i in range(n):
        for j in range(n):
            if inputM[i,j]==0:
                if (i,j) not in zero_dict:   # new zero
                    zero_dict[(i,j)] = 1   # use one for assigned cell
                else:   # skip over eliminated zeros
                    continue
                
                # eliminating zeros in row i and  column j
                for k in range(n):
                    if k!=i and  inputM[k,j]==0:   # zero in same row
                        zero_dict[(k,j)] = -1   # -1 for eliminated zero
                    if k!= j and inputM[i,k]==0:   # zero in same column
                        zero_dict[(i,k)] = -1
                    
    return zero_dict
    
    
# starting step, mark all rows wo. assignments
def markNoAssRows(zero_dict, n):
    rows = np.zeros(n)
    for i in range(n):
        flag = 1
        for j in range(n):
            if (i,j) in zero_dict and zero_dict[(i,j)]==1:
                flag = 0
                break
        rows[i] = flag
    return rows

# marking columns, which have zeros in the marked rows 
def markCols(zero_dict,rows,cols,n):
    colsC = np.copy(cols)
    for r in np.argwhere(rows).flatten():
        for j in range(n):
            if (r,j) in zero_dict:
                colsC[j]=1
    return colsC
            
# marking rows, which have assigned zeros in the marked columns
def markRows(zero_dict,rows,cols,n):
    rowsC = np.copy(rows)
    for c in np.argwhere(cols).flatten():
        for i in range(n):
            if (i,c) in zero_dict and zero_dict[(i,c)]==1:
                rowsC[i]=1
    return rowsC
    

def changeM(inputM, mRows,mCols):
    n = np.shape(inputM)[0]
    
    # get indicies of marked rows and cols
    unmarkedCols = np.where(np.abs(np.ones(n)-mCols).astype(int)==1)[0]
    unmarkedRows = np.where(np.abs(np.ones(n)-mRows).astype(int)==1)[0]
    tmpCols = np.where(mCols.astype(int)==1)[0]
    tmpRows = np.where(mRows.astype(int)==1)[0]
    
    # special cases for empty list, otherwise slicing does not work
    colIndex,rowIndex = 0,0
    if len(unmarkedCols)!=0:
        colIndex = unmarkedCols
    if len(tmpRows)!=0:
        rowIndex = tmpRows
        
    # clever slicing to use built-in numpyfcn
    minimum = np.min(inputM[rowIndex,:][:,colIndex])
    
    # subtract from remaining elements
    for rm in tmpRows:
        for cu in unmarkedCols:
            inputM[rm,cu] -= minimum 
    
    # add to elements in line intersection
    for ru in unmarkedRows:
        for cm in tmpCols:
            inputM[ru,cm] +=minimum
    
def findLines(inputM,zero_dict):
    n= np.shape(inputM)[0]
    oldRows = markNoAssRows(zero_dict, n)   # starting value
    oldCols = np.zeros(n)   # some random staring value
    
    # mark continuosly new rows and cols, stop when no more change
    for k in range(2*n):
        newCols = markCols(zero_dict, oldRows, oldCols, n)
        newRows = markRows(zero_dict, oldRows, oldCols, n)
        if (newCols==oldCols).all() and (newRows==oldRows).all():
            return sum(newCols)+(n-sum(newRows)), newRows, newCols
        else:
            oldRows=newRows
            oldCols=newCols
    else:
        print("could not find zero-lines")
    

a = np.array([6,1,2,3,5,4])

A = np.array([[1,1,1,0],[0,5,0,2],[2,0,4,0],[3,4,0,3]])
B = np.array([[108,125,150],[150,135,175],[122,148,250]])
C =  np.array([[0,17,2],[15,0,0],[0,24,86]])
D = np.array([[0,1,0],[1,0,1],[0,1,0]])
E = np.array([[10,19,8,15,19],[10,18,7,17,19],[13,16,9,14,19],[12,19,8,18,19],[14,17,10,19,19]])
hungarian(E)
