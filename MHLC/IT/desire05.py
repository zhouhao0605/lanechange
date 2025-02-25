# this is to implement the desire function

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

sns.set()

w=15.0
u=110.0 # note that here we use the speed in ft/s
tau1= 3.0
gamma= 1.0 # gamma will change the shape of the exponential distribution, which represents the influence of density
v4= 60.0
s0= 2500
p0= 0.5
dx= 55.0


L=4440.0
x= np.arange(0,L,1)


# def sending(x):
#     flow = 2500*x/L
#     return flow


def phi1(x):
    v=40.0
    deltav=(L-x)/L*(v-10.0)
    pi1=deltav/75.0/tau1
    desire=pi1/u
    return desire

def phi_60(x):
    pi2 = np.exp(-x/(800.0*1.1))
    # actually the tau2 denotes the changing rate of exponential, we can interpret that tau2
    # the shape of exponential distribution influence the rate of probability increase along the distance
    # actually the shape should represent the effect on target lane density
    desire=pi2
    return desire

def phi_50(x):
    pi2 = np.exp(-x/(800.0*1.05))
    # actually the tau2 denotes the changing rate of exponential, we can interpret that tau2
    # the shape of exponential distribution influence the rate of probability increase along the distance
    # actually the shape should represent the effect on target lane density
    desire=pi2
    return desire

def phi_40(x):
    pi2 = np.exp(-x/(800.0*1.01))
    # actually the tau2 denotes the changing rate of exponential, we can interpret that tau2
    # the shape of exponential distribution influence the rate of probability increase along the distance
    # actually the shape should represent the effect on target lane density
    desire=pi2
    return desire

def phi_30(x):
    pi2 = np.exp(-x/(800.0*0.97))
    # actually the tau2 denotes the changing rate of exponential, we can interpret that tau2
    # the shape of exponential distribution influence the rate of probability increase along the distance
    # actually the shape should represent the effect on target lane density
    desire=pi2
    return desire

def phi_20(x):
    pi2 = np.exp(-x/(800.0*0.885))
    # actually the tau2 denotes the changing rate of exponential, we can interpret that tau2
    # the shape of exponential distribution influence the rate of probability increase along the distance
    # actually the shape should represent the effect on target lane density
    desire=pi2
    return desire

def phi_10(x):
    pi2 = np.exp(-x/(800.0*0.84))
    # actually the tau2 denotes the changing rate of exponential, we can interpret that tau2
    # the shape of exponential distribution influence the rate of probability increase along the distance
    # actually the shape should represent the effect on target lane density
    desire=pi2
    return desire


def mlc(dist):
    '''
    the function will take in one argument, i.e. the distribution of mandatory lane changes along distance
    and return the output like the PDF and CDF of theoretical lane changes along the distance
    :param dist:
    :return:
    '''
    sending=[] # s1 means the list of sending flow at each cell
    s0=2500.0
    penetration = []
    pe = p0 =0.5
    pne = 1 - p0
    dmlc = []
    cum = []
    sum = 0
    for i in range(70,1,-1):

    # s0 is the old sending flow from last time
    # s1 is the remaining sending flow after this time
    # pe is the penetration of exiting vehicles
    # pne is the penetration of non-exiting vehiclesl
    # lc1 is the real discretionary LC flow generated by poisson distribution
    # lc2 is the real mandatory LC flow generated by poisson distribution
    # quad is the integrating function along distance
        I1 = quad(phi1, (i-1)*dx, i*dx) # fraction of discretionary LC flow from i*dx to (i+1)*dx
        print('the probability of discretionary lane changes during such a cell', I1[0])
        I2 = quad(dist, (i-1)*dx, i*dx) # fraction of mandatory LC flow from i*dx to (i+1)*dx
        print('the probability of mandatory lane changes during such a cell', I2[0])
        # print('the fraction of LC flow', p)
        # here we should generate the real LC flow by Poisson distribution,using the probability as the mean value
        lc1=s0*pne*I1[0]/u # this is to generate the real discretionary lane change flow
        lc2=s0*pe*I2[0]/u# this is to generate the expected mandatory lane change flow, still it needs a poisson distribution
        sum = sum + lc2 # this is to record the sum of exiting vehicles
        dmlc.append(lc2) # in simulation, the rate and probability is for the average value, not for the real numbers. You need PP
        s1=s0-lc1-lc2 # this is to calculate the remaining sending flow, s1 means the remaining sending flow
        pe=(s0*pe-lc2)/s1 # this is update the penetration of exiting vehicles
        pne=1.0-pe
        # prob.append(phi2(x*(70-i)))
        sending.append(s1)
        penetration.append(pe)
        # we should do a Poisson distribution to generate the real flow
        cum.append(sum)
        s0=s1
    # after end the loop
    sending=sending[::-1] # we need to inverse the list, so the distance can actually start from 0 to 4000
    dmlc = dmlc[::-1]
    dmlc = np.array(dmlc)
    dmlc = dmlc/sum
    print('the generated dmlc flow is',dmlc)
    penetration=penetration[::-1]
    # prob=prob[::-1]
    cum = cum[::-1]
    cum = np.array(cum)
    cum = cum/sum
    x = np.linspace(0,L,69)
    xvals = np.linspace(0, L, 500)
    dmlc = np.interp(xvals, x, dmlc)
    sending = np.interp(xvals, x, sending)
    penetration =np.interp(xvals, x, penetration)
    cum = np.interp(xvals, x, cum)
    return sending,dmlc,cum,penetration


