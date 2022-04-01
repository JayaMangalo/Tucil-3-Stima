from queue import PriorityQueue
import os
import copy

#Tree Nodes
#data is matrix of current state, path is the path to reach that state
#up,right,down,left are children 
class Node:
    def __init__(self,data,path):
        self.data = data
        self.path = path

    def __lt__(self, other):
        return True;
    
    def __le__(self, other):
        return True;   

#reads a file named text from ../test/ and returns inside as a 4x4 matrix of int, invalid inputs will cause the program to fail
def read(text):
    os.chdir("../test")
    f = open(text, "r")

    mat = []
    for x in f:
        arr = (x.strip("\n").split(" ")[:4])
        arr2 = []
        for x in arr:
            xInt = int(x)
            arr2.append(xInt)
        mat.append(arr2)
    f.close()
    return mat;

#turns the 4x4 matrix into an array of 16
def mergelist(mat):
    arr = []
    for l in mat:
        arr += l
    return arr

#returns a list consisting of Kurang(I)
def KurangI(arr):
    arr_KurangI = []
    for i in range(1,17):
        count = 0
        for j in range(1,i):
            if(arr.index(j) > arr.index(i)):
                count+=1
        arr_KurangI += [count]
    return arr_KurangI;

#totals and returns KurangI + X
def KurangIplusX(arr):
    count = sum(KurangI(arr))
    if(arr.index(16) in [1,3,4,6,9,11,12,14]):
        count+=1    
    return count

#returns true if count is event
def isReachable(count):
    if(count%2 == 0):
        return True
    return False

#returns the weight or g(x) of the matrix
def getweight(mat):
    count = 0;
    for i in range(4):
        for j in range(4):
            if(mat[i][j] != 4*i + j + 1):
                count+=1
    return count

#returns the weight or f(x) of the node
def getdepth(Current_Node):
    return 0.001*len(Current_Node.path)
    # return 0

#returns i,j coordinates of 16 in the 4x4 matrix
def Find16(mat):
    for i in range(4):
        for j in range(4):
            if(mat[i][j] == 16):
                return i,j

#turns the matrix into a string such as 01020304..... to be used as a key in a hash table
def matrixtokey(mat):
    key = ""
    for i in range(4):
        for j in range(4):
            key += "{:02d}".format(mat[i][j])
    return key

#checks and updates the hash table 
#gets the matrix mat, hashes it into a key
#if key not exist or key exist but weight (from parameter) is lower than key's value in hash table, returns true and insert/update hash table
#if key exist and key's value is lower than weight (from parameter), returns false
def CheckAndUpdateHashTable(mat,weight):        
    key = matrixtokey(mat)
    global dict
    if(key not in dict.keys()):
        dict[key] = weight
        return True
    else:
        # return False
        if(dict[key] < weight):
            return False
        else:
            dict[key] = weight
            return True
        
#create a new branch and enqueues it (if valid from checking hash table)
def AddBranch(mat,path,i,j,direction):
    newmat = copy.deepcopy(mat)
    path2 = copy.deepcopy(path)
    if(direction == "up" and path[-1] != "down" and i!=0):
        newmat[i][j],newmat[i-1][j] = newmat[i-1][j],newmat[i][j]
        newpath = path2 + ["up"]
        Weight = getdepth(Current_Node) + getweight(newmat)
        if(CheckAndUpdateHashTable(newmat,Weight)):
            NewNode = Node(newmat,newpath)
            q.put((Weight,NewNode))
    elif(direction == "down" and path[-1] != "up" and i!=3):
        newmat[i][j],newmat[i+1][j] = newmat[i+1][j],newmat[i][j]
        newpath = path2 + ["down"] 
        Weight = getdepth(Current_Node) + getweight(newmat)
        if(CheckAndUpdateHashTable(newmat,Weight)):
            NewNode = Node(newmat,newpath)
            q.put((Weight,NewNode))       
    elif(direction == "left" and path[-1] != "right" and j!=0):
        newmat[i][j],newmat[i][j-1] = newmat[i][j-1],newmat[i][j]
        newpath = path2 + ["left"]          
        Weight = getdepth(Current_Node) + getweight(newmat)
        if(CheckAndUpdateHashTable(newmat,Weight)):
            NewNode = Node(newmat,newpath)
            q.put((Weight,NewNode))
    elif(direction == "right" and path[-1] != "left" and j!=3):
        newmat[i][j],newmat[i][j+1] = newmat[i][j+1],newmat[i][j]
        newpath = path2 + ["right"]
        Weight = getdepth(Current_Node) + getweight(newmat)
        if(CheckAndUpdateHashTable(newmat,Weight)):
            NewNode = Node(newmat,newpath)
            q.put((Weight,NewNode))

    
#solves the matrix and returns path(list of "left","right",etc) and number of nodes expanded     
def solve(mat):
    global dict    
    global q 
    global Current_Node

    dict = {}     
    q = PriorityQueue()      
    Expanded_Nodes = 0  

    root = Node(mat,["none"])

    q.put((0, root))

    while not q.empty():
        Current_Node = q.get()[1]
        Expanded_Nodes +=1
        mat = Current_Node.data
        path = Current_Node.path

        print(mat)
        print(path)

        weight = getweight(mat)
        i,j = Find16(mat)

        if(weight == 0 ):
            break
        AddBranch(mat,path,i,j,"up")
        AddBranch(mat,path,i,j,"down")
        AddBranch(mat,path,i,j,"left")
        AddBranch(mat,path,i,j,"right")

    return Current_Node.path,Expanded_Nodes

#uses the base matrix and a list of paths to return a matrix in step number no_state
def getstate(mat,path,no_state):
    newmat = copy.deepcopy(mat)
    i,j = Find16(newmat)

    for no in range(no_state):
        if (path[no+1] == "up"): 
            newmat[i][j],newmat[i-1][j] = newmat[i-1][j],newmat[i][j]
            i = i-1
        elif(path[no+1] == "down"): 
            newmat[i][j],newmat[i+1][j] = newmat[i+1][j],newmat[i][j]
            i = i+1
        elif(path[no+1] == "left"): 
            newmat[i][j],newmat[i][j-1] = newmat[i][j-1],newmat[i][j]
            j = j-1
        elif(path[no+1] == "right"): 
            newmat[i][j],newmat[i][j+1] = newmat[i][j+1],newmat[i][j]
            j = j+1

    return newmat

#main for testing
if __name__ == "__main__": 
    mat = read("valid2.txt")
    path, expandednodes = solve(mat)
