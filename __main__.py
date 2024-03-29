# -*- coding: utf-8 -*-
"""bile.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-F1kjSQvWMxYlQ8qAJ9qvPy_tVt_sziH
"""

#kod do testów

import matplotlib.pyplot as plt
import math as m
import numpy as np

def rown(A,B,C,D,E): #A=0 => B=0, A>=0, E>=0; funkcja zwraca w tabeli rzeczywiste pierwiastki wielomianu czwartego stopnia
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
          T.append(-B/(4*A)+m.sqrt((-a-m.sqrt(a**2-4*c))/2))
          T.append(-B/(4*A)-m.sqrt((-a-m.sqrt(a**2-4*c))/2))
    if (b!=0):
      p=-a**2/12-c
      q=-a**3/108+a*c/3-b**2/8
      if (q**2/4+p**3/27>=0):
        w=(-q/2+m.sqrt(q**2/4+p**3/27))**(1/3)
        y=a/6+w-p/(3*w)
        if (2*y-a>0):
          if (-2*y-a+2*b/m.sqrt(2*y-a)>=0):
            T.append((-m.sqrt(2*y-a)+m.sqrt(-2*y-a+2*b/m.sqrt(2*y-a)))/2-B/(4*A))
            T.append((-m.sqrt(2*y-a)-m.sqrt(-2*y-a+2*b/m.sqrt(2*y-a)))/2-B/(4*A))
          if (-2*y-a-2*b/m.sqrt(2*y-a)>=0):
            T.append((-m.sqrt(2*y-a)+m.sqrt(-2*y-a-2*b/m.sqrt(2*y-a)))/2-B/(4*A))
            T.append((-m.sqrt(2*y-a)-m.sqrt(-2*y-a-2*b/m.sqrt(2*y-a)))/2-B/(4*A))

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
  def __init__(self,R,V,w,d=0.0286,gmu=0.1,h=0.03,masa=0.17,Mz=0.000382): #gmu-opóźnienie wywołane tarciem, h-wysokość bandy
    self.R=R #położenie
    self.V=V #prędkość
    self.d=d #promień
    self.w=w #prędkość kątowa
    self.masa=masa #masa bili
    self.time_bandy=[] #czasy do zderzenia z poszczególnymi bandami
    self.time_bile=[] #czasy do zderzenia z bilami
    self.Va=[]
    self.Va.append(self.V[0]-self.d*self.w[1])
    self.Va.append(self.V[1]+self.d*self.w[0])

    if (self.Va[0]**2+self.Va[1]**2!=0): #wersor prędkości
      self.wer=[self.Va[0]/m.sqrt(self.Va[0]**2+self.Va[1]**2),self.Va[1]/m.sqrt(self.Va[0]**2+self.Va[1]**2)]
      self.time_s=2*m.sqrt(self.Va[0]**2+self.Va[1]**2)/(7*gmu) #czas, po którym bila przestanie się ślizgać
      self.time_z=m.inf
    else:
      self.time_s=m.inf
      if (self.V[0]**2+self.V[1]**2!=0):
        self.wer=[self.V[0]/m.sqrt(self.V[0]**2+self.V[1]**2),self.V[1]/m.sqrt(self.V[0]**2+self.V[1]**2)]
        self.time_z=7*m.sqrt(self.V[0]**2+self.V[1]**2)/(5*gmu) #czas, po którym bila się zatrzyma
      else:
        self.wer=[0,0]
        self.time_z=m.inf

    if (self.w[2]==0): #czas do zatrzymania prędkości katowej w_z
      self.time_wz=m.inf
    else:
      self.time_wz=abs(self.w[2])*2*self.d**2*self.masa/(5*Mz)

  def re_wer(self,gmu): #odświeżenie wersora prędkości
    self.Va[0]=self.V[0]-self.d*self.w[1]
    self.Va[1]=self.V[1]+self.d*self.w[0]
    if (self.Va[0]**2+self.Va[1]**2!=0): #wersor prędkości Va
      self.wer=[self.Va[0]/m.sqrt(self.Va[0]**2+self.Va[1]**2),self.Va[1]/m.sqrt(self.Va[0]**2+self.Va[1]**2)]
      self.time_s=2*m.sqrt(self.Va[0]**2+self.Va[1]**2)/(7*gmu)
      self.time_z=m.inf
    else:
      self.time_s=m.inf
      if (self.V[0]**2+self.V[1]**2!=0): #wersor prędkości
        self.wer=[self.V[0]/m.sqrt(self.V[0]**2+self.V[1]**2),self.V[1]/m.sqrt(self.V[0]**2+self.V[1]**2)]
        self.time_z=7*m.sqrt(self.V[0]**2+self.V[1]**2)/(5*gmu)
      else:
        self.wer=[0,0]
        self.time_z=m.inf


  def time(b_1, b_2, a): #funkcja zwraca czas do zderzenia między bilami
    A=a**2*((b_1.wer[0]-b_2.wer[0])**2+(b_1.wer[1]-b_2.wer[1])**2)
    B=-a*((b_1.wer[0]-b_2.wer[0])*(b_1.V[0]-b_2.V[0])+(b_1.wer[1]-b_2.wer[1])*(b_1.V[1]-b_2.V[1]))
    C=((b_1.V[0]-b_2.V[0])**2+(b_1.V[1]-b_2.V[1])**2)-a*((b_1.R[0]-b_2.R[0])*(b_1.wer[0]-b_2.wer[0])+(b_1.R[1]-b_2.R[1])*(b_1.wer[1]-b_2.wer[1]))
    D=2*((b_1.R[0]-b_2.R[0])*(b_1.V[0]-b_2.V[0])+(b_1.R[1]-b_2.R[1])*(b_1.V[1]-b_2.V[1]))
    E=(b_1.R[0]-b_2.R[0])**2+(b_1.R[1]-b_2.R[1])**2-(b_1.d+b_2.d)**2
    T=rown(A,B,C,D,E) #znajdowanie wszystkich czasów zderzeń

    t=[]

    for i in T: #czas zawiera się w czasie od 0 do czasu zatrzymania lub do czasu ślizgania się pierwszej bili
      if (i>=0 and i<=min(b_1.time_z,b_2.time_z,b_1.time_s,b_2.time_s)):
        t.append(i)

    if (len(t)==0): #jeśli nie ma takich czasów tzn., że bile nigdy się nie zderzą
      return m.inf
    else:
      t=sorted(t) #wybieramy taki czas, żeby był najmniejszy i żeby pochodna wielomianu była <0
      for i in t:
        if (i>=0 and i<=min(b_1.time_z,b_2.time_z,b_1.time_s,b_2.time_s)):
          if (poch(A,B,C,D,E,i)<0):
            return i
            break
      return m.inf

  def t_bandy(self,a,b,gmu,h): #zwraca tablice o długości 4, kolejne elementu opisuja czas zderzenia z bandą: x=0, x=a, y=0, y=b
    i=[]
    if self.V[0]**2+2*gmu*self.wer[0]*(self.R[0]-a+m.sqrt((2*self.d-h)*h))>0 and self.wer[0]>0:
      i.append(m.inf)
      i.append((self.V[0]-m.sqrt(self.V[0]**2+2*gmu*self.wer[0]*(self.R[0]-a+m.sqrt((2*self.d-h)*h))))/(gmu*self.wer[0]))
    elif self.V[0]**2+2*gmu*self.wer[0]*(self.R[0]-m.sqrt((2*self.d-h)*h))>0 and self.wer[0]<0:
      i.append((self.V[0]+m.sqrt(self.V[0]**2+2*gmu*self.wer[0]*(self.R[0]-m.sqrt((2*self.d-h)*h))))/(gmu*self.wer[0]))
      i.append(m.inf)
    else:
      i.append(m.inf)
      i.append(m.inf)


    if self.V[1]**2+2*gmu*self.wer[1]*(self.R[1]-b+m.sqrt((2*self.d-h)*h))>0 and self.wer[1]>0:
      i.append(m.inf)
      i.append((self.V[1]-m.sqrt(self.V[1]**2+2*gmu*self.wer[1]*(self.R[1]-b+m.sqrt((2*self.d-h)*h))))/(gmu*self.wer[1]))
    elif self.V[1]**2+2*gmu*self.wer[1]*(self.R[1]-m.sqrt((2*self.d-h)*h))>0 and self.wer[1]<0:
      i.append((self.V[1]+m.sqrt(self.V[1]**2+2*gmu*self.wer[1]*(self.R[1]-m.sqrt((2*self.d-h)*h))))/(gmu*self.wer[1]))
      i.append(m.inf)
    else:
      i.append(m.inf)
      i.append(m.inf)

    self.time_bandy=i

  def t_bile(self,lista,gmu): #uzupełnia tablice "time_bile", w której przechowywane są czasy do zderzeń ze wszystkimi innymi bilami
    tab=[]

    for i in lista:
      tab.append(self.time(i,gmu))

    self.time_bile=tab

  def move(self, t, gmu, Mz): #odświeża układ po czasie t

    if (self.time_s<m.inf):
      self.R[0]+=t*self.V[0]-gmu*self.wer[0]*t**2/2 #zmiana położeń bil
      self.R[1]+=t*self.V[1]-gmu*self.wer[1]*t**2/2
      self.V[0]-=gmu*self.wer[0]*t #zmiana prędkości
      self.V[1]-=gmu*self.wer[1]*t
      self.Va[0]-=7*gmu*self.wer[0]*t/2
      self.Va[1]-=7*gmu*self.wer[1]*t/2
      self.w[0]-=5*gmu*self.wer[1]*t/(2*self.d) #zmiana prędkości kątowej
      self.w[1]+=5*gmu*self.wer[0]*t/(2*self.d)
    elif (self.time_z<m.inf):
      w=m.sqrt(self.w[0]**2+self.w[1]**2)
      self.R[0]+=t*self.V[0]-5*gmu*self.wer[0]*t**2/14 #zmiana położeń bil
      self.R[1]+=t*self.V[1]-5*gmu*self.wer[1]*t**2/14
      self.V[0]-=5*gmu*self.wer[0]*t/7 #zmiana prędkości
      self.V[1]-=5*gmu*self.wer[1]*t/7
      self.w[0]-=5*gmu*self.w[0]*t/(7*self.d*w) #zmiana prędkości kątowej
      self.w[1]-=5*gmu*self.w[1]*t/(7*self.d*w)

    self.w[2]-=Mz*5/(2*self.d**2*self.masa)*t #zmiana składowej "z" wektora prędkości kątowej
    self.time_wz-=t

    for i in range(len(self.time_bile)): #zmiana czasów do poszczególnych zdarzeń
      self.time_bile[i]-=t #zderzeń z bilami
    for i in range(4):
      self.time_bandy[i]-=t #zderzeń z bandami
    self.time_z-=t #zatrzymania
    self.time_s-=t

    self.re_wer(gmu) #zmiana wersora

  def t_least(self): #funkcja zwraca najszybsze wydarzenie: t-czas do wydarzenia, b-jaki typ zdarzenia to był, j-z czym się zderzyła (np. jeśli b="banda" i j=3 tzn., że bila zderza się z bandą, która jest 3. w tablicy time_bandy)
    j=-1
    t=self.time_z
    b="zatrzymanie" #zatrzymanie bili
    if (self.time_wz<t):
      t=self.time_wz
      b="zatrzymanie_wz" #zatrzymanie prędkości kątowej wz
    if (self.time_s<self.time_z):
      t=self.time_s
      b="ślizg" #koniec poslizgu bili
    for i in range(len(self.time_bandy)):
      if self.time_bandy[i]<t:
        t=self.time_bandy[i]
        b="banda" #odbicie od bandy
        j=i
    for i in range(len(self.time_bile)):
      if self.time_bile[i]<t:
        t=self.time_bile[i]
        b="bila" #odbicie od bili
        j=i
    return t,b,j

