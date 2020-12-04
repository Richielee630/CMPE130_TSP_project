#Useing Greedy Algorithm Heuristic to solve Traveling Salesman Problem (TSP)
#Zhaoqin Li, Chenghan Bian, Zuofan Zhang
import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import time


class Point:
    # data structure for each point
    def __init__(self,x,y):
        self.x,self.y = x,y

    def distanceTo(self,p):
        # Point member function to calculate the Euclidean distance between points
        return math.sqrt((self.x-p.x)**2+(self.y-p.y)**2)


class Node:
    # Linked List Node wraps point
    def __init__(self,p):
        self.p = p 
        self.next = None

    def distanceTo(self,n):
        # Node member function to calculate the Euclidean distance between Nodes
        return self.p.distanceTo(n.p)

class Tour:             #create a Tour data type
    def __init__(self):
        # Nodes are sequentially linked by a linked list, head and tail are the head and tail of the linked list
        self.head = Node(None)
        self.tail = self.head
        self.distance = 0.0
   
    def insert(self,parent,next):
        # help function to insert Node next after parent
        next.next = parent.next
        parent.next = next

    def insertSmallest(self, p):  ###Smallest increase heuristic
        newNode = Node(p)  # create newNode
        if self.head.next == None:
            self.head.next = newNode  # Insert the first node if there's no node in linked list
            self.tail = newNode
            self.distance = 0.0  # total distance
        else:
            next = self.head.next  # test node1 = self.head; test node2 = self.head.next
            record = self.head  # recode first node
            dis = M ** 2 + N ** 2  # set max dis value
            dis_head = next.distanceTo(newNode)  # distance from newNode to head
            dis_tail = self.tail.distanceTo(newNode)  # distance from newNode to tail

            while next.next is not None:  # continue when next node exists
                cal = next.distanceTo(newNode) + next.next.distanceTo(newNode) - next.distanceTo(
                    next.next)  # define cal as distance after include newNode D = Dis(test node1 to F)+Dis(F to test node2)-Dis(between two test nodes)
                if cal <= dis:
                    dis = cal  # update dis if distance from newNode to test node is smaller than last test
                    record = next  # update recode next ndoe
                next = next.next  # test next node

            mindis = min(dis, min(dis_head,
                                  dis_tail))  # When the test node is empty before or after, compare dis with the smallest value between dis_head and dis_tail to find the smallest value and store it in mindis
            if mindis == dis_head:
                self.insert(self.head, newNode)  # put newNode after head node if dis_head is the smallest
            elif mindis == dis_tail:
                self.insert(self.tail, newNode)  # put newNode after tail node if dis_tail is the smallest
                self.tail = newNode  # newNode = tail
            else:
                self.insert(record, newNode)  # put newNode after record node if dis is the smallest
            self.distance += mindis  # update total distance = mindis + original distance

    def insertNearest(self, p):  ###Nearest neighbor heuristic
        newNode = Node(p)  # create newNode
        if self.head.next == None:
            self.head.next = newNode  # Insert the first node if there's no node in linked list
            self.tail = newNode
            self.distance = 0.0  # total distance
        else:
            h, t = self.head.next, self.tail
            if h.distanceTo(newNode) <= t.distanceTo(
                    newNode):  # if distance between newNode and head <= distance between newNode and tail
                self.insert(self.head, newNode)  # put newNode after head node
                self.distance += h.distanceTo(
                    newNode)  # update total distance = distance from newNode to tail + original distance
            else:
                self.insert(self.tail,
                            newNode)  # if distance between newNode and head > distance between newNode and tail
                self.tail = newNode  # put newNode after tail node
                self.distance += t.distanceTo(
                    newNode)  # update total distance = distance from newNode to tail + original distance

    def loop(self):
        if self.head.next is not None:
            self.distance += self.head.next.distanceTo(self.tail)

    def draw(self, l, r):  #draw function
        xdata,ydata = [],[]
        n = self.head.next
        while n is not None:
            xdata.append(n.p.x)
            ydata.append(n.p.y)
            n = n.next
        xdata.append(xdata[0])
        ydata.append(ydata[0])
        l.set_xdata(xdata)
        l.set_ydata(ydata)
        #r.set_xdata(xdata)
        #r.set_ydata(ydata)

        plt.draw()
        plt.pause(0.2)

def read_coordinates(line):     #coordinates reading function
    line = [float(c) for c in line.split(' ')]
    p = Point(line[0],line[1])
    return  p

t = Tour()
f = open(sys.argv[1],"r")
first = f.readline().split(' ')
M,N = int(first[0]),int(first[1])
line = f.readline()


axes = plt.gca()
axes.set_xlim(0,M)
axes.set_ylim(0,N)
l, = axes.plot([],[],'r-')
r, = axes.plot([],[],'bo')

while line:
    p = read_coordinates(line)
    #t.insertNearest(p)
    t.insertSmallest(p)
    t.draw(l,r)
    line = f.readline()
    time.sleep(0.1)
t.loop()

plt.show()
print(t.distance) 

         
