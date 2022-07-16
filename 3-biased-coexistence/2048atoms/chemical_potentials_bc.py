# This script calculates the free energy difference between the liquid and the solid for several temperatures

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

##############################################
# Add more temperatures here if you have them!
##############################################
temperatures=np.array([400]) 
#  For instance: temperatures=np.array([360,380,400,420]) 
##############################################


def func(x,a,b):
    return a*x+b

# Some parameters
ignoreN=1000 # Number of initial lines to discard
nbins=50 # Number of bins in histogram
histmin=1000 # Minimum of interval for histogram construction
histmax=1200 # Maximum of interval for histogram construction

chemical_potentials=np.zeros(temperatures.shape[0])
counter=0

# First plot the FES at all temperatures

for temp in temperatures:
    filename=str(temp) + "K" + '/COLVAR'
    data = np.genfromtxt(filename)
    bias= data[ignoreN:,3]+data[ignoreN:,8]+data[ignoreN:,10] # All bias potentials
    cv=data[ignoreN:,13] # This is the "strict" cv
    beta=1./(0.00831441001626*temp)
    logweights=beta*bias
    logweights -= np.amax(logweights)
    histo, bin_edges = np.histogram(cv,weights=np.exp(logweights),bins=nbins,range=(histmin,histmax))
    bin_centers = (bin_edges[1:]+bin_edges[:-1])/2
    fes = -(1/beta)*np.log(histo)
    offset = np.mean(np.ma.masked_invalid(fes))
    fes -= offset
    plt.plot(bin_centers,fes)
    # Now fit a straight line
    bin_centers = bin_centers[np.isfinite(fes)]
    fes = fes[np.isfinite(fes)]
    popt, pcov = curve_fit(func, bin_centers, fes)
    x=np.linspace(histmin,histmax,10)
    plt.plot(x,func(x,*popt),'--',color='black',alpha=0.5)
    plt.xlabel("# solid-like atoms")
    plt.ylabel("Free energy (kJ/mol)")
    plt.xlim([histmin,histmax])
    # Chemical potential is the slope
    chemical_potentials[counter]=popt[0]
    counter += 1
plt.show()


# Now let's plot the chemical potentials vs temperature

plt.scatter(temperatures,chemical_potentials)
if (temperatures.shape[0]>1):
    popt, pcov = curve_fit(func, temperatures,chemical_potentials)
    x=np.linspace(355,425,100)
    plt.plot(x,func(x,*popt))
    melting_temperature=-popt[1]/popt[0]
    print("Melting T at 1 bar with 2048 atoms is ",melting_temperature," K")


plt.xlim([355,425])
plt.ylim([-0.2,0.45])
plt.plot([355,425],[0,0],'--',color='black',alpha=0.5)
plt.xlabel("Temperature (K)")
plt.ylabel("Chemical potential difference (kJ\mol)")

plt.show()