class stol:
  def __init__(self, lista, a=3.569, b=1.778, gmu=0.1,h=0.03, Mz=0.000382):
    self.lista=lista #bile na stole
    self.a=a #wymiary stołu
    self.b=b
    self.gmu=gmu #opóźnienie wywołane tarciem z podłożem
    self.h=h #wysokość bandy
    self.Mz=Mz #współczynnik tarcia dla współrzędnej "z" wektora prędkości katowej

  def inicjacja(self): #uzupełnienie tabel we własnościach bil na stole
    for i in self.lista:
      i.t_bile(self.lista,self.gmu)
      i.t_bandy(self.a,self.b,self.gmu,self.h)

  def t_least(self):
    T=m.inf
    for i in range(len(self.lista)): #wybór najbliższego czasowo zdarzenia
      t,b,j=self.lista[i].t_least()
      if (T>t):
        T=t
        B=b
        J=j
        k=i
    if (T==m.inf):
      return T,"koniec",-1,-1
    else:
      return T,B,J,k


  def ref(self): #wywołanie zdarzenia i aktualizacja czasu
    T,B,J,k=self.t_least()

    for i in self.lista: #aktualizacja własności wszystkich bil tak, aby otrzymać ich własności chwilę przed zderzeniem
      i.move(T,self.gmu, self.Mz)
      if (i.R[0]>self.a-m.sqrt(self.h*(2*i.d-self.h))):
        i.R[0]=self.a-m.sqrt(self.h*(2*i.d-self.h))
      if (i.R[0]<m.sqrt(self.h*(2*i.d-self.h))):
        i.R[0]=m.sqrt(self.h*(2*i.d-self.h))
      if (i.R[1]>self.b-m.sqrt(self.h*(2*i.d-self.h))):
        i.R[1]=self.b-m.sqrt(self.h*(2*i.d-self.h))
      if (i.R[1]<m.sqrt(self.h*(2*i.d-self.h))):
        i.R[1]=m.sqrt(self.h*(2*i.d-self.h))

    #wywołanie zdarzenia
    if (B=="zatrzymanie"):
      self.lista[k].V[0]=0
      self.lista[k].V[1]=0
      self.lista[k].w[0]=0
      self.lista[k].w[1]=0
      self.lista[k].re_wer(self.gmu)
      self.lista[k].t_bandy(self.a,self.b,self.gmu,self.h)
      self.lista[k].t_bile(self.lista,self.gmu)

      for i in range(len(self.lista)):
        if (i!=k):
          self.lista[i].time_bile[k]=self.lista[k].time_bile[i]

    elif (B=="ślizg"):
      self.lista[k].Va[0]=0
      self.lista[k].Va[1]=0
      self.lista[k].re_wer(self.gmu)
      self.lista[k].t_bandy(self.a,self.b,self.gmu,self.h)
      self.lista[k].t_bile(self.lista,self.gmu)

      for i in range(len(self.lista)):
        if (i!=k):
          self.lista[i].time_bile[k]=self.lista[k].time_bile[i]

    elif (B=="banda"):
      if (J==0 or J==1):
        self.lista[k].V[0]=-self.lista[k].V[0]
      if (J==2 or J==3):
        self.lista[k].V[1]=-self.lista[k].V[1]
      self.lista[k].re_wer(self.gmu)
      self.lista[k].t_bandy(self.a,self.b,self.gmu,self.h)
      self.lista[k].t_bile(self.lista,self.gmu)

      for i in range(len(self.lista)):
        if (i!=k):
          self.lista[i].time_bile[k]=self.lista[k].time_bile[i]

    elif (B=="bila"):
      V1=self.lista[k].V
      V2=self.lista[J].V
      R1=self.lista[k].R
      R2=self.lista[J].R
      a=2*((V1[0]-V2[0])*(R1[0]-R2[0])+(V1[1]-V2[1])*(R1[1]-R2[1]))/((self.lista[k].masa+self.lista[J].masa)*((R1[0]-R2[0])**2+(R1[1]-R2[1])**2))
      self.lista[k].V[0]-=a*self.lista[J].masa*(R1[0]-R2[0])
      self.lista[k].V[1]-=a*self.lista[J].masa*(R1[1]-R2[1])
      self.lista[J].V[0]-=a*self.lista[k].masa*(R2[0]-R1[0])
      self.lista[J].V[1]-=a*self.lista[k].masa*(R2[1]-R1[1])
      self.lista[k].re_wer(self.gmu)
      self.lista[J].re_wer(self.gmu)

      self.lista[k].t_bandy(self.a,self.b,self.gmu,self.h)
      self.lista[k].t_bile(self.lista,self.gmu)
      self.lista[J].t_bandy(self.a,self.b,self.gmu,self.h)
      self.lista[J].t_bile(self.lista,self.gmu)

      for i in range(len(self.lista)):
        if (i!=k and i!=J):
          self.lista[i].time_bile[k]=self.lista[k].time_bile[i]
          self.lista[i].time_bile[J]=self.lista[J].time_bile[i]

  def energia(self): #energia układu
    k=0
    for i in self.lista:
      k+=i.masa*(i.V[0]**2+i.V[1]**2)/2+(i.d**2)*i.masa*(i.w[0]**2+i.w[1]**2+i.w[2]**2)/5
    return k

