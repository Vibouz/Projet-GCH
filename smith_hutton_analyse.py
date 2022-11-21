# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import smith_hutton_corr
import pytest
try:
    from smith_hutton_fct import *
except:
    pass

#------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans smith_hutton_fct.py afin
# de résoudre le problème de Smith Hutton selon différents nombres de Péclet.
# Ensuite, les solutions devront être affichées sur des figures pour l'analyse.
#------------------------------------------------------------------------------

# Position et solutions de référence
x_p = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
s_p10 = np.array([ 1.989, 1.402, 1.146, 0.946, 0.775, 0.621, 0.480, 0.349, 0.227, 0.111, 0.000 ])
s_p100 = np.array([ 2.000, 1.940, 1.836, 1.627, 1.288, 0.869, 0.480, 0.209, 0.070, 0.017, 0.000 ])
s_p1000 = np.array([2.000, 2.000, 2.000, 1.985, 1.841, 0.951, 0.154, 0.001, 0.000, 0.000, 0.000])

# Paramètres
X = [-1,1]
Y = [0,1]

nx = 41
ny = 41

[x,y] = position(X,Y,nx,ny)

alpha = 10
Pe = [10,100,1000]
Mat = np.zeros(3)

# Résolution

Mat10 = mdf_assemblage(X,Y,nx,ny,Pe[0],alpha)
c10 = np.linalg.solve(Mat10[0],Mat10[1])
Mat100 = mdf_assemblage(X,Y,nx,ny,Pe[1],alpha)
c100 = np.linalg.solve(Mat100[0],Mat100[1])
Mat1000 = mdf_assemblage(X,Y,nx,ny,Pe[2],alpha)
c1000 = np.linalg.solve(Mat1000[0],Mat1000[1])

# Graphiques (utilisez les lignes suivantes pour générer la figure demandée)
c10_reshaped = c10.reshape(nx,ny).transpose()
c100_reshaped = c100.reshape(nx,ny).transpose()
c1000_reshaped = c1000.reshape(nx,ny).transpose()

fig,ax = plt.subplots(nrows=3,ncols=1)

fig1 = ax[0].pcolormesh(x,y, c10_reshaped)
plt.colorbar(fig1, ax=ax[0])

fig2 = ax[1].pcolormesh(x,y, c100_reshaped)
plt.colorbar(fig2, ax=ax[1])

fig3 = ax[2].pcolormesh(x,y, c1000_reshaped)
plt.colorbar(fig3, ax=ax[2])
plt.savefig("analyse",dpi=300)
plt.show()

x_exp = np.linspace(0,1,nx//2)

plt.plot(x_p,s_p10,x_p,s_p100,x_p,s_p1000,x_exp,c10_reshaped[40][20:40],x_exp,c100_reshaped[40][20:40],x_exp,c1000_reshaped[40][20:40])
plt.legend(['Référence, Pe = 10','Référence, Pe = 100','Référence, Pe = 1000','Analytique, Pe = 10','Analytique, Pe = 100','Analytique, Pe = 1000'])
plt.title("Comparaison en la référence et l'analytique")
plt.xlabel('x')
plt.ylabel('y')
plt.savefig("comparaison",dpi=300)


#%% Correction
pytest.main(['-q', '--tb=long','--disable-warnings', 'smith_hutton_corr.py'])
