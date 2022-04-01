from tkinter import *
from BranchAndBound import *
import time


#arranges the labels to match mat
def display(mat):
    for i in range(4):
        for j in range(4):
            Labels[int(mat[i][j])-1].grid(row=i+1,column=j)

#updates the display based on the command
def play(command):
    global path
    global total_steps
    global state
    global myLabel17

    if(path == None):
        return
    if(command == "first"):
        state = 1;
    elif(command == "back"):
        state = max(1,state-1)
    elif(command == "next"):
        state = min(total_steps,state+1)
    elif(command == "last"):
        state = total_steps
    newmat = getstate(mat,path,state-1)
    myLabel17["text"] = str(state) +" of " + str(total_steps)
    display(newmat)
    return

#solve the matrix
def run(myEntry):
    global mat
    global state
    global total_steps
    global path
    global statslabel

    text = myEntry.get()
    mat = read(text)

    arr = mergelist(mat)
    ListKurangI = KurangI(arr)
    Kurangiplusx = KurangIplusX(arr)
    if(isReachable(Kurangiplusx)):
        start_time = time.time()
        path,expanded = solve(mat)
        runtime = round((time.time() - start_time),5)

        total_steps = len(path)         #1 to total_steps, not 0 to total
        state = 1;
    else:
        expanded = 0
        runtime = 0
        state = 0 
        total_steps = 0

    stats1 ="KurangI = "+str(ListKurangI)+ "\nKurangI + X = " + str(Kurangiplusx) + "\nSolveable = "+str(isReachable(Kurangiplusx)) 
    stats2 = "\nExpanded Nodes: "+str(expanded)+"\nSearch Time: "+str(runtime) + " seconds"

    stats = stats1 + stats2
    display(mat)
    myLabel17["text"] = str(state) +" of " + str(total_steps)
    statslabel["text"] = stats


#gui interface    
def main():
    root = Tk()
    root.title("15-Puzzle")
    myEntry = Entry(root,text ="Enter Filename here",width=40)
    myEntry.grid(row=0,column=0,pady=10,columnspan = 3)
    
    myButton = Button(root,text = "Solve",command= lambda: run(myEntry))
    myButton.grid(row=0,column=3,pady=10)

    myLabel1 = Label(root,text ="01",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel2 = Label(root,text ="02",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel3 = Label(root,text ="03",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel4 = Label(root,text ="04",height=5,width=10,borderwidth=2, relief="solid",font=(30))

    myLabel5 = Label(root,text ="05",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel6 = Label(root,text ="06",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel7 = Label(root,text ="07",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel8 = Label(root,text ="08",height=5,width=10,borderwidth=2, relief="solid",font=(30))

    myLabel9 = Label(root,text ="09",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel10 = Label(root,text ="10",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel11 = Label(root,text ="11",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel12 = Label(root,text ="12",height=5,width=10,borderwidth=2, relief="solid",font=(30))

    myLabel13 = Label(root,text ="13",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel14 = Label(root,text ="14",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel15 = Label(root,text ="15",height=5,width=10,borderwidth=2, relief="solid",font=(30))
    myLabel16 = Label(root,text ="  ",height=5,width=10,borderwidth=2, relief="solid",font=(30))

    Button_first = Button(root,text="<<",command = lambda: play("first"))
    Button_back = Button(root,text="<",command = lambda: play("back"))
    Button_next = Button(root,text=">",command = lambda: play("next"))
    Button_last = Button(root,text=">>",command = lambda: play("last"))

    Button_first.grid(row=5,column=0,pady=10,padx=20)
    Button_back.grid(row=5,column=1,pady=10,padx=20)
    Button_next.grid(row=5,column=2,pady=10,padx=20)
    Button_last.grid(row=5,column=3,pady=10,padx=20)
    
    global path
    path = None
    state = 0;
    total_steps = 0;
    mat = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
    stats = ""

    global myLabel17
    myLabel17 = Label(root,text=str(state) +" of " + str(total_steps))
    myLabel17.grid(row=6,column=0,pady=10,columnspan=4)

    global Labels
    Labels = [myLabel1,myLabel2,myLabel3,myLabel4,myLabel5,myLabel6,myLabel7,myLabel8,myLabel9,myLabel10,myLabel11,myLabel12,myLabel13,myLabel14,myLabel15,myLabel16]
    
    
    display(mat)

    global statslabel
    statslabel = Label(root,text = stats)
    statslabel.grid(row = 7,column=0,pady=10,padx=20,columnspan=4)
    root.mainloop()


#starts the gui
if __name__ == "__main__":
    main()