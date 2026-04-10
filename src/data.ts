import { State } from './state';

const STORAGE_KEY = 'hanoi_fil_rouge_state';

export function saveNow(): void {
  const data = {
    state: State.state,
    date: new Date().toISOString()
  };
  
  let history: Array<{ state: number; date: string }> = [];
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    try { history = JSON.parse(stored); } catch (e) { history = []; }
  }
  history.push(data);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  console.log("État sauvegardé");
}

export function readState(): number {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (!stored) return 0;
  try {
    const history = JSON.parse(stored);
    if (history.length > 0) return history[history.length - 1].state;
  } catch (e) { /* ignore */ }
  return 0;
}
