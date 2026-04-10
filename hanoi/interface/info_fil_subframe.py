import tkinter.font as font
import tkinter.ttk as ttk

import customtkinter as ctk

from hanoi.logic.state import State
import hanoi.logic.temporality as temporality

class InfoFilSubframe(ctk.CTkFrame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    #grid
    self.columnconfigure(0, weight = 1)
    self.rowconfigure((0,1,2,3,4,5,6,7,8), weight = 1)

    self.parent = parent
    self.colors = parent.colors
    self.font_family = parent.font_family

    # Contenu

    # Label Temps Restant

    self.label_title = ctk.CTkLabel(
      self, text = "Date de fin au rythme de...",
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 18, family = self.font_family, weight = "bold")
    )
    self.label_title.grid(
      column = 0, row = 0, pady = 10
    )

    # Estimations 


    # 1v/s

    # Label

    self.label_second = ctk.CTkLabel(
      self, text = "1 visiteur par seconde (86 400/j) :",
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 18, family = self.font_family)
    )
    self.label_second.grid(
      column = 0, row = 1, sticky = ctk.W
    )

    # Résultat

    self.result_second = ctk.CTkLabel(
      self, text = "default s",
      text_color = self.colors.get("dark_red"),
      text_font = font.Font(size = 20, family = self.font_family)
    )
    self.result_second.grid(
      column = 0, row = 2, sticky = ctk.EW, pady = 5
    )


    # 1v/m

    # Label

    self.label_minute = ctk.CTkLabel(
      self, text = "1 visiteur par minute (1 440/j) :",
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 18, family = self.font_family)
    )
    self.label_minute.grid(
      column = 0, row = 3, sticky = ctk.W
    )

    # Résultat

    self.result_minute = ctk.CTkLabel(
      self, text = "default m",
      text_color = self.colors.get("dark_red"),
      text_font = font.Font(size = 20, family = self.font_family)
    )
    self.result_minute.grid(
      column = 0, row = 4, sticky = ctk.EW, pady = 5
    )


    # 1v/h

    # Label

    self.label_hour = ctk.CTkLabel(
      self, text = "1 visiteur par heure (24/j) :",
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 18, family = self.font_family)
    )
    self.label_hour.grid(
      column = 0, row = 5, sticky = ctk.W
    )

    # Résultat

    self.result_hour = ctk.CTkLabel(
      self, text = "default h",
      text_color = self.colors.get("dark_red"),
      text_font = font.Font(size = 20, family = self.font_family)
    )
    self.result_hour.grid(
      column = 0, row = 6, sticky = ctk.EW, pady = 5
    )


    # 1v/j

    # Label

    self.label_day = ctk.CTkLabel(
      self, text = "1 visiteur par jour :",
      text_color = self.colors.get("dark_blue"),
      text_font = font.Font(size = 18, family = self.font_family)
    )
    self.label_day.grid(
      column = 0, row = 7, sticky = ctk.W
    )

    # Résultat

    self.result_day = ctk.CTkLabel(
      self, text = "default j",
      text_color = self.colors.get("dark_red"),
      text_font = font.Font(size = 20, family = self.font_family)
    )
    self.result_day.grid(
      column = 0, row = 8, sticky = ctk.EW, pady = 5
    )

    self.update_display()

  
  def update_display(self):

    state = State.state

    self.result_second.configure(text = temporality.end_date(temporality.remaining_time(state, 1, State.disk_amount)))
    self.result_minute.configure(text = temporality.end_date(temporality.remaining_time(state, 1/60, State.disk_amount)))
    self.result_hour.configure(text = temporality.end_date(temporality.remaining_time(state, 1/(60*60), State.disk_amount)))
    self.result_day.configure(text = temporality.end_date(temporality.remaining_time(state, 1/(60*60*24), State.disk_amount)))
  
  def stage(self)-> None:
    """Fait apparaître la frame sur l'interface.
    """
    self.grid(
      column = 0, row = 3, columnspan = 2,
      sticky = ctk.NSEW
    )