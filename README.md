# PLUMED Masterclass 22.12
# Free energy calculations for crystalline solids with the environment similarity CV 

Authors: Pablo Piaggi
Date: July 18, 2022

## Aims

This Masterclass is an introduction to the use of the environment similarity CV available in PLUMED to the calculation of liquid-solid free energy differences (chemical potentials).

## Objectives

The objectives of this Masterclass are:
- Learn to define reference environments for a crystal structure and choose appropriate parameters
- Learn how to run simulations in which the bulk liquid and the bulk solid are reversibly interconverted
- Learn how to run biased coexistence simulations (similar to interface pinning)
- Understand the importance of finite size effects in these simulations
- Understand the advantages and limitations of each method

## Prerequisites

We assume that the person that will follow this tutorial is familiar with the linux terminal, LAMMPS, and basic functionality of PLUMED.
Knowledge of one enhanced sampling technique, such as metadynamics, is recommended.

## Setting up PLUMED

We will use LAMMPS and PLUMED to perform the calculations.
Conda packages with the software required for this class have been prepared and you can install them following the instructions in [this link](https://github.com/plumed/masterclass-2022).
Make sure to install the conda package for LAMMPS.

The environment similarity CV is a part of the crystallization module and you will need to enable this module if you are compiling PLUMED on your own.
Also, LAMMPS has to be compiled with the following optional packages PLUMED, MANYBODY, EXTRA-DUMP, and EXTRA-FIX.

The data needed to run the exercises of this Masterclass can be found on [GitHub](https://github.com/PabloPiaggi/masterclass-22-12).
You can clone this repository locally on your machine using the following command:
```
git clone https://github.com/PabloPiaggi/masterclass-22-12
```

## Summary of theory

We would like to define a per-atom quantity that tells us how similar the environments around atoms in the simulation box are to the environments found in some reference crystal structure.
Crystal structures are usually defined by a Bravais lattice with an associated basis of atoms.
An important consideration, that follows from the symmetry properties of lattices, is that the number of distint environments that exist in a crystal structure is equal to the number of atoms in the basis $M$.
To judge if a given environment is compatible with a given crystal structures, we will have to compare it against $M$ reference environments.

The environment similarity kernel is a way to quantify the similarity between environments.
This idea was introduced in this article \cite Piaggi-JCP-2019 and is based on the [SOAP descriptors](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.87.184115) of Bartok et al.
Unlike SOAPs, this kernel will be non rotationally invariant and thus will break the SO(3) symmetry of space.
The starting point for the definition of our CV is the local atomic density around a given atom.
We consider an environment $\chi$ around this atom and we define the density by,
$\rho_{\chi}(\mathbf{r})=\sum\limits_{i\in\chi} \exp\left(- \frac{|\mathbf{r}_i-\mathbf{r}|^2} {2\sigma^2} \right),$
where $i$ runs over the neighbors in the environment $\chi$, $\sigma$ is a broadening parameter, and $\mathbf{r}_i$ are the
coordinates of the neighbors relative to the central atom.
We will see later how the best $\sigma$ can be rigorously determined.
We now define a single reference environment $\chi_0$ that contains $n$ reference positions $\{\mathbf{r}^0_1,...,\mathbf{r}^0_n\}$
that describe, for instance, the nearest neighbors in a given crystal structure.

The environments $\chi$ and $\chi_0$ are compared using the kernel,

$k_{\chi_0}(\chi)= \int d\mathbf{r} \rho_{\chi}(\mathbf{r}) \rho_{\chi_0}(\mathbf{r}) .$

Combining the two equations above and performing the integration analytically we obtain,

$k_{\chi_0}(\chi)= \sum\limits_{i\in\chi} \sum\limits_{j\in\chi_0} \pi^{3/2} \sigma^3  \exp\left(-\frac{|\mathbf{r}_i-\mathbf{r}^0_j|^2} {4\sigma^2} \right).$

The kernel is finally normalized,

$\tilde{k}_{\chi_0}(\chi)=\frac{1}{n}\sum\limits_{i\in\chi}\sum\limits_{j\in\chi_0}\exp\left(-\frac{|\mathbf{r}_i-\mathbf{r}^0_j|^2}{4\sigma^2}\right),$

such that $\tilde{k}_{\chi_0}(\chi_0)=1$.
We note that using the normalization above, the measure looses the symmetry property $k_{\chi_0}(\chi)=k_{\chi}(\chi_0)$.

The definition above is only useful for Bravais lattices since these have a single, unique atomic environment.
The kernel can be generalized to crystal structures described as a lattice with a basis of more than one atom.
As discussed above, in this case there is more than one type of environment.
We consider the case of $M$ environments $X = \chi_1,\chi_2,...,\chi_M$ and we define the kernel through a best match strategy:

$\tilde{k}_X(\chi)= \frac{1}{}\lambda}\log\left(\sum\limits_{l=1}^{M}\exp\left(\lambda\:\tilde{k}_{\chi_l}(\chi)\right)\right).$

For a large enough $\lambda$ this expression will select the largest $\tilde{k}_{\chi_l}(\chi)$ with $\chi_l\in X$.

$\tilde{k}_X(\chi)$ is a per-atom quantity and we will have to compute global functions of these quantities, for instance, the mean or the number of atoms with at $\tilde{k}_X(\chi)$ larger than some value.

## The system: Sodium as the alanine dipeptide of solids

Alanine dipeptide is the prototypical system on which enhanced sampling methods are tested (and sometimes benchmarked) on.
The reasons behind this choice is that alanine dipeptide is a small and relatively simple molecule that nonetheless captures well the phenomenon of conformational isomerism with relatively large free energy barriers.
I argue that a similar system in the context of materials is sodium.
It crystallizes in the bcc structure which is one of the simplest crystal structures.
Also, it does not show the competition between fcc and hcp structures typical of systems that crystallize in these two compact structures.
This fact greatly simplifies the task of characterizing the structure: all that we can see is liquid or bcc environments.
We will use an embedded atom model (EAM) for sodium.

## Exercise 1: Choosing reference environments and apropriate \f$\sigma\f$ values

In the case of the bcc structure, the reference environment for the environment similarity CV can be chosen automatically using the following PLUMED input:

```
ENVIRONMENTSIMILARITY ...
 SPECIES=1-1024
 CRYSTAL_STRUCTURE=BCC
 LATTICE_CONSTANTS=0.423
 SIGMA=0.07
... ENVIRONMENTSIMILARITY
```

Here we have chosen the bcc crystal structure with a lattice constant of 0.423 nm which is appropriate for bcc sodium.
This choice will automatically build an environment with 14 nearest neighbors.
There are other structures for which environments can be built automatically, see the manual for further information \ref ENVIRONMENTSIMILARITY .
Another option is to use CRYSTAL_STRUCTURE=CUSTOM and provide environments manually as PDB files using the REFERENCE keyword.
In this case, I suggest using the [Environment Finder](https://mybinder.org/v2/gh/PabloPiaggi/EnvironmentFinder/master?urlpath=apps%2FApp.ipynb) app to determine the appropriate environments for your structure.

For the PLUMED input above we also have to determine the value for the SIGMA keyword.
The first exercise of this class is to determine this value.
Here is the rationale behind the choice.
We are trying to determine a per-atom quantity that is able to distinguish liquid from solid environments.
We should find a SIGMA such that the probability of mislabeling liquid atoms as solid, and viceversa, is minimized.
This can be done by computing the probability of finding a given value of $ \tilde{k}_X(\chi) $ in the bulk solid and the bulk liquid.
So, first things first, let's do a simulation of the bulk liquid and the bulk bcc solid!

cd to the folder ```1-distributions/bcc``` and run the command:
```
mpiexec lmp -in start.lmp > /dev/null &
```
Then cd to the folder ```1-distributions/liquid``` and run again the same command.
These commands will run simulations of the bulk liquid and bulk solid at 1 bar and 375 K.
I have chosen this temperature because it is close to coexistence for these phases.
The files start.lmp are the LAMMPS input and they specify that we are doing a NPT simulations.
The output of these runs are in the files log.lammps, dump.na, and out.dcd .
log.lammps is a log file that also contains some thermodynamic ouput.
dump.na is the trajectory is LAMMPS dump atom format and it is useful for visualization with [Ovito](https://www.ovito.org/).
out.dcd is the trajectory in DCD format, which is useful to postprocess directly using PLUMED's driver, as we shall see.

Once that these simulations have completed, we will compute the distributions of the environment similarity kernel using this input

```
ENVIRONMENTSIMILARITY ...
 SPECIES=1-1024
 SIGMA=replace
 CRYSTAL_STRUCTURE=BCC
 LATTICE_CONSTANTS=0.423
 LABEL=s
 MEAN
... ENVIRONMENTSIMILARITY

hh: HISTOGRAM ...
   DATA=s
   GRID_MIN=-0.5
   GRID_MAX=2
   GRID_BIN=1000
   BANDWIDTH=0.01
...

DUMPGRID GRID=hh FILE=histo
```

Here, SIGMA=replace has to be replaced by an apprpriate value. 
The action HISTOGRAM will compute the normalized histogram using all per-atom values of the kernel and the action DUMPGRID will write it to a file named histo.
We have to compute these histograms for different values of SIGMA and this can be done with the script run.sh in the folder 1-distributions (execute the command ./run.sh > results.txt).
This script will calculate the distributions and their overlaps for different SIGMA.
The overlap $O(p,q)$ between two distributions $p(x)$ and $q(x)$ can be defined in a variety of ways. Here we use,
$O(p,q) = \int dx \: min[p(x),q(x)]$

The output of the script will have two columns, the sigma value used and the overlap between the liquid and solid distributions of the kernel for that sigma.
The best choice of SIGMA will be the one that minimizes the overlap which in this case should be around 0.07 nm.
Did you get that result? Great! Then, let's move to the next section.
