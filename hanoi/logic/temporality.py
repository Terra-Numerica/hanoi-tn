import datetime
import math  


month_names: dict = {
  1 : "janvier",
  2 : "février",
  3 : "mars",
  4 : "avril",
  5 : "mai",
  6 : "juin",
  7 : "juillet",
  8 : "août",
  9 : "septembre",
  10 : "octobre",
  11 : "novembre",
  12 : "décembre"
}

def render_time(seconds: int)-> str:
  """Retourne une chaîne de caractère représentant le laps de temps "seconds" en jours, heures, minutes et secondes.

  Le temps à représenter sera compris entre 0s et (2**20)-1 s, soit 12j3h16min15s environ.

  Args:
      seconds (int): Le laps de temps à convertir, en secondes.

  Returns:
      str: La chaîne de caractère représentant le résultat.
  """
  values: list[int] = [0,0,0,0] #j,h,m,s
  secs: int = seconds

  if seconds == 0:
    return "Terminé !"

  #jours (60*60*24s)
  values[0] = secs // (60*60*24)
  secs = secs % (60*60*24)

  #heures (60*60s)
  values[1] = secs // (60*60)
  secs = secs % (60*60)

  #minutes (60s)
  values[2] = secs // 60
  secs = secs % 60

  #secondes
  values[3] = secs

  if values[0] != 0: #jours
    return f"{values[0]} jour{plural(values[0])} {values[1]} heure{plural(values[1])}\n{values[2]} minute{plural(values[2])} {values[3]} seconde{plural(values[3])}"
  elif values[1] != 0: #heures
    return f"{values[1]} heure{plural(values[1])}\n{values[2]} minute{plural(values[2])} {values[3]} seconde{plural(values[3])}"
  elif values[2] != 0: #minutes
    return f"\n{values[2]} minute{plural(values[2])} {values[3]} seconde{plural(values[3])}"
  else: #secondes
    return f"{values[3]} seconde{plural(values[3])}"

def plural(value: int)-> str:
  """Retourne "s" si la valeur 'value' est > 1, "" sinon.

  Args:
      value (int): La valeur à tester.

  Returns:
      str: 's' si value > 1, '' sinon. 
  """
  return 's' if value > 1 else ''


def remaining_time(state: int, speed: int, disk_amount: int)-> int:
  """Retourne le temps restant pour résoudre les tours de Hanoï, à partir de l'état courant "state" et de la vitesse sélectionnée "speed".

  Args:
      state (int): L'état courant.
      speed (int): La vitesse actuelle de l'exécution automatique.
      disk_amount (int): Le nombre de disques.

  Returns:
      int: Le nombre de secondes pour passer de l'état courant à l'état 2**20 à la vitesse 'speed' (en mouvement/s), arrondi à la seconde supérieure.
  """
  moves:int = (2**(disk_amount) - 1) - state

  return math.ceil(moves/speed)

def end_date(seconds: int)-> str:
  """Retourne une chaîne de caractères représentant la date de fin d'une opération de seconds secondes commençant maintenant.
  Si cette date est aujourd'hui, affiche "Aujourd'hui ! (HH:MM)", où HH:MM est l'heure de fin.

  Args:
      seconds (int): Le temps pris par l'opération, en secondes.

  Returns:
      str: La chaîne de caractères représentant la date de fin.
  """
  now = datetime.datetime.now()
  then = now + datetime.timedelta(seconds = seconds)

  if now.date() == then.date():
    return f"Aujourd'hui ! ({0 if then.hour < 10 else ''}{then.hour}:{0 if then.minute < 10 else ''}{then.minute})"
  else:
    return f"{then.day} {month_names[then.month]} {then.year}"