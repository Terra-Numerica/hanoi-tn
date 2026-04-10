import { Towers, Move, computeState, edgeState, computeNextMove, neighborState } from './towers';

export class State {
  static state: number = 0;
  static diskAmount: number = 20;
  static moveDisplay: boolean = false;
  static towersState: Towers = edgeState(20);
  static move: Move = computeNextMove(20, 0, State.towersState);
  static speed: number = 1;
  static mode: string = "";

  static changeDiskAmount(diskAmount: number): void {
    State.diskAmount = diskAmount;
    State.startState();
  }

  static incrementDiskAmount(increment: number): void {
    let newAmount = State.diskAmount + increment;
    if (newAmount > 20) newAmount = 20;
    else if (newAmount < 2) newAmount = 2;
    State.diskAmount = newAmount;
    State.startState();
  }

  static startState(): void {
    State.state = 0;
    State.towersState = edgeState(State.diskAmount);
    State._computeMove();
  }

  static endState(): void {
    State.state = 2 ** State.diskAmount - 1;
    State.towersState = edgeState(State.diskAmount, true);
    State.move = null;
  }

  static incrementState(increment: number): void {
    if (Math.abs(increment) <= 100) {
      State.towersState = neighborState(State.diskAmount, State.state, State.towersState, increment);
    } else {
      State.towersState = computeState(State.diskAmount, State.state + increment);
    }
    State.state += increment;
    if (State.state < 0) State.state = 0;
    if (State.state > 2 ** State.diskAmount - 1) State.state = 2 ** State.diskAmount - 1;
    State._computeMove();
  }

  static stateByNumber(state: number): void {
    State.state = state;
    State.towersState = computeState(State.diskAmount, state);
    State._computeMove();
  }

  static _computeMove(): void {
    if (State.state === 2 ** State.diskAmount - 1) {
      State.move = null;
    } else {
      State.move = computeNextMove(State.diskAmount, State.state, State.towersState);
    }
  }

  static isEndState(): boolean {
    return State.state === 2 ** State.diskAmount - 1;
  }

  // --- Mode Jeu interactif ---
  static playerMoveCount: number = 0;

  static applyPlayerMove(from: number, to: number): void {
    const disk = State.towersState[from].pop()!;
    State.towersState[to].push(disk);
    State.playerMoveCount++;
  }

  static isPlayerWin(): boolean {
    return State.towersState[2].length === State.diskAmount;
  }

  static startGame(diskAmount: number): void {
    State.diskAmount = diskAmount;
    State.towersState = edgeState(State.diskAmount);
    State.playerMoveCount = 0;
    State.mode = "jeu";
    State.move = null;
  }
}