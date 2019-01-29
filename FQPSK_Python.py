from matplotlib import pylab as pl
import numpy as np
import random
from math import sqrt as sqrt
from math import cos as cos
from math import sin as sin
from math import pi as pi

Rsym = 8000                 # Input symbol rate
Rbit = Rsym*2               # Input bit rate
Nos = 60                    # Oversampling factor
ts = (1/Rsym) / Nos         # Input sample period
Fcarrier = 80000            # carrier
A = 1/sqrt(2)               # constant Envelope

#------------IJF-Encoder-------------------
# baseband signals
s0 = [A for i in range(Nos)] # s8 = -s0
pl.figure(1)
pl.plot(s0)
pl.show()

s1 = [A for i in range(30)] # s9 = -s1
for i in range(30,60):
    s1.append(1-(1-A)*cos(pi*(i-Nos/2)/Nos)*cos(pi*(i-Nos/2)/Nos))
pl.figure(2)
pl.plot(s1)
pl.show()

s2 = []         # s10 = -s2
for i in range(30):
    s2.append(1-(1-A)*cos(pi*(i-Nos/2)/Nos)*cos(pi*(i-Nos/2)/Nos))

s =[A for i in range(30)]
s2.extend(s)
pl.figure(3)
pl.plot(s2)
pl.show()

s3 = []     # s11 = -s3                
for i in range(60):
    s3.append(1-(1-A)*cos(pi*(i-Nos/2)/Nos)*cos(pi*(i-Nos/2)/Nos))
pl.figure(4)
pl.plot(s3)
pl.show()

s4 = []     # s12 = -s4
for i in range(60):
    s4.append(A*sin(pi*(i-Nos/2)/Nos))
pl.figure(5)
pl.plot(s4)
pl.show()

s5 = []     # s13 = -s5
for i in range(30):
    s5.append(A*sin(pi*(i-Nos/2)/Nos))
for i in range(30,60):
    s5.append(sin(pi*(i-Nos/2)/Nos))
pl.figure(6)
pl.plot(s5)
pl.show()  

s6 = []     # s14 = -s6
for i in range(30):
    s6.append(sin(pi*(i-Nos/2)/Nos))
for i in range(30,60):
    s6.append(A*sin(pi*(i-Nos/2)/Nos))
pl.figure(7)
pl.plot(s6)
pl.show()  

s7 = []     # s15 = -s7
for i in range(60):
    s7.append(sin(pi*(i-Nos/2)/Nos))
pl.figure(8)
pl.plot(s7)
pl.show()

s8,s9,s10,s11,s12,s13,s14,s15=[],[],[],[],[],[],[],[]
for i in range(len(s0)):
    s8.append(s0[i]*-1) 
    s9.append(s1[i]*-1)  
    s10.append(s2[i]*-1) 
    s11.append(s3[i]*-1) 
    s12.append(s4[i]*-1) 
    s13.append(s5[i]*-1)  
    s14.append(s6[i]*-1) 
    s15.append(s7[i]*-1) 

#------------Signal-Mapping-------------------
S = [s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15]
SourceLen = 40
source = [random.randint(0,3) for i in range(SourceLen)] 

def QPSKmod(data):
    c = 0
    for j in data:
        if j==0:
            data[c]=0.7071+0.7071j
        elif j==1:
            data[c]=-0.7071+0.7071j
        elif j==2:
            data[c]=-0.7071-0.7071j
        elif j==3:
            data[c]=0.7071-0.7071j
        c += 1
    return data

modData = QPSKmod(source)
modIData = np.real(modData)>0
modQData = np.imag(modData)>0
modIData = list(modIData*1)
modQData = list(modQData*1)

def xor(a,b):
    c = a^b
    return c

FQPSK_IData,FQPSK_QData = [],[]
for i in range(3,len(modIData)-1):
    I0 = xor(modQData[i],modQData[i-1])
    I1 = xor(modQData[i-1],modQData[i-2])
    I2 = xor(modIData[i],modIData[i-1])
    I3 = (modIData[i]>0)*1
    Q0 = xor(modIData[i+1],modIData[i])
    Q1 = I2
    Q2 = I0
    Q3 = (modQData[i]>0)*1
    IndexI = I3*8+I2*4+I1*2+I0
    IndexQ = Q3*8+Q2*4+Q1*2+Q0
    FQPSK_IData.extend(S[IndexI])
    FQPSK_QData.extend(S[IndexQ])

t = np.linspace(0,len(FQPSK_IData)*ts,len(FQPSK_IData))
pl.figure(9)
pl.plot(t,FQPSK_IData,color='g')
pl.show()

pl.figure(10)
pl.plot(t,FQPSK_QData,color='r')
pl.show()

wt= 2*pi*Fcarrier*t
cosCarrier = [cos(wt[i]) for i in range(len(wt))]
sinCarrier = [sin(wt[i]) for i in range(len(wt))]

FQPSK_IData = np.array(FQPSK_IData)
FQPSK_QData = np.array(FQPSK_QData)

finalData = FQPSK_IData*cosCarrier + FQPSK_QData*sinCarrier
time = np.linspace(0,len(finalData)*ts,len(finalData))

pl.figure(11)
pl.plot(time,finalData,color='k')
pl.show()