#(self,R,V,w,d=0.0286,gmu=0.1,h=0.03,masa=0.17,Mz=0.000382)
args = [[[9.,3.],[-1.5,0.],[1.,1.,0]],
        [[3.,3.],[0.8, 0.],[3.,0.,2.]]]
bil1=bila(args[0][0], args[0][1], args[0][2])
bil2=bila(args[1][0], args[1][1], args[1][2]) 
kule=stol([bil1, bil2],10,10,0.1)
kule.inicjacja()

x = np.zeros((1000,len(kule.lista)))
y = np.zeros((1000,len(kule.lista)))

f = open("bilard.txt", "w")

for elem in args:
  f.write('{0} {1} {2} {3}'.format(elem[0][0], elem[0][1], elem[1][0], elem[1][1]))
  f.write(' ')

f.write('\n')

for i in range(1000):
  kule.ref()
  k = 0
  for j in kule.lista:
    print(j.R, j.V, j.w)
    f.write('{0} {1} {2} {3}'.format(j.R[0], j.R[1], j.V[0], j.V[1]))
    x[i][k] = j.R[0]
    y[i][k] = j.R[1]
    k+=1
    print(' ')
    f.write(' ')
  print('\n')
  f.write('\n')
  
f.close()

plt.scatter(x, y)
plt.show()
