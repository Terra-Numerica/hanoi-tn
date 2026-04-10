"""
Manipule les tours de Hanoï sous la forme d'une liste de listes d'entiers [[],[],[]], dans laquelle chaque liste correspond à une tour ([0] la tour la plus à gauche).
Les entiers représentent des disques, avec 1 le plus petit.
"""


def compute_state(nbr_disques: int, etat: int)-> list[list[int]]:
  """Retourne l'état des tours à l'état etat pour nbr_disques disques.

  Args:
      nbr_disques (int): Le nombre de disques utilisés
      etat (int): L'indice de l'état retourné, entre 0 (état 1 initial) et 2**nbr_disques - 1 (état 2**n final) inclus.

  Returns:
      list[list[int]]: La liste représentant l'état des tours obtenu.
  """

  tours = [[],[],[]]
  nbr_mouvements = etat

  # pour chaque disque n de 1 à nbr_disques
  for n in range(1, nbr_disques + 1):
      
    #compter mouvements
    if (nbr_mouvements < 2**(n-1)):
      compteur = 0
    else:
      dernier_mouvement = 2**(n-1)
      compteur = 1
      while dernier_mouvement + 2**n <= nbr_mouvements:
        compteur += 1
        dernier_mouvement += 2**n
    
    #déterminer direction
    vers_gauche = (n%2 == 0) #vers la gauche si n pair

    #calculer position après mouvement nbr_mouvements
    if vers_gauche: 
      tours[(- compteur) % 3].append(n)
    else:
      tours[compteur % 3].append(n)
  
  #inverser tours 1 et 2 si nbr_disques impair
  if nbr_disques % 2 == 1:
    temp = tours[2]
    tours[2] = tours[1]
    tours[1] = temp

  #remettre dans l'ordre
  for i in range(3):
    tours[i].reverse()
  
  return tours


def edge_state(disk_amount: int, final: bool = False)-> list[list[int]]:
  towers = [[],[],[]]
  index: int = 2 if final else 0

  for i in range(disk_amount, 0, -1):
    towers[index].append(i)

  return towers


def neighbor_state(disk_amount: int, state: int, towers: list[list[int]], increment: int)-> list[list[int]]:
  """Retourne la représentation des tours à l'état state + increment.

  Args:
      disk_amount (int): Nombre de disques du problème.
      state (int): État de départ.
      towers (list[list[int]]): Représentation de l'état de départ.
      increment (int): Différence entre l'état d'arrivée et l'état de départ.

  Returns:
      list[list[int]]: Représentation de l'état obtenu.
  """
  if (state == 0 and increment < 0) or (state == 2**disk_amount - 1 and increment > 0):
    return towers

  while increment != 0:
    
    if increment > 0:
      return neighbor_state(disk_amount, state+1, _apply_move(towers, compute_next_move(disk_amount, state, towers)), increment-1)
    
    if increment < 0:
      return neighbor_state(disk_amount, state-1, _apply_move(towers, _compute_back_move(disk_amount, state, towers)), increment+1)
  
  return towers


def _next_state(disk_amount: int, state: int, towers: list[list[int]])-> list[list[int]]:
  """Retourne l'état state+1 à partir de la représentation towers de l'état state.

  Args:
      disk_amount (int): Le nombre de disques du problème.
      state (int): L'indice de l'état de départ.
      towers (list[list[int]]): La représentation de l'état de départ.

  Returns:
      list[list[int]]: La représentation de l'état suivant l'état de départ.
  """
  return _apply_move(towers, compute_next_move(disk_amount, state, towers))


def _previous_state(disk_amount: int, state: int, towers: list[list[int]])-> list[list[int]]:
  """Retourne l'état state-1 à partir de la représentation towers de l'état state.

  Args:
      disk_amount (int): Le nombre de disques du problème.
      state (int): L'indice de l'état de départ.
      towers (list[list[int]]): La représentation de l'état de départ.

  Returns:
      list[list[int]]: La représentation de l'état précédant l'état de départ.
  """
  return _apply_move(towers, _compute_back_move(disk_amount, state, towers))


