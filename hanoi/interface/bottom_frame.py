import os
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk

import customtkinter as ctk

from hanoi.logic.state import State
# from hanoi.app import App

class BottomFrame(ctk.CTkFrame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    self.parent = parent
    self.colors = parent.colors
    self.font_family = parent.font_family

    # Assets

    self.rewind_icon = tk.PhotoImage(
      file = os.path.join(os.path.dirname(__file__), "..", "assets", "rewind.png")
    ).subsample(3)
    self.previous_icon = tk.PhotoImage(
      file = os.path.join(os.path.dirname(__file__), "..", "assets", "previous.png")
    ).subsample(2)
    self.next_icon = tk.PhotoImage(
      file = os.path.join(os.path.dirname(__file__), "..", "assets", "next.png")
    ).subsample(2)
    self.forward_icon = tk.PhotoImage(
      file = os.path.join(os.path.dirname(__file__), "..", "assets", "fastForward.png")
    ).subsample(3)

    #grid
    self.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14), weight = 1)
    self.rowconfigure((0,1,2,3), weight = 1)

    # Contenu

    #bouton <
    self.back_button = ctk.CTkButton(
      self,
      text = "",
      fg_color = self.colors.get("blue"),
      hover_color = self.colors.get("blue_hover"),
      image = self.previous_icon,
      command = lambda: self.increment_state(-1)
    )
    self.back_button.grid(
      column = 1, row = 0, rowspan = 3, sticky = ctk.NSEW, padx = 5, pady = 2, ipady = 5
    )

    #bouton >
    self.forward_button = ctk.CTkButton(
      self,
      text = "",
      fg_color = self.colors.get("blue"),
      hover_color = self.colors.get("blue_hover"),
      image = self.next_icon,
      command = lambda: self.increment_state(1)
    )
    self.forward_button.grid(
      column = 2, row = 0, rowspan = 3, sticky = ctk.NSEW, padx = 5, pady = 2, ipady = 5
    )

    #bouton <<
    self.beginning_button = ctk.CTkButton(
      self,
      text = "",
      fg_color = self.colors.get("blue"),
      hover_color = self.colors.get("blue_hover"),
      image = self.rewind_icon,
      command = self.start_state
    )
    self.beginning_button.grid(
      column = 1, row = 3, sticky = ctk.NSEW, padx = 5, pady = 2
    )

    #bouton >>
    self.end_button = ctk.CTkButton(
      self,
      text = "",
      fg_color = self.colors.get("blue"),
      hover_color = self.colors.get("blue_hover"),
      image = self.forward_icon,
      command = self.end_state
    )
    self.end_button.grid(
      column = 2, row = 3, sticky = ctk.NSEW, padx = 5, pady = 2
    )

    #toggle état/mouvement
    self.display_toggle = ctk.CTkButton(
      self, width = 205,
      text = "Mouvements",
      fg_color = self.colors.get("blue"),
      hover_color = self.colors.get("blue_hover"),
      text_font = font.Font(size = 25, family = self.font_family),
      command = self.toggle_display,
    )
    self.display_toggle.grid(
      column = 0, row = 0, rowspan = 4, sticky = ctk.NSEW, padx = 5, pady = 5
    )

    ttk.Separator(self, orient="vertical").grid(
      column = 3, row = 0, rowspan = 4, sticky = ctk.NS, padx = 20
    )

    # Boutons puissances de 10

    for i in range(1,5):
      
      # boutons - 10^i

      val = -10**i
      ctk.CTkButton(
        self,
        text = str(val), width = 20,
        text_font = font.Font(size = 25, family = self.font_family),
        fg_color = self.colors.get("blue"),
        hover_color = self.colors.get("blue_hover"),
        command = lambda val=val: self.increment_state(val)
      ).grid(
        column = 8-i, row = 0, rowspan = 2, sticky = ctk.NSEW, padx = 5, pady = (2, 7)
      )

      # boutons 10^i

      val = 10**i
      ctk.CTkButton(
        self,
        text = str(val), width = 20,
        text_font = font.Font(size = 25, family = self.font_family),
        fg_color = self.colors.get("blue"),
        hover_color = self.colors.get("blue_hover"),
        command = lambda val=val: self.increment_state(val)
      ).grid(
        column = 8+i, row = 0, rowspan = 2, sticky = ctk.NSEW, padx = 5, pady = (2, 7)
      )

    # label 10^n
    
    ctk.CTkLabel(
      self, text = "10ⁿ",
      text_font = font.Font(size = 30),
      text_color = self.colors.get("dark_blue"),
      width = 30, height = 30
    ).grid(
      column = 8, row = 0, rowspan = 2, sticky = ctk.NSEW, padx = 10
    )

    # Boutons puissances de 2

    for i in range(1,4):

      # boutons - 2^(n-1)
      
      val = -(2**(i+1) - 1)
      ctk.CTkButton( # -
        self,
        text = str(val), width = 20,
        text_font = font.Font(size = 25, family = self.font_family),
        fg_color = self.colors.get("blue"),
        hover_color = self.colors.get("blue_hover"),
        command = lambda val=val: self.increment_state(val)
      ).grid(
        column = 8-i, row = 2, rowspan = 2, sticky = ctk.NSEW, padx = 5, pady = (7, 2)
      )

      # boutons 2^(n-1)

      val = 2**(i+1) - 1
      ctk.CTkButton( # +
        self,
        text = str(val), width = 20,
        text_font = font.Font(size = 25, family = self.font_family),
        fg_color = self.colors.get("blue"),
        hover_color = self.colors.get("blue_hover"),
        command = lambda val=val: self.increment_state(val)
      ).grid(
        column = 8+i, row = 2, rowspan = 2, sticky = ctk.NSEW, padx = 5, pady = (7, 2)
      )
    
    #### boutons max pour update
    
    self.button_minus_two = None
    self.button_plus_two = None
    self.update_buttons()
    
    # label 2^n - 1

    ctk.CTkLabel(
      self, text = "2ⁿ-1",
      text_font = font.Font(size = 30),
      text_color = self.colors.get("dark_blue"),
      width = 30, height = 30
    ).grid(
      column = 8, row = 2, rowspan = 2, sticky = ctk.NSEW, padx = 10
    )

  
  def increment_state(self, increment:int):
    State.increment_state(increment)
    self.parent.update_display()

  def start_state(self):
    State.start_state()
    self.parent.update_display()

  def end_state(self):
    State.end_state()
    self.parent.update_display()

  def toggle_display(self):
    State.move_display = not State.move_display
    self.parent.update_display()

  def stage(self)-> None:
    """Fait apparaître la frame sur l'interface.
    """
    self.grid(
    column = 0, row = 1, 
    padx = 0, pady = 0,
    sticky = ctk.NSEW
  )

  def update_buttons(self):

    if self.button_minus_two != None:
      self.button_minus_two.grid_forget()
    if self.button_plus_two != None:
      self.button_plus_two.grid_forget()
      
    val = -(2**((State.disk_amount - 2) + 1) - 1)
    self.button_minus_two = ctk.CTkButton( # -
      self,
      text = str(val), width = 20,
      text_font = font.Font(size = 25, family = self.font_family),
      fg_color = self.colors.get("blue"),
      hover_color = self.colors.get("blue_hover"),
      command = lambda val=val: self.increment_state(val)
    )
    self.button_minus_two.grid(
      column = 4, row = 2, rowspan = 2, sticky = ctk.NSEW, padx = 5, pady = (7, 2)
    )

    val = 2**((State.disk_amount - 2) + 1) - 1
    self.button_plus_two = ctk.CTkButton( # +
      self,
      text = str(val), width = 20,
      text_font = font.Font(size = 25, family = self.font_family),
      fg_color = self.colors.get("blue"),
      hover_color = self.colors.get("blue_hover"),
      command = lambda val=val: self.increment_state(val)
    )
    self.button_plus_two.grid(
      column = 12, row = 2, rowspan = 2, sticky = ctk.NSEW, padx = 5, pady = (7, 2)
    )