# -*- coding: utf-8 -*-


import math as m
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.patches import Circle
import imageio
def rown(A,B,C,D,E): #A=0 => B=0, A>=0, E>=0
  T=[]
  if (A!=0):
    a=-3*B**2/(8*A**2)+C/A
    b=B**3/(8*A**3)-B*C/(2*A**2)+D/A
    c=-3*B**4/(256*A**4)+C*B**2/(16*A**3)-B*D/(4*A**2)+E/A
    if (b==0 and a**2-4*c>0):
      if (-a+m.sqrt(a**2-4*c)>=0):
        T.append(-B/(4*A)+m.sqrt((-a+m.sqrt(a**2-4*c))/2))
        T.append(-B/(4*A)-m.sqrt((-a+m.sqrt(a**2-4*c))/2))
        if (-a-m.sqrt(a**2-4*c)>=0):
          T.append(k=-B/(4*A)+m.sqrt((-a-m.sqrt(a**2-4*c))/2))
          T.append(-B/(4*A)-m.sqrt((-a-m.sqrt(a**2-4*c))/2))
    if (b!=0):
      p=-a**2/12-c
      if (p>=0):
        q=-a**3/108+a*c/3-b**2/8
        w=(-q/2+m.sqrt(q**2/4+p**3/27))**(1/3)
        y=a/6+w-p/(3*w)
        if (2*y-a>0):
          if (-2*y-a+2*b/m.sqrt(2*y-a)>=0):
            T.append((-m.sqrt(2*y-a)+m.sqrt(-2*y-a+2*b/m.sqrt(2*y-a)))/2)
            T.append((-m.sqrt(2*y-a)-m.sqrt(-2*y-a+2*b/m.sqrt(2*y-a)))/2)
          if (-2*y-a-2*b/m.sqrt(2*y-a)>=0):
            T.append((-m.sqrt(2*y-a)+m.sqrt(-2*y-a-2*b/m.sqrt(2*y-a)))/2)
            T.append((-m.sqrt(2*y-a)-m.sqrt(-2*y-a-2*b/m.sqrt(2*y-a)))/2)

  if (A==0):
    if (C!=0):
      delta=D**2-4*C*E
      if (delta>=0):
        T.append((-D-m.sqrt(delta))/(2*C))
        T.append((-D+m.sqrt(delta))/(2*C))
      
  return T

def poch(A,B,C,D,E,t):
  return 4*A*t**3+3*B*t**2+2*C*t+D

class bila:
  def __init__(self,R,V,d,gmu):
    self.R=R
    self.V=V
    self.d=d
    self.time_bandy=[]
    self.time_bile=[]
    self.time_z=m.sqrt(self.V[0]**2+self.V[1]**2)/gmu

    if (m.sqrt(self.V[0]**2+self.V[1]**2)!=0):
      self.wer=[self.V[0]/m.sqrt(self.V[0]**2+self.V[1]**2),self.V[1]/m.sqrt(self.V[0]**2+self.V[1]**2)]
    else:
      self.wer=[0,0]

  def re_wer(self):
    if (m.sqrt(self.V[0]**2+self.V[1]**2)!=0):
      self.wer=[self.V[0]/m.sqrt(self.V[0]**2+self.V[1]**2),self.V[1]/m.sqrt(self.V[0]**2+self.V[1]**2)]
    else:
      self.wer=[0,0]

  def time(b_1, b_2, a):
    A=a**2*((b_1.wer[0]-b_2.wer[0])**2+(b_1.wer[1]-b_2.wer[1])**2)
    B=-a*((b_1.wer[0]-b_2.wer[0])*(b_1.V[0]-b_2.V[0])+(b_1.wer[1]-b_2.wer[1])*(b_1.V[1]-b_2.V[1]))
    C=((b_1.V[0]-b_2.V[0])**2+(b_1.V[1]-b_2.V[1])**2)-a*((b_1.R[0]-b_2.R[0])*(b_1.wer[0]-b_2.wer[0])+(b_1.R[1]-b_2.R[1])*(b_1.wer[1]-b_2.wer[1]))
    D=2*((b_1.R[0]-b_2.R[0])*(b_1.V[0]-b_2.V[0])+(b_1.R[1]-b_2.R[1])*(b_1.V[1]-b_2.V[1]))
    E=(b_1.R[0]-b_2.R[0])**2+(b_1.R[1]-b_2.R[1])**2-(b_1.d+b_2.d)**2
    T=rown(A,B,C,D,E)

    t=[]

    for i in T:
      if (i>=0 and i<=min(b_1.time_z,b_2.time_z)):
        t.append[i]

    if (len(t)==0):
      return m.inf
    else:
      t=sorted(t)
      for i in t:
        if (i>=0 and i<=min(b_1.time_z,b_2.time_z)):
          if (poch(A,B,C,D,E,i)<0):
            return i
            break
      return m.inf

  def t_bandy(self,a,b,gmu):
    i=[]
    if self.V[0]**2+2*gmu*self.wer[0]*(self.R[0]-a+self.d)>0 and self.V[0]>0:
      i.append(m.inf)
      i.append((self.V[0]-m.sqrt(self.V[0]**2+2*gmu*self.wer[0]*(self.R[0]-a+self.d)))/(gmu*self.wer[0]))
    elif self.V[0]**2+2*gmu*self.wer[0]*(self.R[0]-self.d)>0 and self.V[0]<0:
      i.append((self.V[0]+m.sqrt(self.V[0]**2+2*gmu*self.wer[0]*(self.R[0]-self.d)))/(gmu*self.wer[0]))
      i.append(m.inf)
    else:
      i.append(m.inf)
      i.append(m.inf)

    
    if self.V[1]**2+2*gmu*self.wer[1]*(self.R[1]-b+self.d)>0 and self.V[1]>0:
      i.append(m.inf)
      i.append((self.V[1]-m.sqrt(self.V[1]**2+2*gmu*self.wer[1]*(self.R[1]-b+self.d)))/(gmu*self.wer[1]))
    elif self.V[1]**2+2*gmu*self.wer[1]*(self.R[1]-self.d)>0 and self.V[1]<0:
      i.append((self.V[1]+m.sqrt(self.V[1]**2+2*gmu*self.wer[1]*(self.R[1]-self.d)))/(gmu*self.wer[1]))
      i.append(m.inf)
    else:
      i.append(m.inf)
      i.append(m.inf)

    self.time_bandy=i
  
  def t_bile(self,lista,gmu):
    tab=[]

    for i in lista:
      tab.append(self.time(i,gmu))
    
    self.time_bile=tab

  def move(self, t, gmu):
    self.R[0]+=t*self.V[0]-gmu*self.wer[0]*t**2/2
    self.R[1]+=t*self.V[1]-gmu*self.wer[1]*t**2/2

    self.V[0]-=gmu*self.wer[0]*t
    self.V[1]-=gmu*self.wer[1]*t

    for i in range(len(self.time_bile)):
      self.time_bile[i]-=t
    for i in range(4):
      self.time_bandy[i]-=t
    self.time_z-=t

    self.re_wer()

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
    if (self.time_z<t):
      t=self.time_z
      b="zatrzymanie"
      j=-1
    return t,b,j

