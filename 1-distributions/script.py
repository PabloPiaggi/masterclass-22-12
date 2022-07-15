# This python scripts computes the overlap between two distributions

data1=np.genfromtxt("bcc/histo")
data2=np.genfromtxt("liquid/histo")
print(np.trapz(np.minimum(data1[:,1],data2[:,1]),x=data1[:,0]))

