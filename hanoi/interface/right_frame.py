import os
import tkinter as tk
import tkinter.font as font

import customtkinter as ctk

import hanoi.interface.auto_frame as auto_frame
import hanoi.interface.fil_rouge_frame as fil_rouge_frame
import hanoi.interface.info_frame as info_frame
from hanoi.logic.state import State
import hanoi.logic.data as data

class RightFrame(ctk.CTkFrame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    self.columnconfigure((0,1), weight = 1)
    self.rowconfigure((0,1,2,3), weight = 1)

    self.parent = parent
    self.colors = parent.colors
    self.font_family = parent.font_family

    self.cross_icon = tk.PhotoImage(
      file = os.path.join(os.path.dirname(__file__), "..", "assets", "cross.png"),
    ).subsample(3)
    self.larger_icon = tk.PhotoImage(
      file = os.path.join(os.path.dirname(__file__), "..", "assets", "larger.png"),
    ).subsample(3)
    self.smaller_icon = tk.PhotoImage(
      file = os.path.join(os.path.dirname(__file__), "..", "assets", "smaller.png"),
    ).subsample(3)

    #Boutons fenêtre

    self.window_button = ctk.CTkButton(
      self, text = "",
      corner_radius = 15,
      fg_color = self.colors.get("cyan"),
      hover_color = self.colors.get("dark_cyan"),
      image = self.smaller_icon if self.parent.attributes("-fullscreen") else self.larger_icon,
      command = self.toggle_window
    )
    self.window_button.grid(
      column = 0, row = 0, 
      sticky = ctk.E + ctk.N, 
      padx = 15, pady = 10
    )

    self.quit_button = ctk.CTkButton(
      self, text = "",
      corner_radius = 15,
      fg_color = self.colors.get("red"),
      hover_color = self.colors.get("dark_red"),
      image = self.cross_icon,
      command = exit
    )
    self.quit_button.grid(
      column = 1, row = 0,
      sticky = ctk.W + ctk.N, 
      padx = 15, pady = 10
    )

    #Info frame

    self.info_frame = info_frame.InfoFrame(self, fg_color = self.colors.get("grey"))
    self.info_frame.stage()

    #Frame dépendant du mode

    #Mode Démo

    self.auto_frame = auto_frame.AutoFrame(self, fg_color = self.colors.get("grey"))

    #Mode Fil rouge

    self.fil_rouge_frame = fil_rouge_frame.FilRougeFrame(self, fg_color = self.colors.get("grey"))
    

    #Switch mode

    ####################
    self.mode_switch = ctk.CTkButton(
      self, text = "Fil Rouge",
      text_font = font.Font(size = 30),
      text_color = self.colors.get("dark_blue"),
      command = self.parent.switch_view
    )
    self.mode_switch.grid(
      column = 0, row = 3, 
      columnspan = 2,
      pady = (10,50),
      sticky = ctk.S
    )
    ####################

    #Disk amount

    self.disk_less = ctk.CTkButton(
      self, text = "-1",
      text_font = font.Font(size = 20),
      text_color = self.colors.get("dark_blue"),
      command = self.remove_disk
    )
    self.disk_less.grid(
      column = 0, row = 4,
      pady = 5, padx = 5,
      sticky = ctk.N + ctk.E
    )

    self.disk_more = ctk.CTkButton(
      self, text = "+1",
      text_font = font.Font(size = 20),
      text_color = self.colors.get("dark_blue"),
      command = self.add_disk
    )
    self.disk_more.grid(
      column = 1, row = 4,
      pady = 5, padx = 5,
      sticky = ctk.N + ctk.W
    )


  
  def add_disk(self):
    State.increment_disk_amount(1)
    self.parent.update_display()
    self.parent.bottom_frame.update_buttons()

  def remove_disk(self):
    State.increment_disk_amount(-1)
    self.parent.update_display()
    self.parent.bottom_frame.update_buttons()
  
  def toggle_window(self):
    if self.parent.attributes("-fullscreen") == True:
      self.parent.attributes("-fullscreen", False)
      self.window_button.configure(image = self.larger_icon)
    else:
      self.parent.attributes("-fullscreen", True)
      self.window_button.configure(image = self.smaller_icon)
  
  def demo_view(self)-> None: 
    """Passe à la vue du mode Démo.
    """
    #Changement de frame : auto_frame
    self.fil_rouge_frame.grid_forget()
    self.auto_frame.stage()

    #MaJ texte de mode_switch
    self.mode_switch.configure(text = "Fil Rouge")

    #Changement de vue de info_frame
    self.info_frame.demo_view()

    #Réinitialisation de l'état
    State.start_state()
    State.move_display = False
    self.parent.update_display()
  
  def fil_rouge_view(self)-> None:
    """Passe à la vue du mode Fil Rouge.
    """
    #Changement de frame : fil_rouge_frame
    self.auto_frame.grid_forget()
    self.fil_rouge_frame.stage()

    #MaJ texte de mode_switch
    self.mode_switch.configure(text = "Démo")
    
    #Changement de vue de info_frame
    self.info_frame.fil_rouge_view()