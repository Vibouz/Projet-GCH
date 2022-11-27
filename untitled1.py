import numpy as np

def fick_10pas(vec_C):
    """
    Fonction qui effectue le calcul des nouvelles concentrations 10 pas de temps plus tard.
    - dt = 0.01s
    - dx = 0.01m
    - D = 4e-3
    Args:
        vec_C: vecteur des concentrations
    Returns:
        vec_C: nouveau vecteur des concentrations
    """
    for _ in range(10):
        vec_C[1:-1] = vec_C[1:-1] + 0.4 * (vec_C[2:] - 2 * vec_C[1:-1] + vec_C[:-2])

    return vec_C


def init_variables():
    n = 100  # Nombre de noeuds du domaine 1D
    vec_x = np.linspace(0, 1, n)  # Vecteur des coordonnées des noeuds allant de 0 à 1

    # Conditions initiales de concentration
    vec_C = np.zeros(n)
    vec_C[: int(n / 2)] = 1

    # Pour pouvoir afficher le vecteur des concentrations sous forme d'un gradient de couleurs dans imshow, il faut qu'il
    # soit sous forme matricielle. Pour cela on crée une matrice 2xn avec ses 2 lignes étant le vecteur des concentrations.
    # Ici blank va servir pour initialiser le graphique.
    blank = np.zeros((2, n))
    return n, vec_x, vec_C, blank