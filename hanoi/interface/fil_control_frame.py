import tkinter as tk
import tkinter.font as font

import customtkinter as ctk

from hanoi.logic.state import State

class FilControlFrame(ctk.CTkFrame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    self.parent = parent
    self.colors = parent.colors
    self.font_family = parent.font_family

    #grid
    self.columnconfigure((0,1,2,3,4), weight = 1)
    self.rowconfigure(0, weight = 1)

    self.title = ctk.CTkLabel(
      self, text = "Contrôles Fil Rouge",
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 40, family = self.font_family, weight = "bold")
    )
    self.title.grid(
      column = 2, row = 0, 
    )

  def stage(self)-> None:
    """Fait apparaître la frame sur l'interface.
    """
    self.grid(
    column = 0, row = 1, 
    padx = 88, pady = 10,
    sticky = ctk.NS
  )