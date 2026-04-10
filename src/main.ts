import * as THREE from 'three';
// @ts-ignore - Framework is a JS module, typed via framework.d.ts
import Framework from '../framework/js/framework.js';
import { State } from './state';
import { HanoiRenderer } from './hanoiRenderer';
import { renderTime, remainingTime } from './temporality';
import { saveNow, readState } from './data';

// ============================================================
// Initialisation du Framework
// ============================================================
const fw = new Framework();

const scene: THREE.Scene = fw.mainParameters.scene;
const rendererGL: THREE.WebGLRenderer = fw.mainParameters.renderer;
const camera: THREE.PerspectiveCamera = fw.mainParameters.camera;

// Fond texture mur
const textureLoader = new THREE.TextureLoader();
scene.background = textureLoader.load('./framework/textures/wall.jpg');

// Lumières
const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
scene.add(ambientLight);
const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
dirLight.position.set(30, 60, 40);
dirLight.castShadow = true;
scene.add(dirLight);
const fillLight = new THREE.DirectionalLight(0xffffff, 0.4);
fillLight.position.set(-30, 20, -20);
scene.add(fillLight);

// Caméra
camera.position.set(0, 40, 80);
camera.lookAt(0, 20, 0);
fw.onResize();

// ============================================================
// Renderer Hanoï 3D (avec support clic)
// ============================================================
const hanoiRenderer = new HanoiRenderer(scene, camera, rendererGL);

// ============================================================
// CSS : fond blanc + texte noir sur les modals
// ============================================================
const customStyle = document.createElement('style');
customStyle.textContent = `
  .modal-content {
    background-color: #ffffff !important;
    color: #1A182D !important;
  }
  .modal-content h2 {
    color: #1A182D !important;
    border-bottom: 1px solid #ccc !important;
  }
  .modal-content .form-container { color: #1A182D !important; }
  .modal-content label { color: #1A182D !important; }
  .modal-content div { color: #1A182D !important; }
  .modal-content span { color: #1A182D !important; }
  .modal-content button {
    color: #1A182D !important;
    background-color: #EBEBEC !important;
    border: 1px solid #ccc !important;
  }
  .modal-content button:hover {
    background-color: #f9bb12 !important;
    color: #1A182D !important;
  }
  .modal-close.modal-close-expanded::before { color: #1A182D !important; }
  .modal-close.modal-close-collapsed::before { color: #1A182D !important; }
`;
document.head.appendChild(customStyle);

// ============================================================
// Interface (Modals) - remplace le panneau droit tkinter
// ============================================================

// Informations modal removed per user request — expose label variables as null so updateAll() keeps working
let progressLabel: any = null;
let stateLabel: any = null;
let secondaryLabel: any = null;
let remainingLabel: any = null;
let gameInfoLabel: any = null;

// --- Modal "Contrôles" ---
const controlModal = fw.getPermanentModal({
  title: "Contrôles",
  position: { top: 45, right: 1 },
  width: "320px",
  theme: "light",
  id: "controlModal"
});

controlModal.AddButtonToModal("⏮ Début", () => { State.startState(); updateAll(); });
controlModal.AddButtonToModal("◀ -1", () => { State.incrementState(-1); updateAll(); });
controlModal.AddButtonToModal("▶ +1", () => { State.incrementState(1); updateAll(); });
controlModal.AddButtonToModal("⏭ Fin", () => { State.endState(); updateAll(); });
controlModal.AddSeparatorToModal();
controlModal.AddButtonToModal("-10", () => { State.incrementState(-10); updateAll(); });
controlModal.AddButtonToModal("+10", () => { State.incrementState(10); updateAll(); });
controlModal.AddButtonToModal("-100", () => { State.incrementState(-100); updateAll(); });
controlModal.AddButtonToModal("+100", () => { State.incrementState(100); updateAll(); });
controlModal.AddButtonToModal("-10 000", () => { State.incrementState(-10000); updateAll(); });
controlModal.AddButtonToModal("+10 000", () => { State.incrementState(10000); updateAll(); });
controlModal.AddSeparatorToModal();
controlModal.AddButtonToModal("Basculer États ↔ Mouvements", () => {
  State.moveDisplay = !State.moveDisplay;
  updateAll();
});

// --- Modal "Paramètres" ---
const paramModal = fw.getPermanentModal({
  title: "Paramètres",
  position: { top: 2, right: 1 },
  width: "280px",
  theme: "light",
  id: "paramModal"
});

paramModal.AddSliderToModal("Nombre de disques", 2, 20, State.diskAmount, (val: number) => {
  if (State.mode === "jeu") {
    State.startGame(val);
  } else {
    State.changeDiskAmount(val);
  }
  updateAll();
}, { step: 1 });

paramModal.AddSeparatorToModal();
paramModal.AddLabelToModal("Mode automatique", { bold: true, align: "center", color: "#1A182D" });

