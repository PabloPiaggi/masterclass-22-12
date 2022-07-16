# This script calculates the free energy difference between the liquid and the solid for several temperatures

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


##############################################
# Adjust the line below according to the
# temperatures you simulated
##############################################
temperatures=np.arange(330,420,10)
##############################################

numAtoms=1024
enthalpy_liquid=np.zeros(temperatures.shape[0])
enthalpy_bcc=np.zeros(temperatures.shape[0])
counter=0
eVtokJmol=96.4853075
for temp in temperatures:
    enthalpy_liquid[counter]=np.mean(np.genfromtxt("liquid/" + str(int(temp)) + "K/thermo.txt")[:,1])*eVtokJmol/numAtoms
    enthalpy_bcc[counter]=np.mean(np.genfromtxt("bcc/" + str(int(temp)) + "K/thermo.txt")[:,1])*eVtokJmol/numAtoms
    counter += 1

plt.scatter(temperatures,enthalpy_bcc,label="bcc")
plt.scatter(temperatures,enthalpy_liquid,label="liquid")
plt.xlabel("Temperature (K)")
plt.ylabel("Enthalpy (kJ/mol)")
plt.ylim([-99,-92])
plt.legend()
plt.show()

# Interpolate the difference between enthalpies
f_diff = interpolate.interp1d(temperatures,enthalpy_liquid-enthalpy_bcc,fill_value="extrapolate") #,kind='cubic')

# Do the thermodynamic integration
temps_ti=np.linspace(325,425,100)
chemical_potential_ti=np.zeros(temps_ti.shape[0])
meltingT=366
for i in range(temps_ti.shape[0]):
    dummy_temps=np.linspace(meltingT,temps_ti[i],1000)
    integrand=f_diff(dummy_temps)/np.power(dummy_temps,2)
    chemical_potential_ti[i]=temps_ti[i]*np.trapz(integrand,dummy_temps)


plt.plot(temps_ti,chemical_potential_ti)

#  Some plot customization
plt.xlim([355,425])
plt.ylim([-0.2,0.4])
plt.plot([355,425],[0,0],'--',color='black',alpha=0.5)
plt.xlabel("Temperature (K)")
plt.ylabel("Chemical potential difference (kJ\mol)")

plt.show()
