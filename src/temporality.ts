const monthNames: Record<number, string> = {
  1: "janvier", 2: "février", 3: "mars", 4: "avril",
  5: "mai", 6: "juin", 7: "juillet", 8: "août",
  9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
};

function plural(value: number): string {
  return value > 1 ? 's' : '';
}

export function renderTime(seconds: number): string {
  if (seconds === 0) return "Terminé !";

  let secs = seconds;
  const days = Math.floor(secs / 86400); secs %= 86400;
  const hours = Math.floor(secs / 3600); secs %= 3600;
  const minutes = Math.floor(secs / 60); secs %= 60;

  if (days !== 0) {
    return `${days} jour${plural(days)} ${hours} heure${plural(hours)}\n${minutes} minute${plural(minutes)} ${secs} seconde${plural(secs)}`;
  } else if (hours !== 0) {
    return `${hours} heure${plural(hours)}\n${minutes} minute${plural(minutes)} ${secs} seconde${plural(secs)}`;
  } else if (minutes !== 0) {
    return `${minutes} minute${plural(minutes)} ${secs} seconde${plural(secs)}`;
  } else {
    return `${secs} seconde${plural(secs)}`;
  }
}

export function remainingTime(state: number, speed: number, diskAmount: number): number {
  const moves = (2 ** diskAmount - 1) - state;
  return Math.ceil(moves / speed);
}

export function endDate(seconds: number): string {
  const now = new Date();
  const then = new Date(now.getTime() + seconds * 1000);

  if (now.toDateString() === then.toDateString()) {
    const h = then.getHours().toString().padStart(2, '0');
    const m = then.getMinutes().toString().padStart(2, '0');
    return `Aujourd'hui ! (${h}:${m})`;
  } else {
    return `${then.getDate()} ${monthNames[then.getMonth() + 1]} ${then.getFullYear()}`;
  }
}
