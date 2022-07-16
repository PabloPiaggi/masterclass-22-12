# This script calculates the free energy difference between the liquid and the solid for several temperatures

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

##############################################
# Add more temperatures here if you have them!
##############################################
temperatures=np.array([400]) 
#  For instance: temperatures=np.array([380,400,420]) 
##############################################

##############################################
# Change number of atoms here, if needed
##############################################
Natoms=1024
##############################################

# Function to compute free energy differences
def free_energy_difference(CV,bias,temperature,CVlimit):
    """Calculate the free energy difference between two phases.

    Args:
        CV (numpy array): An array with the collective variable values
        bias (numpy array): An array with the bias values in kJ/mol
        temperature (float): The temperature in K
        CVlimit (float): Watershed between the two phases (CVunits)

    Returns:
        float: the free energy in kJ/mol
    """
    beta=1./(0.00831441001626*temperature) # 1/(kJ/mol)
    probLiquid=np.sum(np.exp(beta*bias[CV<=CVlimit]))
    probSolid=np.sum(np.exp(beta*bias[CV>=CVlimit]))
    freeEnergy=-(1./beta)*np.log(probSolid/probLiquid)
    return freeEnergy

# Read data and calculate chemical potential
ignoreN=1000
chemical_potentials=np.zeros(temperatures.shape[0])
for i in range(temperatures.shape[0]):
    string=str(int(temperatures[i]))
    filename=string + "K/COLVAR"
    data=np.genfromtxt(filename)
    bias=data[ignoreN:,3]+data[ignoreN:,10]
    cv=data[ignoreN:,2]
    # This is the value of the CV that separates liquid and solid configurations
    CVlimit = float(Natoms/2) 
    # Next lines are chemical potentials: free energy differences / number of atoms
    chemical_potentials[i]=free_energy_difference(cv,bias,temperatures[i],CVlimit)/Natoms 


# Plot data
plt.scatter(temperatures,chemical_potentials)

# If there are at least two temperatures let's do a linear fit
# and calculate the melting (coexistence) temperature
def func(x, a, b):
    return a * x + b
if (temperatures.shape[0]>1):
    popt, pcov = curve_fit(func, temperatures,chemical_potentials)
    x=np.linspace(355,425,100)
    plt.plot(x,func(x,*popt))
    melting_temperature=-popt[1]/popt[0]
    print("Melting T at 1 bar with ", Natoms, " atoms is ",melting_temperature," K")

# Some plot customization

plt.xlim([355,425])
plt.ylim([-0.2,0.4])
plt.plot([355,425],[0,0],'--',color='black',alpha=0.5)
plt.xlabel("Temperature (K)")
plt.ylabel("Chemical potential difference (kJ\mol)")

plt.show()

