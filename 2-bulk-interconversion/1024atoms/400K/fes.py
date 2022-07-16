# This script computes the FES using reweighting

import numpy as np
import matplotlib.pyplot as plt

###########################################
# Change temperature (in K) here, if needed
###########################################
temperature=400
###########################################

ignoreN=1000 # Discard N lines during which the bias changes
data=np.genfromtxt("COLVAR")
cv=data[ignoreN:,2]
bias=data[ignoreN:,3]+data[ignoreN:,10] # We have two bias potentials
kb=0.008314462618 # Boltzmann constant in kJ/mol/K
beta=1./(kb*temperature)
logweights=beta*bias
logweights -= np.amax(logweights) # Subtract max to avoid overfow probles
hist, bin_edges = np.histogram(cv,weights=np.exp(logweights),range=(0,250),bins=100)
bin_centers=(bin_edges[1:]+bin_edges[:-1])/2. # Compute bin centers
fes=-(1./beta)*np.log(hist)
fes -= np.amin(fes) # Set min to zero
plt.plot(bin_centers,fes)
plt.xlabel("CV")
plt.ylabel("Free energy (kJ/mol)")

plt.show()
