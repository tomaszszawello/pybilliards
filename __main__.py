import math as m
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

#klasa bila
class bila:
  def __init__(self,R,V,d,m):
    self.R=R
    self.V=V
    self.d=d
    self.m=m
    self.time_bandy=[]
    self.time_bile=[]

  def time(self,i):
      a=(i.V[0]-self.V[0])**2+(i.V[1]-self.V[1])**2
      b=2*((i.V[0]-self.V[0])*(i.R[0]-self.R[0])+(i.V[1]-self.V[1])*(i.R[1]-self.R[1]))
      c=(i.R[0]-self.R[0])**2+(i.R[1]-self.R[1])**2-(self.d+i.d)**2
      delta=b**2-4*a*c

      if (delta<=0):
        return m.inf
        
      if (delta>0):
        if ((-b+m.sqrt(delta))/(2*a)<=0):
          return m.inf
        if ((-b-m.sqrt(delta))/(2*a)>=0):
          return (-b-m.sqrt(delta))/(2*a)
        if ((-b+m.sqrt(delta))/(2*a)>0) and ((-b-m.sqrt(delta))/(2*a)<0):
          print("odległość miedzy bilami jest mniejsza niż suma ich promieni")

  def t_bandy(self,a,b):
    i=[]

    if self.V[0]>0:
      i.append(m.inf)
      i.append((a-self.R[0]-self.d)/self.V[0])
    if self.V[0]==0:
      i.append(m.inf)
      i.append(m.inf)
    if self.V[0]<0:
      i.append(-(self.R[0]-self.d)/self.V[0])
      i.append(m.inf)

    if self.V[1]>0:
      i.append(m.inf)
      i.append((b-self.R[1]-self.d)/self.V[1])
    if self.V[1]==0:
      i.append(m.inf)
      i.append(m.inf)
    if self.V[1]<0:
      i.append(-(self.R[1]-self.d)/self.V[1])
      i.append(m.inf)

    self.time_bandy=i
  
  def t_bile(self,lista):
    tab=[]

    for i in lista:
      tab.append(self.time(i))
    
    self.time_bile=tab

  def move(self, t):
    self.R[0]+=t*self.V[0]
    self.R[1]+=t*self.V[1]
    for i in range(len(self.time_bile)):
      self.time_bile[i]-=t
    for i in range(4):
      self.time_bandy[i]-=t

  def t_least(self):
    t=m.inf
    b="banda"
    for i in range(len(self.time_bandy)):
      if self.time_bandy[i]<t:
        t=self.time_bandy[i]
        j=i
    for i in range(len(self.time_bile)):
      if self.time_bile[i]<t:
        t=self.time_bile[i]
        b="bila"
        j=i
    return t,b,j

#klasa stol
class stol:
  def __init__(self, lista, a, b):
    self.lista=lista
    self.a=a
    self.b=b

  def inicjacja(self):
    for i in self.lista:
      i.t_bile(self.lista)
      i.t_bandy(self.a,self.b)
  
  def ref(self):
    T=m.inf
    for i in range(len(self.lista)):
      t,b,j=self.lista[i].t_least()
      if (T>t):
        T=t
        B=b
        J=j
        k=i

    for i in self.lista:
      i.move(T)

    if (B=="banda"):
      if (J==0 or J==1):
        self.lista[k].V[0]=-self.lista[k].V[0]
      if (J==2 or J==3):
         self.lista[k].V[1]=-self.lista[k].V[1]
      self.lista[k].t_bandy(self.a,self.b)
      self.lista[k].t_bile(self.lista)

      for i in range(len(self.lista)):
        if (i!=k):
          self.lista[i].time_bile[k]=self.lista[k].time_bile[i]

    if (B=="bila"):
      V1=self.lista[k].V
      V2=self.lista[J].V
      R1=self.lista[k].R
      R2=self.lista[J].R
      a=2*((V1[0]-V2[0])*(R1[0]-R2[0])+(V1[1]-V2[1])*(R1[1]-R2[1]))/((self.lista[k].m+self.lista[J].m)*((R1[0]-R2[0])**2+(R1[1]-R2[1])**2))
      self.lista[k].V[0]-=a*self.lista[J].m*(R1[0]-R2[0])
      self.lista[k].V[1]-=a*self.lista[J].m*(R1[1]-R2[1])
      self.lista[J].V[0]-=a*self.lista[k].m*(R2[0]-R1[0])
      self.lista[J].V[1]-=a*self.lista[k].m*(R2[1]-R1[1])

      self.lista[k].t_bandy(self.a,self.b)
      self.lista[k].t_bile(self.lista)
      self.lista[J].t_bandy(self.a,self.b)
      self.lista[J].t_bile(self.lista)

      for i in range(len(self.lista)):
        if (i!=k and i!=J):
          self.lista[i].time_bile[k]=self.lista[k].time_bile[i]
          self.lista[i].time_bile[J]=self.lista[J].time_bile[i]

#test
a, b = (10, 16)

bil1=bila([5,5],[1,1],1,1)
bil2=bila([7,5],[-1,0],1,1)
kule=stol([bil1,bil2],a,b)

kule.inicjacja()
'''
for i in range(10):
  kule.ref()
  for i in kule.lista:
    print(i.R, i.V)
  print(" ")
'''  
#symulacja
def symulacja(lista, a, b, T):
  s=stol(lista,a,b)
  s.inicjacja()

  fig, ax = plt.subplots()
  ax.set_xlim([0,a])
  ax.set_ylim([0,b])
  ax.set_aspect('equal')
  ax.set_xticks([])
  ax.set_yticks([])
  
  patches=[]
  for i in range(len(lista)):
    patches.append(plt.Circle((lista[i].R[0],lista[i].R[1]),lista[i].d))
  for i in range(len(lista)):
    ax.add_patch(patches[i])

  def animate(i):
    s.ref()
    for i in range(len(lista)):
      patches[i].center=(lista[i].R[0],lista[i].R[1])
    return patches

  ani = FuncAnimation(fig, animate, frames=int(T*60), interval=10, blit=True)
  plt.show()
  ani.save('bilard.gif', writer = "pillow", fps=10 )
 
symulacja([bil1, bil2],a,b,10)
