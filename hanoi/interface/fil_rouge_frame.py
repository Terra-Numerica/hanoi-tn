import tkinter as tk
import tkinter.font as font

import customtkinter as ctk

import hanoi.logic.data as data
from hanoi.logic.state import State

class FilRougeFrame(ctk.CTkFrame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    #grid
    self.columnconfigure(0, weight = 5)
    self.columnconfigure(1, weight = 5)
    self.columnconfigure(2, weight = 1)
    self.rowconfigure((0,1,2,3,4), weight = 1)

    self.parent = parent
    self.colors = parent.colors
    self.font_family = parent.font_family

    # Contenu

    # Titre

    self.title = ctk.CTkLabel(
      self, text = "Fil Rouge", 
      text_font = font.Font(size = 30, family = self.font_family, weight = "bold")
    )
    self.title.grid(
      column = 0, row = 0, columnspan = 3,
      pady = 5, sticky = ctk.W
    )

    # nième visiteur #TODO améliorer placement du texte

    couleur_texte = self.colors.get("dark_blue")
    # font_texte = font.Font(size = 20, family = self.font_family)

    self.text1 = ctk.CTkLabel(
      self, text = "Vous êtes le",
      text_color = couleur_texte,
      text_font = font.Font(size = 18, family = self.font_family)
    )
    self.text1.grid(
      column = 0, row = 1,
      sticky = ctk.NS
    )

    self.visiteurs = ctk.CTkLabel(
      self, text = "Xème",
      text_color = self.colors.get("green"),
      text_font = font.Font(size = 20, family = self.font_family)
    )
    self.visiteurs.grid(
      column = 1, row = 1,
      sticky = ctk.NS
    )

    self.text2 = ctk.CTkLabel(
      self, text = "visiteur !",
      text_color = couleur_texte,
      text_font = font.Font(size = 18, family = self.font_family)
    )
    self.text2.grid(
      column = 2, row = 1,
      sticky = ctk.NS
    )

    # Paragraphe

    self.paragraph = ctk.CTkLabel(
      self, text = "Le mouvement à réaliser est représenté à l'écran.",
      text_color = couleur_texte,
      text_font = font.Font(size = 20, family = self.font_family),
      justify = ctk.CENTER
    )
    self.paragraph.bind('<Configure>', lambda e: self.paragraph.configure(wraplength = self.paragraph.winfo_width()))
    self.paragraph.grid(
      column = 0, row = 2, columnspan = 3,
      sticky = ctk.EW, pady = 15
    )

    # Boutons

    self.button = ctk.CTkButton(
      self, text = "Sauvegarder",
      command = self.save,
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 30, family = self.font_family)
    )
    self.button.grid(
      column = 0, row = 3, columnspan = 3
    )

    self.numpad_button = ctk.CTkButton(
      self, text = "Manuel",
      command = self.show_numpad,
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 20, family = self.font_family)
    )
    self.numpad_button.grid(
      column = 0, row = 4, columnspan = 3, pady = (20, 0)
    )

  def stage(self)-> None:
    """Fait apparaître la frame sur l'interface.
    """
    self.grid(
      column = 0, row = 2, columnspan = 2,
      sticky = ctk.EW
    )
  
  def set_visiteurs(self, nombre: int)-> None:
    """Change l'affichage du label "Xème visiteur" pour la valeur passée en paramètre.

    Args:
        nombre (int): Nombre de visiteurs à afficher.
    """
    self.visiteurs.configure(text = f"{nombre}ème" if nombre > 1 else f"{nombre}er")
  
  def save(self, increment = 1)->None:
    State.increment_state(increment)
    data.save_now()
    self.parent.parent.update_display()
  
  def show_numpad(self)->None:
    self.parent.parent.show_numpad()