let autoMode = false;
let autoTimeout: number | null = null;
const speedSteps: Record<number, [number, number]> = {
  1: [1000, 1], 10: [100, 1], 100: [100, 10], 1000: [100, 100]
};

paramModal.AddSliderToModal("Vitesse (mouv/s)", 0, 3, 0, (val: number) => {
  State.speed = Math.round(10 ** val);
}, { step: 1, formatValue: (v: number) => `${Math.round(10 ** v)}` });

paramModal.AddButtonToModal("▶ Lancer / ⏸ Arrêter Auto", () => {
  autoMode = !autoMode;
  if (autoMode) {
    autoRun();
  } else if (autoTimeout !== null) {
    clearTimeout(autoTimeout);
    autoTimeout = null;
  }
});

function autoRun(): void {
  if (!autoMode) return;
  const sp = State.speed;
  const step = speedSteps[sp] || [1000, 1];
  State.incrementState(step[1]);
  updateAll();
  if (State.isEndState()) {
    autoMode = false;
  } else {
    autoTimeout = window.setTimeout(autoRun, step[0]);
  }
}

function stopAuto(): void {
  autoMode = false;
  if (autoTimeout !== null) {
    clearTimeout(autoTimeout);
    autoTimeout = null;
  }
}

// ============================================================
// Mode Jeu : callback quand le joueur clique sur les tours
// ============================================================
hanoiRenderer.onPlayerMove = (from: number, to: number) => {
  State.applyPlayerMove(from, to);
  updateAll();

  if (State.isPlayerWin()) {
    const optimal = 2 ** State.diskAmount - 1;
    const msg = State.playerMoveCount === optimal
      ? `🎉 Bravo ! Résolu en ${State.playerMoveCount} coups (optimal) !`
      : `✅ Résolu en ${State.playerMoveCount} coups (optimal : ${optimal})`;
    if (gameInfoLabel) gameInfoLabel.textContent = msg;
  }
};

// ============================================================
// Navbar (seul le mode Jouer est exposé)
// ============================================================
fw.addButtonToNavbar({
  textButton: "🎮 Jouer",
  onclickFunction: () => {
    stopAuto();
    State.startGame(State.diskAmount);
    hanoiRenderer.onPlayerMove = (from: number, to: number) => {
      State.applyPlayerMove(from, to);
      updateAll();

      if (State.isPlayerWin()) {
        const optimal = 2 ** State.diskAmount - 1;
        const msg = State.playerMoveCount === optimal
          ? `🎉 Bravo ! Résolu en ${State.playerMoveCount} coups (optimal) !`
          : `✅ Résolu en ${State.playerMoveCount} coups (optimal : ${optimal})`;
        if (gameInfoLabel) gameInfoLabel.textContent = msg;
      }
    };
    hanoiRenderer.resetSelection();
    updateAll();
  }
});

// ============================================================
// Mise à jour globale
// ============================================================
function updateAll(): void {
  hanoiRenderer.updateDisplay();

  if (State.mode === "jeu") {
    if (progressLabel) {
      const done = State.towersState[2].length === State.diskAmount;
      progressLabel.textContent = done ? "🏆 Terminé !" : `Coups joués : ${State.playerMoveCount}`;
    }
    if (stateLabel) {
      stateLabel.textContent = `${State.diskAmount} disques`;
    }
    if (secondaryLabel) {
      const sel = hanoiRenderer.getSelectedTower();
      secondaryLabel.textContent = sel !== null
        ? `Tour ${sel + 1} sélectionnée — cliquez la destination`
        : "Cliquez une tour pour prendre un disque";
    }
    if (remainingLabel) {
      const optimal = 2 ** State.diskAmount - 1;
      remainingLabel.textContent = `Minimum théorique : ${optimal} coups`;
    }
  } else {
    const state = State.state;
    const total = 2 ** State.diskAmount - 1;
    const pct = total > 0
      ? ((state / total) * 100).toFixed(6).replace(/\.?0+$/, '')
      : '0';

    if (progressLabel) progressLabel.textContent = `Progression : ${pct} %`;
    if (stateLabel) {
      stateLabel.textContent = State.moveDisplay
        ? `Mouvement ${state + 1}`
        : `État ${state + 1}`;
    }
    if (secondaryLabel) {
      secondaryLabel.textContent = State.moveDisplay
        ? `(De l'État ${state + 1} à l'État ${state + 2})`
        : `(Obtenu après ${state} mouvements)`;
    }
    if (remainingLabel) {
      remainingLabel.textContent = `Temps restant : ${renderTime(remainingTime(state, State.speed, State.diskAmount))}`;
    }
    if (gameInfoLabel) gameInfoLabel.textContent = "";
  }
}

// ============================================================
// Init
// ============================================================
State.mode = "demo";
updateAll();

// ============================================================
// Boucle d'animation
// ============================================================
function animate(): void {
  requestAnimationFrame(animate);
  rendererGL.render(scene, camera);
}
animate();