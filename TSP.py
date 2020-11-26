#使用贪婪算法以及其启发式来解决商旅问题Traveling Salesman Problem (TSP)
#李兆钦
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
 
    def insertSmallest(self, p):        ###Smallest increase heuristic
        newNode = Node(p)               #输入node
        if self.head.next == None:
            self.head.next = newNode    #在链表中没有node时，直接放入第一个输入node
            self.tail = newNode
            self.distance = 0.0         #distance总里程
        else:
            next = self.head.next       #测试node1 = self.head; 测试node2 = self.head.next
            record = self.head      #记录要测试的两个node中的前一个
            dis = M**2+N**2         #给dis距离变量 设定理论最大距离
            dis_head = next.distanceTo(newNode)     #新输入node到head的距离
            dis_tail = self.tail.distanceTo(newNode)       #新输入node到tail的距离

            while next.next is not None:            #当链表下一位存在时，继续
               cal = next.distanceTo(newNode)+next.next.distanceTo(newNode)-next.distanceTo(next.next)      #定义 cal 为包含新输入node D 之后的距离变量 = Dis(测试node1 到 F)+Dis(F 到 测试node2)-Dis(两个测试node之间)
               if cal <= dis:
                   dis = cal        #如果新输入node加入到两个测试node之间之后的距离 小于 上一个测试的两个测试node之间的距离， 更新dis
                   record = next    #更新record所记录的测试node
               next = next.next     #测试下一对测试node

            mindis = min(dis,min(dis_head,dis_tail))        #当测试node之前或之后为空白时， 比较输入node到已知最短相对距离的一对测试node的距离 dis，然后再与dis_head 和 dis_tail分别对比，找出其中最小的值，存入变量mindis
            if mindis == dis_head:
                self.insert(self.head,newNode)          #当dis_head为最小时，将输入node放置于总链表head之前
            elif mindis == dis_tail:
                self.insert(self.tail,newNode)          #当dis_tail为最小时，将输入node放置于总链表tail之后
                self.tail = newNode                     #并且将链表tail指向新输入node
            else:
                self.insert(record,newNode)             #当dis最小时, 将输入node放置于record node之后
            self.distance += mindis                     #更新distance总里程 等于 mindis加 原始里程
     
    def insertNearest(self, p):             ###Nearest neighbor heuristic
        newNode = Node(p)                   #输入node
        if self.head.next == None:
            self.head.next = newNode        #在链表中没有node时，直接放入第一个输入node
            self.tail = newNode
            self.distance = 0.0             #distance总里程
        else:
            h,t = self.head.next,self.tail
            if h.distanceTo(newNode) <= t.distanceTo(newNode):      #如果输入node到head node的距离 <= 输入node到tail node的距离
                self.insert(self.head,newNode)              #将输入node放置于head node之后
                self.distance += h.distanceTo(newNode)      #更新distance总里程 等于 输入node到head node的距离 加 原始里程
            else:
                self.insert(self.tail,newNode)              #如果输入node到head node的距离 > 输入node到tail node的距离
                self.tail = newNode                         #将输入node放置于tail node之后
                self.distance += t.distanceTo(newNode)      #更新distance总里程 等于 输入node到tail node的距离 加 原始里程

    def draw(self, l, r):  #画图function
        xdata,ydata = [],[]
        n = self.head.next
        while n is not None:
            xdata.append(n.p.x)
            ydata.append(n.p.y)
            n = n.next
        l.set_xdata(xdata)
        l.set_ydata(ydata)
        r.set_xdata(xdata)
        r.set_ydata(ydata)

        plt.draw()
        plt.pause(0.2)

def read_coordinates(line):     #数据读取function
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

plt.show()
print(t.distance) 

         