linewidth=2
xvals = np.linspace(0, L, 500)
## execute the different spatial distribution of mandatory lane changes
sending_60,dmlc_60,cum_60,penetration_60 = mlc(phi_60)
sending_50,dmlc_50,cum_50,penetration_50 = mlc(phi_50)
sending_40,dmlc_40,cum_40,penetration_40 = mlc(phi_40)
sending_30,dmlc_30,cum_30,penetration_30 = mlc(phi_30)
sending_20,dmlc_20,cum_20,penetration_20 = mlc(phi_20)
sending_10,dmlc_10,cum_10,penetration_10 = mlc(phi_10)



f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

ax1.set_title('The exponential-distributed desire of mandatory lane changes')
ax1.plot(xvals, phi_60(xvals),color="#9b59b6", lw=linewidth) # gamma= 1.5
ax1.plot(xvals, phi_50(xvals),color="#3498db", lw=linewidth) # gamma= 1.5
ax1.plot(xvals, phi_40(xvals),color="#95a5a6", lw=linewidth) # gamma= 1.5
ax1.plot(xvals, phi_30(xvals),color="#e74c3c", lw=linewidth) # gamma= 1.5
ax1.plot(xvals, phi_20(xvals),color="#34495e", lw=linewidth) # gamma= 1.5
ax1.plot(xvals, phi_10(xvals),color="#2ecc71", lw=linewidth) # gamma= 1.5




ax2.set_title('The simulated number of mandatory lane changes')
ax2.set_ylabel('flow(veh/h)', fontsize=10)
ax2.plot(xvals, sending_60, sns.xkcd_rgb["pale red"], lw=linewidth)
# ax2.plot(xvals, s_2, sns.xkcd_rgb["medium green"], lw=linewidth)
# ax2.plot(xvals, s_3, sns.xkcd_rgb["denim blue"], lw=linewidth)


ax3.set_xlabel('distance to gore (ft)', fontsize=10)
ax3.set_title('The PDF of spatial distribution of mandatory lane changes')
ax3.set_ylabel('vehicles', fontsize=10)
ax3.plot(xvals, dmlc_60, color="#9b59b6", lw=linewidth)
ax3.plot(xvals, dmlc_50, color="#3498db", lw=linewidth)
ax3.plot(xvals, dmlc_40, color="#95a5a6", lw=linewidth)
ax3.plot(xvals, dmlc_30, color="#e74c3c", lw=linewidth)
ax3.plot(xvals, dmlc_20, color="#34495e", lw=linewidth)
ax3.plot(xvals, dmlc_10, color="#2ecc71", lw=linewidth)

# ax3.plot(xvals, y_60, '*', sns.xkcd_rgb["pale red"], lw=linewidth)

# ax3.plot(xvals, dmlc_2, sns.xkcd_rgb["medium green"], lw=linewidth)
# ax3.plot(xvals, dmlc_3, sns.xkcd_rgb["denim blue"], lw=linewidth)


ax4.set_title('The cumulative probability of mandatory lane changes')
ax4.set_ylabel('vehicles', fontsize=10)
ax4.set_xlabel('distance to gore (ft)', fontsize=10)
ax4.plot(xvals, cum_60,color="#9b59b6",lw=linewidth)
ax4.plot(xvals, cum_50,color="#3498db",lw=linewidth)
ax4.plot(xvals, cum_40,color="#95a5a6",lw=linewidth)
ax4.plot(xvals, cum_30,color="#e74c3c",lw=linewidth)
ax4.plot(xvals, cum_20,color="#34495e",lw=linewidth)
ax4.plot(xvals, cum_10,color="#2ecc71",lw=linewidth)


# ax4.plot(xvals, cum_2,sns.xkcd_rgb["medium green"],lw=linewidth)
# ax4.plot(xvals, cum_3,sns.xkcd_rgb["denim blue"],lw=linewidth)

# color="#9b59b6"

sns.axes_style("darkgrid")
plt.show()



