import tkinter.font as font
import customtkinter as ctk


class Numpad(ctk.CTkToplevel):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    self.title("Numpad")
    #self.resizable(False, False) #TODO
    self.attributes("-topmost", True)
    
    self.parent = parent
    self.colors = parent.colors
    self.font_family = parent.font_family

    self.unlocked = False


    #Contenu

    # self.title = ctk.CTkLabel(
    #   self, text = "Numpad",
    #   text_color = self.colors.get("dark_blue"),
    #   text_font = font.Font(size = 40, family = self.font_family, weight = "bold")
    # )
    # self.title.grid(
    #   column = 0, row = 0, columnspan = 3
    # )

    self.entry = ctk.CTkEntry(
      self, placeholder_text = "Code",
      text_font = font.Font(size = 30),
      text_color = self.colors.get("dark_blue"),
      justify = ctk.CENTER
    )
    self.entry.grid(
      column = 0, row = 0, columnspan = 2, sticky = ctk.EW
    )

    self.del_button = ctk.CTkButton(
      self, text = "Clear",
      text_font = font.Font(size = 30),
      text_color = self.colors.get("dark_blue"),
      command = lambda: self.entry.delete(0, len(self.entry.get())),
      width = 100, height = 50
    )
    self.del_button.grid(
      column = 2, row = 0, padx = 10, pady = 10
    )


    for c in range(3):
      for r in range(3):
        ctk.CTkButton(
          self, text = str(r*3+c+1),
          text_font = font.Font(size = 30),
          text_color = self.colors.get("dark_blue"),
          command = lambda x = str(r*3+c+1): self.add(x),
          width = 100, height = 100
        ).grid(column = c, row = r+1, padx = 10, pady = 10)
    
    ctk.CTkButton(
      self, text = "0",
      text_font = font.Font(size = 30),
      text_color = self.colors.get("dark_blue"),
      command = lambda : self.add("0"),
      width = 100, height = 100
    ).grid(column = 1, row = 4, padx = 10, pady = 10)

    self.confirm_button = ctk.CTkButton(
      self, text = "OK",
      text_font = font.Font(size = 30),
      text_color = self.colors.get("dark_blue"),
      command = self.check,
      width = 100, height = 100
    )
    self.confirm_button.grid(
      column = 2, row = 4, padx = 10, pady = 10
    )

    self.minus_button = ctk.CTkButton(
      self, text = "-",
      text_font = font.Font(size = 30),
      text_color = self.colors.get("dark_blue"),
      command = lambda: self.add("-"),
      width = 100, height = 100
    )
    self.minus_button.grid(
      column = 0, row = 4, padx = 10, pady = 10
    )
  
  
  def hide(self):
    self.withdraw()
    self.after(1000, self.deiconify)
  
  def add(self, car)->None:
    if car == "-":
      self.entry.delete(0, len(self.entry.get()))
    elif not self.entry.get().strip("-").isnumeric() and not self.entry.get() == "-":
      self.entry.delete(0, len(self.entry.get()))
    self.entry.insert(len(self.entry.get()), car)
  
  def check(self)->None:
    if not self.unlocked:
      if self.entry.get() == "2468":
        self.entry.delete(0, len(self.entry.get()))
        self.unlocked = True
        self.entry.insert(0, "Débloqué !")
      else:
        self.entry.delete(0, len(self.entry.get()))
        self.entry.insert(0, "Code faux !")
    else:
      if not self.entry.get().strip("-").isnumeric():
        self.entry.delete(0, len(self.entry.get()))
        self.entry.insert(0, "Invalide !")
      else:
        input = int(self.entry.get())
        self.entry.delete(0, len(self.entry.get()))
        self.parent.right_frame.fil_rouge_frame.save(input)
        self.entry.insert(0, "Sauvegardé !")