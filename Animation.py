# Sous-module de matplotlib pour l'animation
from matplotlib import animation
import numpy as np
import matplotlib.pyplot as plt
# Sous-module pour afficher une animation dans un notebook, n'est pas nécessaire dans un fichier .py normal.
from IPython.display import HTML
from matplotlib.animation import FuncAnimation
try:
    from untitled1 import *
except:
    pass

# Initialiser les variables
# -------------------------------------------------------------------------------------------------
n, vec_x, vec_C, blank = init_variables()

# Initialisation de la figure et d'un systeme d'axes avec une image, une courbe et du texte
# -------------------------------------------------------------------------------------------------
fig = plt.figure(figsize=(10, 7))
ax = plt.axes()
# Définition d'un objet imshow initialement vide
im = ax.imshow(
    blank,  # Matrice de l'image
    vmin=0.0,  # Valeur minimale, utile pour la palette de couleurs
    vmax=1.0,  # Valeur maximale, " "
    cmap=plt.cm.spring,
    aspect="auto",
    extent=[0, 1, 0, 1],  # [xmin, xmax, ymin, ymax]
)
(line,) = ax.plot([], [])  # Définition d'un objet courbe initialement vide (ne pas oublier la virgule)
# Définition d'un objet texte initialement vide
txt = ax.text(0.8, 0.9, "")  # (x,y,texte)
fig.colorbar(im, ax=ax)  # Ajout d'une barre de couleur à l'axe principal
plt.close()  # Fermeture de la figure puisque qu'elle sera générée avec la fonction animation

# Note: Cette fonction est placée ici dans le code uniquement pour permettre de mieux comprendre ses différents
# éléments. Elle devrait être placée en haut normalement.
def draw_frame(i, vec_C, vec_x):
    """
    Fonction qui dessine une frame de l'animation
    Args:
        i: (obligatoire) numéro de la frame
        vec_C: vecteur des concentrations
        vec_x: vecteur des abscisses
    Returns:
        liste des objets à dessiner (obligatoire)
    """
    mat_C = [vec_C, vec_C]  # Matrice 2xN aux lignes identiques pour pouvoir afficher le vecteur comme une image
    im.set_data(mat_C)  # Modifier la matrice de l'image
    line.set_data(vec_x, vec_C)  # Modifier la courbe
    txt.set_text(f"t = {i*0.1:.1f}s")  # Afficher le temps de simulation avec 1 décimale

    # Effectuer un bond de 10 pas uniquement à partir de la 2e frame
    if i != 0:
        vec_C = fick_10pas(vec_C)

    return [im, line, txt]  # (obligatoire) retourner la liste des objets à dessiner


# Création de l'animation
# -------------------------------------------------------------------------------------------------
anim = animation.FuncAnimation(
    fig,  # Figure du graphique
    draw_frame,  # Fonction qui dessine une frame
    # 🕹️ --------------------------------------------------------------
    frames=100,  # Nombre de frames
    interval=40,  # Intervalle de temps entre chaque frame (ms): 40ms = 25fps
    # 🕹️ --------------------------------------------------------------
    fargs=(
        vec_C,
        vec_x,
    ),  # Arguments supplémentaires (en plus de i) à passer à la fonction
)

# Affichage de l'animation
# -------------------------------------------------------------------------------------------------
# Dans un notebook:
HTML(anim.to_jshtml())  # ou HTML(anim.to_html5_video())
# Dans un fichier .py normal:
# f = "animation.mp4" # Nom du fichier vidéo
# writervideo = animation.FFMpegWriter(fps=25) # Création d'un objet qui va exporter l'animation en vidéo
# anim.save(f, writer=writervideo) # Exportation