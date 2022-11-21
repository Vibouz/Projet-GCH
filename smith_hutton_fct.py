# Importation des modules
import numpy as np

def position(X,Y,nx,ny):
    """ Fonction générant deux matrices de discrétisation de l'espace

    Entrées:
        - X : Bornes du domaine en x, X = [x_min, x_max]
        - Y : Bornes du domaine en y, Y = [y_min, y_max]
        - nx : Discrétisation de l'espace en x (nombre de points)
        - ny : Discrétisation de l'espace en y (nombre de points)

    Sorties (dans l'ordre énuméré ci-bas):
        - x : Matrice (array) de dimension (ny x nx) qui contient la position en x
        - y : Matrice (array) de dimension (ny x nx) qui contient la position en y
            * Exemple d'une matrice position :
            * Si X = [-1, 1] et Y = [0, 1]
            * Avec nx = 3 et ny = 3
                x = [-1    0    1]
                    [-1    0    1]
                    [-1    0    1]

                y = [1    1    1  ]
                    [0.5  0.5  0.5]
                    [0    0    0  ]
    """

    x = np.zeros([ny,nx])
    y = np.zeros([ny,nx])
    
    x[:] = np.linspace(X[0],X[1],nx)
    y = np.transpose(y)
    y[:] = np.linspace(Y[1],Y[0],ny)
    y = np.transpose(y)

    return x,y

def vitesse(x,y):
    """ Fonction donnant les vitesses en x et y selon la position

    Entrées:
        - x : Matrice de dimension (ny x nx) qui contient la position en x
        - y : Matrice de dimension (ny x nx) qui contient la position en y

    Sorties (dans l'ordre énuméré ci-bas):
        - u : Matrice (array) de dimension (ny x nx) qui contient la vitesse en x
        - v : Matrice (array) de dimension (ny x nx) qui contient la vitesse en y

    """

    u = 2*y*(1-x**2)
    v = -2*x*(1-y**2)

    return u,v

def mdf_assemblage(X,Y,nx,ny,Pe,alpha):
    """ Fonction assemblant la matrice A et le vecteur b

    Entrées:
        - X : Bornes du domaine en x, X = [x_min, x_max]
        - Y : Bornes du domaine en y, Y = [y_min, y_max]
        - nx : Discrétisation de l'espace en x (nombre de points)
        - ny : Discrétisation de l'espace en y (nombre de points)
        - Pe : Nombre de Péclet
        - alpha : Constante des conditions de Dirichlet sur les frontières

    Sorties (dans l'ordre énuméré ci-bas):
        - A : Matrice (array)
        - b : Vecteur (array)
    """
    
    [x,y] = position(X,Y,nx,ny)

    dx = (X[1]-X[0])/(nx-1)
    dy = (Y[1]-Y[0])/(ny-1)
    
    N = nx*ny

    A = np.zeros([N,N])
    b = np.zeros(N)
    [u_x,u_y] = vitesse(x,y)


    # conditions bas milieu droit - good
    j = ny-1
    for i in range(nx//2+1,nx):
        k = i*ny + j
        A[k,k] = 3
        A[k,k-1] = -4
        A[k,k-2] = 1
        b[k] = 0

    # conditions bas milieu gauche - good
    j = ny-1
    for i in range(0,nx//2+1):
        k = i*ny + j
        A[k,k] = 1
        b[k] = 1 + np.tanh(alpha*(2*x[j][i] + 1))   
        
    # conditions de gauche - 
    i = 0
    for j in range(0,ny):
        k = i*ny + j
        A[k,k] = 1
        A[k,k-1] = 0
        A[k,k-2] = 0
        b[k] = 1 - np.tanh(alpha)
        
    # conditions de haut - good
    j = 0
    for i in range(0,nx):
        k = i*ny + j
        A[k,k] = 1
        A[k,k-1] = 0
        A[k,k-2] = 0
        b[k] = 1 - np.tanh(alpha)   
        
    # conditions de droite - good
    i = nx-1
    for j in range(0,ny):
        k = i*ny + j
        A[k,k] = 1
        A[k,k-1] = 0
        A[k,k-2] = 0
        b[k] = 1 - np.tanh(alpha)   

    # coeur de la matrice - good
    for i in range (1,nx-1):
        for j in range(1,ny-1):
            k = i*ny + j
            A[k,k] = 2/(Pe*(dx**2)) + 2/(Pe*dy**2)
            A[k,k+1] = (-u_y[j][i]/(2*dy)) - (1/(Pe*(dy**2)))
            A[k,k-1] = (u_y[j][i]/(2*dy)) - (1/(Pe*(dy**2)))
            A[k,k+ny] = (u_x[j][i]/(2*dx)) - (1/(Pe*(dx**2)))
            A[k,k-ny] = (-u_x[j][i]/(2*dx)) - (1/(Pe*(dx**2)))
            b[k] = 0

    return A,b
