import json

import customtkinter as ctk

import hanoi.interface.bottom_frame as bottom_frame
import hanoi.interface.fil_control_frame as fil_control_frame
import hanoi.interface.hanoi_canvas as hanoi_canvas
import hanoi.interface.numpad as numpad
import hanoi.interface.right_frame as right_frame 
import hanoi.logic.data as data
from hanoi.logic.state import State

class App(ctk.CTk):
  
  def __init__(self):
    super().__init__()

    self.title("Hanoi mockup")
    self.geometry("1920x1080")
    self.resizable(False, False)
    self.attributes("-fullscreen", True)
    
    self.colors = json.load(open('./hanoi/colors.json'))
    self.font_family = "Poppins"

    self.fg_color = self.colors.get("grey")
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("dark-blue")

    #grid 
    self.columnconfigure(0, weight = 0)
    self.columnconfigure(1, weight = 1)
    self.rowconfigure(0, weight = 0)
    self.rowconfigure(1, weight = 1)

    #canvas
    self.canvas = hanoi_canvas.HanoiCanvas(self, width = 1500, height = 950, bg = "#ffffff", cursor = "circle")
    self.canvas.grid(column = 0, row = 0, sticky = ctk.NSEW)

    #bottom frame
    
    self.bottom_frame = bottom_frame.BottomFrame(self, fg_color = self.colors.get("grey"))

    self.fil_control_frame = fil_control_frame.FilControlFrame(self, fg_color = self.colors.get("grey"))

    #right frame
    self.right_frame = right_frame.RightFrame(self, fg_color = self.colors.get("grey"))
    self.right_frame.grid(
      column = 1, row = 0, rowspan = 2, sticky = ctk.NSEW
    )

    # self.numpad = numpad.Numpad(self, fg_color = self.colors.get("grey"))
    # self.numpad.withdraw()
    
    self.demo_view()
    self.update_display()
    
  
  def update_display(self):
    self.right_frame.info_frame.update_display()
    self.right_frame.fil_rouge_frame.set_visiteurs(State.state + 1)
    self.bottom_frame.display_toggle.configure(
      text = ("États" if (State.move_display) else "Mouvements")
    )
    self.canvas.update_display()
  
  def demo_view(self):
    self.fil_control_frame.grid_forget()
    self.bottom_frame.stage()

    self.right_frame.demo_view()

    State.mode = "demo"
  
  def fil_rouge_view(self):
    # Arrête le mode auto s'il est activé
    if self.right_frame.auto_frame.auto_mode:
      self.right_frame.auto_frame.toggle_auto()

    self.bottom_frame.grid_forget()
    self.fil_control_frame.stage()

    self.right_frame.fil_rouge_view()

    State.mode = "fil rouge"
    State.change_disk_amount(20)

    #Préparation de l'état
    State.state_by_number(data.read_state())
    State.move_display = True
    self.update_display()

  
  def switch_view(self):
    if State.mode == "demo":
      self.fil_rouge_view()
    else:
      self.demo_view()
  
  def show_numpad(self):
    self.numpad = numpad.Numpad(self, fg_color = self.colors.get("grey"))
    self.eval(f"tk::PlaceWindow {str(self.numpad)} center")