class stol:
  def __init__(self, lista, a, b, gmu):
    self.lista=lista
    self.a=a
    self.b=b
    self.gmu=gmu

  def inicjacja(self):
    for i in self.lista:
      i.t_bile(self.lista,self.gmu)
      i.t_bandy(self.a,self.b,self.gmu)
  
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
      i.move(T,self.gmu)

    if (B=="zatrzymanie"):
      self.lista[k].V[0]=0
      self.lista[k].V[1]=0
      self.lista[k].wer=[0,0]
      self.lista[k].t_bandy(self.a,self.b,self.gmu)
      self.lista[k].t_bile(self.lista,self.gmu)

      for i in range(len(self.lista)):
        if (i!=k):
          self.lista[i].time_bile[k]=self.lista[k].time_bile[i]

    if (B=="banda"):
      if (J==0 or J==1):
        self.lista[k].V[0]=-self.lista[k].V[0]
      if (J==2 or J==3):
         self.lista[k].V[1]=-self.lista[k].V[1]
      self.lista[k].re_wer()
      self.lista[k].t_bandy(self.a,self.b,self.gmu)
      self.lista[k].t_bile(self.lista,self.gmu)

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

      self.lista[k].re_wer()
      self.lista[J].re_wer()

      self.lista[k].t_bandy(self.a,self.b,self.gmu)
      self.lista[k].t_bile(self.lista,self.gmu)
      self.lista[J].t_bandy(self.a,self.b,self.gmu)
      self.lista[J].t_bile(self.lista,self.gmu)

      for i in range(len(self.lista)):
        if (i!=k and i!=J):
          self.lista[i].time_bile[k]=self.lista[k].time_bile[i]
          self.lista[i].time_bile[J]=self.lista[J].time_bile[i]
          
bil1=bila([5.,5.],[1,1],1.,0.1)
bil2=bila([7.,5.],[-5.,0.],1.,0.1)
kule=stol([bil2,bil1],10,16,0.1)
kule.inicjacja()


  
#symulacja
def symulacja(lista, a, b, klatki):
  

  s=stol(lista,a,b,0.1)
  s.inicjacja()
  fig = plt.figure()
  ax = fig.add_subplot(111, aspect='equal')
  ax.set_xlim([0,a])
  ax.set_ylim([0,b])
  for bila in lista:
     ax.add_artist(Circle(xy=(bila.R[0], bila.R[1]), radius=bila.d))
  fig.savefig(str(0)+'.png')
  fig.clf()
  for i in range (1,klatki):
    s.ref()
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim([0,a])
    ax.set_ylim([0,b])
    for bila in lista:
     ax.add_artist(Circle(xy=(bila.R[0], bila.R[1]), radius=bila.d))
    fig.savefig(str(i)+'.png')
    fig.clf()
klatki=10
symulacja([bil1,bil2],16,16,klatki)
frames=[]
for i in range(0,klatki):
  image = imageio.v2.imread(str(i)+'.png')
  frames.append(image)
imageio.mimsave('example.gif', frames, duration=20)         