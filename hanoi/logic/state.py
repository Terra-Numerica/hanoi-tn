import hanoi.logic.towers as towers

class State():

  #État initial : 20 disques, premier état, affichage en états, vitesse 1

  #Indice d'état : 0 (state 1) to 2**20 - 1 = 1 048 575 (state 2**20)
  state: int = 0
  #Nombre de disques
  disk_amount: int = 20
  #Affichage en mode mouvement ?
  move_display: bool = False
  #Représentation des tours à l'état actuel
  towers_state: list[list[int]] = towers.edge_state(disk_amount)
  #Prochain mouvement, ou None si l'état est le dernier possible
  move: tuple[int, int] = towers.compute_next_move(disk_amount, state, towers_state)
  #Vitesse de mouvement actuelle (mouvement/s)
  speed: int = 1
  #Mode du logiciel
  mode: str = ""

  @classmethod
  def change_disk_amount(cls, disk_amount: int)-> None:
    cls.disk_amount = disk_amount
    cls.start_state()
  
  @classmethod
  def increment_disk_amount(cls, increment: int)-> None:
    new_amount = cls.disk_amount + increment
    if new_amount > 20:
      new_amount = 20
    elif new_amount < 2:
      new_amount = 2
    cls.disk_amount = new_amount
    cls.start_state()

  @classmethod
  def start_state(cls)-> None:
    #ok
    cls.state = 0
    cls.towers_state = towers.edge_state(cls.disk_amount)
    cls._compute_move()
  
  @classmethod
  def end_state(cls)-> None:
    #ok
    cls.state = 2**(cls.disk_amount) - 1
    cls.towers_state = towers.edge_state(cls.disk_amount, True)
    cls.move = None

  @classmethod
  def increment_state(cls, increment:int)-> None:
    #ok
    if abs(increment) <= 100:
      cls.towers_state = towers.neighbor_state(cls.disk_amount, cls.state, cls.towers_state, increment)
    else:
      cls.towers_state = towers.compute_state(cls.disk_amount, cls.state + increment)
    cls.state += increment
    if cls.state < 0:
      cls.state = 0
    if cls.state > 2**cls.disk_amount - 1:
      cls.state = 2**cls.disk_amount - 1
    # State.move = State._get_move()
    cls._compute_move()

  @classmethod
  def state_by_number(cls, state: int)-> None:
    #ok
    cls.state = state
    cls.towers_state = towers.compute_state(cls.disk_amount, state)
    cls._compute_move()

  @classmethod
  def _compute_move(cls)-> None:
    #ok
    if cls.state == 2**(cls.disk_amount) - 1:
      cls.move = None
    else:
      cls.move = towers.compute_next_move(cls.disk_amount, cls.state, cls.towers_state)



  def is_end_state():
    return State.state == 2**(State.disk_amount) - 1