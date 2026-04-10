/**
 * Manipule les tours de Hanoï sous la forme d'une liste de listes d'entiers [[],[],[]],
 * dans laquelle chaque liste correspond à une tour ([0] la tour la plus à gauche).
 * Les entiers représentent des disques, avec 1 le plus petit.
 */

export type Towers = number[][];
export type Move = [number, number] | null;

export function computeState(nbrDisques: number, etat: number): Towers {
  const tours: Towers = [[], [], []];
  const nbrMouvements = etat;

  for (let n = 1; n <= nbrDisques; n++) {
    let compteur = 0;
    if (nbrMouvements >= 2 ** (n - 1)) {
      let dernierMouvement = 2 ** (n - 1);
      compteur = 1;
      while (dernierMouvement + 2 ** n <= nbrMouvements) {
        compteur++;
        dernierMouvement += 2 ** n;
      }
    }

    const versGauche = n % 2 === 0;

    if (versGauche) {
      tours[((-compteur % 3) + 3) % 3].push(n);
    } else {
      tours[compteur % 3].push(n);
    }
  }

  if (nbrDisques % 2 === 1) {
    const temp = tours[2];
    tours[2] = tours[1];
    tours[1] = temp;
  }

  for (let i = 0; i < 3; i++) {
    tours[i].reverse();
  }

  return tours;
}

export function edgeState(diskAmount: number, final: boolean = false): Towers {
  const towers: Towers = [[], [], []];
  const index = final ? 2 : 0;
  for (let i = diskAmount; i > 0; i--) {
    towers[index].push(i);
  }
  return towers;
}

function top(nbrDisques: number, list: number[]): number {
  return list.length === 0 ? nbrDisques + 1 : list[list.length - 1];
}

export function computeNextMove(diskAmount: number, state: number, towers: Towers): Move {
  if (state < 0 || state >= 2 ** diskAmount) return null;

  let oneTower = 0;
  if (top(diskAmount, towers[0]) === 1) oneTower = 0;
  else if (top(diskAmount, towers[1]) === 1) oneTower = 1;
  else oneTower = 2;

  if (state % 2 === 0) {
    if (diskAmount % 2 === 0) {
      return [oneTower, (oneTower + 1) % 3];
    } else {
      return [oneTower, ((oneTower - 1) % 3 + 3) % 3];
    }
  } else {
    const remainingTowers = [0, 1, 2].filter(t => t !== oneTower);
    if (top(diskAmount, towers[remainingTowers[0]]) < top(diskAmount, towers[remainingTowers[1]])) {
      return [remainingTowers[0], remainingTowers[1]];
    } else {
      return [remainingTowers[1], remainingTowers[0]];
    }
  }
}

function computeBackMove(diskAmount: number, state: number, towers: Towers): Move {
  if (state < 1 || state > 2 ** diskAmount) return null;

  let oneTower = 0;
  if (top(diskAmount, towers[0]) === 1) oneTower = 0;
  else if (top(diskAmount, towers[1]) === 1) oneTower = 1;
  else oneTower = 2;

  if (state % 2 === 1) {
    if (diskAmount % 2 === 0) {
      return [oneTower, ((oneTower - 1) % 3 + 3) % 3];
    } else {
      return [oneTower, (oneTower + 1) % 3];
    }
  } else {
    const remainingTowers = [0, 1, 2].filter(t => t !== oneTower);
    if (top(diskAmount, towers[remainingTowers[0]]) < top(diskAmount, towers[remainingTowers[1]])) {
      return [remainingTowers[0], remainingTowers[1]];
    } else {
      return [remainingTowers[1], remainingTowers[0]];
    }
  }
}

function applyMove(towers: Towers, move: Move): Towers {
  if (!move) return towers;
  towers[move[1]].push(towers[move[0]].pop()!);
  return towers;
}

export function neighborState(diskAmount: number, state: number, towers: Towers, increment: number): Towers {
  if ((state === 0 && increment < 0) || (state === 2 ** diskAmount - 1 && increment > 0)) {
    return towers;
  }

  // Deep copy to avoid mutation
  let currentTowers: Towers = towers.map(t => [...t]);
  let currentState = state;
  let remaining = increment;

  while (remaining !== 0) {
    if (remaining > 0) {
      const move = computeNextMove(diskAmount, currentState, currentTowers);
      currentTowers = applyMove(currentTowers, move);
      currentState++;
      remaining--;
      if (currentState >= 2 ** diskAmount - 1) break;
    } else {
      const move = computeBackMove(diskAmount, currentState, currentTowers);
      currentTowers = applyMove(currentTowers, move);
      currentState--;
      remaining++;
      if (currentState <= 0) break;
    }
  }

  return currentTowers;
}
