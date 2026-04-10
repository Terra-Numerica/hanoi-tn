import os
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk

import customtkinter as ctk

from hanoi.logic.state import State

class AutoFrame(ctk.CTkFrame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    #grid
    self.columnconfigure(0, weight = 1)
    self.columnconfigure(1, weight = 3)
    self.rowconfigure((0,1,2,3,4), weight = 1)

    self.parent = parent
    self.colors = parent.colors
    self.font_family = parent.font_family
    
    self.auto_mode = False
    self.identifier = "" #identifiant du callback en cours
    self.steps = { #speed : (delay, step)
      1 : (1000, 1),
      10 : (100, 1),
      100 : (100, 10),
      1000 : (100, 100)
    }

    self.play_icon = tk.PhotoImage(
      file = os.path.join(os.path.dirname(__file__), "..", "assets", "right.png")
    ).subsample(2)

    # Contenu

    # Titre
    self.title = ctk.CTkLabel(
      self, text = "Mode automatique",
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 25, family = self.font_family, weight = "bold")
    )
    self.title.grid(
      column = 0, row = 0, columnspan = 2, pady = 5
    )

    self.auto_button = ctk.CTkButton(
      self, 
      text = "Lancer", 
      image = self.play_icon,
      fg_color = self.colors.get("blue"),
      hover_color = self.colors.get("blue_hover"),
      text_font = font.Font(size = 25, family = self.font_family),
      command = self.toggle_auto
    )
    self.auto_button.grid(
      column = 0, row = 1, columnspan = 2, pady = 25
    )

    self.speed_readout = ctk.CTkLabel(
      self, 
      # textvariable = state.State.speed,
      text = State.speed,
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 25, family = self.font_family)
    )
    self.speed_readout.grid(
      column = 0, row = 2, sticky = ctk.E
    )

    self.speed_unit = ctk.CTkLabel(
      self, text = "mouvement/s",
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 25, family = self.font_family)
    )
    self.speed_unit.grid(
      column = 1, row = 2, sticky = ctk.W
    )

    self.speed_slider = ctk.CTkSlider(
      self,
      button_color = self.colors.get("blue"),
      button_hover_color = self.colors.get("blue_hover"),
      progress_color = self.colors.get("dark_blue"),
      fg_color = self.colors.get("light_blue"),
      width = 400, height = 35,
      from_ = 0, to = 3, number_of_steps = 3,
      command = self.update_speed
    )
    self.speed_slider.set(0)
    self.speed_slider.grid(
      column = 0, row = 3, columnspan = 2
    )

    ttk.Separator(
      self, orient = "horizontal"
    ).grid(
      column = 0, row = 4, pady = 5, columnspan = 2, sticky = ctk.EW 
    )

    # self.separator2 = ctk.CTkLabel(
    #   self, text = "--------------------------------------------",
    #   text_font = font.Font(size = 15, family = self.font_family),
    #   text_color = self.colors.get("dark_blue")
    # ).grid(column = 0, row = 5, pady = 15, columnspan = 2)
  
  def update_speed(self, value):
    State.speed = int(10**value)
    self.speed_readout.configure(text = str(State.speed))
    self.parent.parent.update_display()

  def toggle_auto(self):
    self.auto_mode = not self.auto_mode
    self.auto_button.configure(text = "Arrêter" if self.auto_mode else "Lancer")
    #TODO : toggle icon
    if self.auto_mode is True:
      self.auto_run()
    elif self.identifier != "":
      self.after_cancel(self.identifier)
      self.identifier = ""

  def auto_run(self):
    speed:int = State.speed
    if self.auto_mode:
      State.increment_state(self.steps[speed][1])
      self.parent.parent.update_display()
      if State.is_end_state():
        self.toggle_auto()
      else:
        self.identifier = self.after(self.steps[speed][0], self.auto_run)
  
  def stage(self)-> None:
    """Fait apparaître la frame sur l'interface.
    """
    self.grid(
      column = 0, row = 2, columnspan = 2,
      sticky = ctk.EW
    )
