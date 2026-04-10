import tkinter.font as font
import tkinter.ttk as ttk

import customtkinter as ctk

from hanoi.logic.state import State
import hanoi.logic.temporality as temporality

class InfoDemoSubframe(ctk.CTkFrame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    #grid
    self.columnconfigure(0, weight = 1)
    self.rowconfigure((0,1,2), weight = 1)

    self.parent = parent
    self.colors = parent.colors
    self.font_family = parent.font_family

    # Contenu

    # État/mouvement principal

    self.main_state = ctk.CTkLabel(
      self,
      text_color = self.colors.get('dark_blue'),
      text_font = font.Font(size = 18, family = self.font_family), 
    )
    self.main_state.grid(
      column = 0, row = 3
    )

    # État/mouvement secondaire

    self.secondary_state = ctk.CTkLabel(
      self,
      text_color = self.colors.get('dark_blue'),
      text_font = font.Font(size = 18, family = self.font_family)
    )
    self.secondary_state.grid(
      column = 0, row = 4
    )

    # Temps restant

    self.remaining_time = ctk.CTkLabel(
      self,
      text_color = self.colors.get('dark_blue'),
      text_font = font.Font(size = 18, family = self.font_family)
    )
    self.remaining_time.grid(
      column = 0, row = 5,
      pady = 20
    )
  
  def update_display(self):

    state = State.state
    move_display = State.move_display

    self.main_state.configure(text = (
      f"Mouvement {state + 1}" if move_display else 
      f"État {state + 1}"
    ))

    self.secondary_state.configure(text = (
      f"(De l'État {state + 1} à l'État {state + 2})" if move_display else
      f"(Obtenu après {state} mouvements)"
    ))

    self.remaining_time.configure(text = (
      "Temps restant : " + temporality.render_time(temporality.remaining_time(state, State.speed, State.disk_amount))
    ))
  
  def stage(self)-> None:
    """Fait apparaître la frame sur l'interface.
    """
    self.grid(
      column = 0, row = 3, columnspan = 2,
      sticky = ctk.NSEW
    )