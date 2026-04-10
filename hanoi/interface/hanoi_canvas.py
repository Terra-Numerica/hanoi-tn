import tkinter.font as font

import customtkinter as ctk

# import hanoi.logic.towers as towers
from hanoi.logic.state import State

class HanoiCanvas(ctk.CTkCanvas):

  def __init__(self, parent, couleur_disque = "black", *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.parent = parent

    #variables de configuration du rendu
    self.largeur_base = 450
    self.intervalle = 500
    self.largeur_initiale_disque = 400
    self.increment_disque = 15
    self.hauteur_disque = 38
    self.hauteur_base = 40
    self.hauteur_tour = 825
    self.largeur_tour = 20
    self.marge_inf = 0
    self.couleur_bg_texte = "white"
    
    self.couleur_disque = couleur_disque
    self.couleur_contour_disque = "white"
    self.couleur_disque_origine = "blue"
    self.couleur_contour_disque_origine = "black"
    self.couleur_disque_destination = "red"
    self.couleur_contour_disque_destination = "black"
  
  def draw_setup(self)-> None:

    for i in range(-1,2,1):
      
      #tours
      self.create_rectangle(
        ((750 + i * self.intervalle) - (self.largeur_tour / 2), 950 - self.marge_inf),
        ((750 + i * self.intervalle) + (self.largeur_tour / 2), 950 - self.marge_inf - self.hauteur_tour),
        fill = "brown"
      )

      #bases
      self.create_rectangle(
        ((750 + i * self.intervalle) - (self.largeur_base / 2), 950 - self.marge_inf), 
        ((750 + i * self.intervalle) + (self.largeur_base / 2), 950 - self.marge_inf - self.hauteur_base), 
        fill = "brown"
      )
    
  def draw_disk_shape(self, origin: tuple[int,int], largeur: int, hauteur: int, marge: int, etiquette: str, couleur: str, couleur_contour: str)-> None:
    """Dessine un disque "posé" sur le point origin (x,y), de largeur et de hauteur spécifiées.
    Coordonnées :        Axe y :
    /-------------\  <--  top
    |             +  <--  top_margin
    |             |
    |             +  <--  bottom_margin
    \-|----o----|-/  <--  bottom

    ^ ^    ^    ^ ^      Axe x :
    | |    |    | L-----  right
    | |    |    L-------  right_margin
    | |    L------------  (origin)
    | L-----------------  left_margin
    L-------------------  left

    Args:
        origin (tuple): L'origine sur lequel est posée le disque.
        largeur (int): Sa largeur.
        hauteur (int): Sa hauteur.
        marge (int): Le rayon, en px, de l'arrondi du disque.
        etiquette (str): La chaîne de caractère à afficher au centre du disque.
        couleur (str): La couleur du disque.
        couleur_contour (str): La couleur du contour du disque.
    """

    x = origin[0]
    y = origin[1]
    top = y - hauteur
    top_margin = y - hauteur + marge
    bottom_margin = y - marge
    bottom = y
    left = x - (largeur/2)
    left_margin = x - (largeur/2) + marge
    right_margin = x + (largeur/2) - marge
    right = x + (largeur/2)


    self.create_polygon(
      (left_margin, bottom), (left_margin, bottom),
      (left, bottom), #coin SW
      (left, bottom_margin), (left, bottom_margin),
      (left, top_margin), (left, top_margin),
      (left, top), #coin NW
      (left_margin, top), (left_margin, top),
      (right_margin, top), (right_margin, top),
      (right, top), #coin NE
      (right, top_margin), (right, top_margin),
      (right, bottom_margin), (right, bottom_margin),
      (right, bottom), #coin SE
      (right_margin, bottom), (right_margin, bottom),
      
      fill = couleur,
      outline = couleur_contour,
      smooth = True,
    )

    self.create_text(
      (x, y - (hauteur/2)),
      text = etiquette,
      fill = self.couleur_bg_texte,
      font = font.Font(size = int(hauteur/2))
    )

  def draw_disk(self, tower: int, height_index: int, disk_number: int, origine: bool = False, destination: bool = False)-> None:
    """Desine le disque disk_number posé sur la tour tower à la hauteur d'indice height_index.

    Args:
        tower (int): 0-2, indice de la tour sur laquelle poser le disque.
        height_index (int): indice de hauteur où poser le disque, où 0 correspond au disque posé sur la base de la tour, 1 le disque posé sur un autre disque, etc.
        disk_number (int): Indice du disque, détermine sa taille et son étiquette.
        origine (bool, optional): Indique si le disque est le disque d'origine d'un mouvement. Defaults to False.
        destination (bool, optional): Indique si le disque est le disque de destination d'un mouvement. Defaults to False.
    """
    if origine:
      couleur = self.couleur_disque_origine
      couleur_contour = self.couleur_contour_disque_origine
    elif destination:
      couleur = self.couleur_disque_destination
      couleur_contour = self.couleur_contour_disque_destination
    else:
      couleur = self.couleur_disque
      couleur_contour = self.couleur_contour_disque

    self.draw_disk_shape(
      (750 + self.intervalle * (tower - 1), 950 - self.marge_inf - self.hauteur_base - height_index * self.hauteur_disque),
      self.largeur_initiale_disque - self.increment_disque * (20 - disk_number),
      self.hauteur_disque,
      self.hauteur_disque / 2,
      str(disk_number),
      couleur, couleur_contour
    )
    pass

  def draw_state(self, towers: list[list[int]])-> None:
    """Dessine l'état représenté par towers.

    Args:
        towers (list[list[int]]): La représentation de l'état à afficher.
    """
    for tower in range(3):
      for i in range(len(towers[tower])):
        self.draw_disk(tower, i, towers[tower][i])
  
  def draw_move(self, towers: list[list[int]], move: tuple[int, int])-> None:
    """Dessine le mouvement d'une pièce décrit par move à partir de l'état initial décrit par towers.
    Si le state actuel est le dernier (2**20 - 1), afficher le dernier état.

    Args:
        towers (list[list[int]]): La représentation de l'état initial.
        move (tuple[int, int]): La représentation du mouvement à afficher, sous la forme (origine, destination) avec les indices des tours (0,1,2).
    """
    if move == None:
      
      self.draw_state(towers)
    
    else:

      for tower in range(3):
        for i in range(len(towers[tower])):
          self.draw_disk(tower, i, towers[tower][i], 
            origine = (tower == move[0]) and (i == len(towers[tower]) - 1) #origine
          )
      
      # destination
      self.draw_disk(move[1], len(towers[move[1]]), towers[move[0]][len(towers[move[0]]) - 1], destination = True)

      self.draw_arrow(*move)
  
  def draw_arrow(self, origine: int, destination: int)-> None:
    """Dessine une flèche allant de la tour d'indice origine vers la tour d'indice destination.

    Args:
        origine (int): L'indice de la tour d'origine de la flèche.
        destination (int): L'indice de la tour de destination de la flèche.
    """
    #hauteur de la flèche
    hauteur = 100
    #decalage entre 2 tours
    intervalle = self.intervalle
    #coordonnée y du haut de la plus grande tour possible
    top = 950 - self.marge_inf - 1.01 * self.hauteur_tour

    #départ/arrivée : coordonnée x des tours correspondantes
    coords = [750 + i * intervalle for i in [-1, 0, 1]]
    (depart, arrivee) = (coords[origine], coords[destination])

    self.create_line(
      (depart, top),
      (depart, top - hauteur),
      (arrivee, top - hauteur),
      (arrivee, top),
      width = 10,
      arrow = ctk.LAST, arrowshape = (24, 30, 9),
      smooth = True
    )
  

  def update_display(self)-> None:
    self.delete("all")
    self.draw_setup()
    if State.move_display:
      self.draw_move(State.towers_state, State.move)
      # self.draw_move(*towers.current_state_and_move(20))
    else:
      self.draw_state(State.towers_state)
      # self.draw_state(towers.current_state(20))