def _apply_move(towers: list[list[int]], move: tuple[int, int])-> list[list[int]]:
  """Applique le mouvement move à l'état représenté par towers et retourne le nouvel état obtenu.

  Args:
      towers (list[list[int]]): L'état initial.
      move (tuple[int, int]): Le mouvement à appliquer à towers.

  Returns:
      list[list[int]]: L'état obtenu après avoir appliqué le mouvement.
  """
  towers[move[1]].append(towers[move[0]].pop())
  return towers


def compute_next_move(disk_amount: int, state: int, towers: list[list[int]])-> tuple[int, int]:
  """Retourne le prochain mouvement sous la forme (depart, arrivée)

  Args:
      disk_amount (int): Nombre de disques
      state (int): Indice de l'état actuel (états de 0 à 2**disk_amount - 1)
      towers (list[list[int]]): État actuel des tours

  Returns:
      tuple[int, int]: Représentation du prochain mouvement sous la forme (départ, arrivée), indices entre 0 (gauche) et 2 (droite)
  """
  if state < 0 or state >= 2**disk_amount:
    return None

  #détermine l'indice de la tour sur laquelle se trouve le disque 1
  if _top(disk_amount, towers[0]) == 1:
    one_tower = 0
  elif _top(disk_amount, towers[1]) == 1:
    one_tower = 1
  else:
    one_tower = 2

  if state%2 == 0:
    #indice de mouvement pair ==> mouvement du disque 1

    if disk_amount%2 == 0:
      #nombre de disques pair ==> vers la droite
      return (one_tower, (one_tower+1)%3)
        
    else:
      #nombre de disques impair ==> vers la gauche
      return (one_tower, (one_tower-1)%3)

  else:
    #indice de mouvement impair ==> mouvement n'impliquant pas le disque 1
    remaining_towers = [0,1,2]
    remaining_towers.remove(one_tower)
    
    if _top(disk_amount, towers[remaining_towers[0]]) < _top(disk_amount, towers[remaining_towers[1]]):
      return (remaining_towers[0], remaining_towers[1])
    else:
      return (remaining_towers[1], remaining_towers[0])


def _compute_back_move(disk_amount: int, state: int, towers: list[list[int]])-> list[list[int]]:
  """Retourne le mouvement menant à l'état précédent sous la forme (depart, arrivée)

  Args:
      disk_amount (int): Nombre de disques
      state (int): Indice de l'état actuel (états de 0 à 2**disk_amount - 1)
      towers (list[list[int]]): État actuel des tours

  Returns:
      tuple[int, int]: Représentation du mouvement sous la forme (départ, arrivée), indices entre 0 (gauche) et 2 (droite)
  """
  if state < 1 or state > 2**disk_amount:
    return None

  #détermine l'indice de la tour sur laquelle se trouve le disque 1
  if _top(disk_amount, towers[0]) == 1:
    one_tower = 0
  elif _top(disk_amount, towers[1]) == 1:
    one_tower = 1
  else:
    one_tower = 2

  if state%2 == 1:
    #indice de state impair ==> mouvement du disque 1

    if disk_amount%2 == 0:
      #nombre de disques pair ==> vers la gauche
      return (one_tower, (one_tower-1)%3)
        
    else:
      #nombre de disques impair ==> vers la droite
      return (one_tower, (one_tower+1)%3)

  else:
    #indice de state pair ==> mouvement n'impliquant pas le disque 1
    remaining_towers = [0,1,2]
    remaining_towers.remove(one_tower)
    
    if _top(disk_amount, towers[remaining_towers[0]]) < _top(disk_amount, towers[remaining_towers[1]]):
      return (remaining_towers[0], remaining_towers[1])
    else:
      return (remaining_towers[1], remaining_towers[0])


def _top(nbr_disques: int, list: list)-> int:
  """Retourne le dernier élément de la liste si elle n'est pas vide, nbr_disques+1 sinon.

  Args:
      list (list): La liste.
      nbr_disques (int): Le nombre de disques du problème.

  Returns:
      int: Le dernier élément de la liste, ou nbr_disques+1 si la liste est vide.
  """
  if len(list) == 0:
    return nbr_disques + 1
  else:
    return list[-1]