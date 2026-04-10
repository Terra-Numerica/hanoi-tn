import tkinter.font as font
import tkinter.ttk as ttk

import customtkinter as ctk

import hanoi.interface.info_demo_subframe as demo_subframe
import hanoi.interface.info_fil_subframe as fil_subframe
from hanoi.logic.state import State
import hanoi.logic.temporality as temporality

class InfoFrame(ctk.CTkFrame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    #grid
    self.columnconfigure(0, weight = 1)
    self.rowconfigure((0,1,2,3,4), weight = 1)

    self.parent = parent
    self.colors = parent.colors
    self.font_family = parent.font_family

    #titre
    
    self.title = ctk.CTkLabel(
      self, text = "Tours de Hanoï",
      text_color = self.colors.get('dark_blue'),
      text_font = font.Font(size = 35, family = self.font_family, weight = "bold")
    )
    self.title.grid(
      column = 0, row = 0, 
    )

    #Séparateur de début

    ttk.Separator(
      self, orient = "horizontal"
    ).grid(
      column = 0, row = 1, pady = 5, sticky = ctk.EW 
    )

    #Progression (%)

    self.progress = ctk.CTkLabel(
      self,
      text_color = self.colors.get('green'),
      text_font = font.Font(size = 25, family = self.font_family)
    )
    self.progress.grid(
      column = 0, row = 2,
      pady = 5
    )

    # Contenu dépendant du mode

    ## Mode démo

    self.demo_frame = demo_subframe.InfoDemoSubframe(self)

    ## Mode fil rouge

    self.fil_frame = fil_subframe.InfoFilSubframe(self)


    #Séparateur de fin

    ttk.Separator(
      self, orient = "horizontal"
    ).grid(
      column = 0, row = 4, pady = 5, sticky = ctk.EW 
    )


    self.demo_view()
  

  def update_display(self):

    state = State.state
    
    self.progress.configure(
      text = f"Progression : { format( round(((state)/(2**(State.disk_amount) - 1))*100, 6), 'f').rstrip('0').rstrip('.') } %"
    )

    self.demo_frame.update_display()
    self.fil_frame.update_display()

    # self.main_state.configure(text = (
    #   f"Mouvement {state + 1}" if move_display else 
    #   f"État {state + 1}"
    # ))

    # self.secondary_state.configure(text = (
    #   f"(De l'État {state + 1} à l'État {state + 2})" if move_display else
    #   f"(Obtenu après {state} mouvements)"
    # ))

    # self.remaining_time.configure(text = (
    #   "Temps restant : " + temporality.render_time(temporality.remaining_time(state, State.speed))
    # ))
  
  def stage(self)-> None:
    """Fait apparaître la frame sur l'interface.
    """
    self.grid(
      column = 0, row = 1, columnspan = 2,
      sticky = ctk.NSEW
    )

  def demo_view(self)-> None: 
    """Passe à la vue du mode Démo.
    """
    # MaJ texte titre
    self.title.configure(text = "Tours de Hanoï")
    
    # Changement de frame : demo_frame
    self.fil_frame.grid_forget()
    self.demo_frame.stage()
  
  def fil_rouge_view(self)-> None:
    """Passe à la vue du mode Fil Rouge.
    """
    # MaJ texte titre
    self.title.configure(text = "Fil Rouge")

    # Changement de frame : fil_frame
    self.demo_frame.grid_forget()
    self.fil_frame.stage()