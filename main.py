from datetime import datetime

class Process:

    def __init__(self, myIndex):
        # spot in the PCB array
        self.myIndex = int(myIndex)
        # Parent Process
        self.ParentProcess = None
        # pointer to a linkedList of the rest of this processes' Children
        self.firstChild = None
        self.YSib = None
        self.OSib = None

    def setFirstChild(self, Child):
        self.firstChild = Child

    def getFirstChild(self):
        return self.firstChild

    def setMyIndex(self, num):
        self.myIndex = int(num)

    def getMyIndex(self):
        return self.myIndex

    def setParentProcess(self, p):
        self.ParentProcess = p

    def getParentProcess(self):
        return self.ParentProcess

    def setOldSib(self, s):
        self.OSib = s

    def getOldSib(self):
        return self.OSib

    def setYoungSib(self, s):
        self.YSib = s

    def getYoungSib(self):
        return self.YSib

    def checkForChild(self):
        if self.firstChild is None:
            return False
        else:
            return True


def create(parent, PCB):  # p is a process, PCB is which PCB you want to add a process to

    # makes a new child & puts it in the next available spot
    childProcess = Process(len(PCB) - 1)
    PCB.append(childProcess)

    # sets the child process' parent
    childProcess.setParentProcess(parent)

    # sets the child's index to where you placed the Child
    childProcess.setMyIndex(len(PCB) - 1)

    # check if the parent has previous children
    check = parent.checkForChild()

    # if the parent does have children, go through the linked list of child processes and add one to the end
    if check is True:
        currProcess = parent.getFirstChild()
        while currProcess.getYoungSib() is not None:
            currProcess = currProcess.getYoungSib()
        currProcess.setYoungSib(childProcess)
        childProcess.setOldSib(currProcess)

    # if the parent does not have children, create a pointer to anew linkedList with the Child as the start
    else:
        parent.setFirstChild(childProcess)

    print("Process [", parent.getMyIndex(), "] created Process[", childProcess.getMyIndex(), "]")
    # return the updated PCB
    return PCB


def destroy(theProcess, original, pcb):
    # does the process have children?
    if theProcess is not None:
        child = theProcess.getFirstChild()
        # yes, go through each child and their sibs
        if child is not None:
            destroy(child, original, pcb)

        if theProcess != original:
            sib = theProcess.getYoungSib()
            while sib is not None:
                destroy(sib, original, pcb)
                sib = sib.getYoungSib()

        older = theProcess.getOldSib()
        younger = theProcess.getYoungSib()
        if older is not None and younger is not None:
            older.setYoungSib(younger)
            younger.setOldSib(older)
        elif younger is not None:
            parent = theProcess.getParentProcess()
            if parent is not None:
                parent.setFirstChild(younger)
            younger.setOldSib(None)
        elif older is not None:
            older.setYoungSib(None)

        print("The PCB at index:", theProcess.getMyIndex(), "has been destroyed")
        pcb.remove(theProcess)
        theProcess.getMyIndex = None
        theProcess.ParentProcess = None
        theProcess.OSib = None
        theProcess.YSib = None
    return PCB


def display(pcb):
    displayPCB = []
    for x in range(len(pcb)):
        y = pcb[x]
        a = y.getMyIndex()
        displayPCB.append(a)
    print(displayPCB)


def initializeThePCB():
    PCB1 = []
    initialProcess = Process(0)
    initialProcess.setMyIndex(0)
    PCB1.append(initialProcess)
    return PCB1


begin_time = datetime.now()

for x in range(100):
    PCB = initializeThePCB()
    PCB = create(PCB[0], PCB)
    PCB = create(PCB[0], PCB)
    PCB = create(PCB[0], PCB)
    PCB = create(PCB[2], PCB)
    print("Updated PCB: ")
    display(PCB)
    destroy(PCB[0], PCB[0], PCB)
    print("Updated PCB: ")
    display(PCB)
    print("************************************")  # so you can differentiate each round

print(datetime.now() - begin_time)
