import * as THREE from 'three';
import { Towers, Move } from './towers';
import { State } from './state';

/**
 * HanoiRenderer: dessine les tours de Hanoï en 3D avec Three.js.
 * Supporte le mode jeu interactif avec zones cliquables par tour.
 * Utilise pointerdown/pointerup pour ne pas interférer avec OrbitControls.
 */
export class HanoiRenderer {
  private scene: THREE.Scene;
  private hanoiGroup: THREE.Group;
  private camera: THREE.PerspectiveCamera;

  // Zones invisibles cliquables pour chaque tour (mode jeu)
  private towerHitZones: THREE.Mesh[] = [];
  private selectedTower: number | null = null;

  // Pour distinguer clic vs drag
  private pointerDownPos: { x: number; y: number } | null = null;

  // Configuration du rendu
  private readonly intervalle = 30;
  private readonly baseWidth = 28;
  private readonly baseHeight = 2;
  private readonly baseDepth = 12;
  private readonly towerRadius = 0.8;
  private readonly towerHeight = 50;
  private readonly diskHeight = 2.2;
  private readonly maxDiskWidth = 24;
  private readonly diskDepth = 8;
  private readonly diskIncrement = 0.9;

  // Couleurs
  private readonly colorDisk = 0x1a182d;
  private readonly colorDiskOrigin = 0x24a1eb;
  private readonly colorDiskDest = 0xdc143c;
  private readonly colorDiskSelected = 0x00a19a;
  private readonly colorTower = 0x8b4513;
  private readonly colorBase = 0x8b4513;
  private readonly colorHighlight = 0xf9bb12;

  // Callback quand le joueur fait un mouvement
  public onPlayerMove: ((from: number, to: number) => void) | null = null;

  constructor(scene: THREE.Scene, camera: THREE.PerspectiveCamera, renderer: THREE.WebGLRenderer) {
    this.scene = scene;
    this.camera = camera;
    this.hanoiGroup = new THREE.Group();
    this.hanoiGroup.name = "hanoiGroup";
    this.scene.add(this.hanoiGroup);

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const domElement = renderer.domElement;

    // Enregistrer la position au pointerdown
    domElement.addEventListener('pointerdown', (event: PointerEvent) => {
      this.pointerDownPos = { x: event.clientX, y: event.clientY };
    });

    // Au pointerup, vérifier si c'est un vrai clic (pas un drag)
    domElement.addEventListener('pointerup', (event: PointerEvent) => {
      if (!this.onPlayerMove || !this.pointerDownPos) return;

      const dx = event.clientX - this.pointerDownPos.x;
      const dy = event.clientY - this.pointerDownPos.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      this.pointerDownPos = null;

      if (dist > 5) return; // C'est un drag, pas un clic

      const rect = domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, this.camera);
      const intersects = raycaster.intersectObjects(this.towerHitZones);

      if (intersects.length > 0) {
        const towerIndex = intersects[0].object.userData.towerIndex as number;
        this.handleTowerClick(towerIndex);
      }
    });
  }

  private handleTowerClick(towerIndex: number): void {
    if (!this.onPlayerMove) return;

    if (this.selectedTower === null) {
      if (State.towersState[towerIndex].length > 0) {
        this.selectedTower = towerIndex;
        this.updateDisplay();
      }
    } else {
      if (towerIndex === this.selectedTower) {
        this.selectedTower = null;
        this.updateDisplay();
      } else {
        const from = this.selectedTower;
        const to = towerIndex;
        const fromTop = State.towersState[from][State.towersState[from].length - 1];
        const toTop = State.towersState[to].length > 0
          ? State.towersState[to][State.towersState[to].length - 1]
          : Infinity;

        if (fromTop < toTop) {
          this.selectedTower = null;
          this.onPlayerMove(from, to);
        } else {
          this.selectedTower = null;
          this.updateDisplay();
        }
      }
    }
  }

  getSelectedTower(): number | null {
    return this.selectedTower;
  }

  resetSelection(): void {
    this.selectedTower = null;
  }

  clearDisplay(): void {
    while (this.hanoiGroup.children.length > 0) {
      const child = this.hanoiGroup.children[0];
      this.hanoiGroup.remove(child);
      if ((child as THREE.Mesh).geometry) (child as THREE.Mesh).geometry.dispose();
      if ((child as THREE.Mesh).material) {
        const mat = (child as THREE.Mesh).material;
        if (Array.isArray(mat)) mat.forEach(m => m.dispose());
        else (mat as THREE.Material).dispose();
      }
    }
    this.towerHitZones = [];
  }

  updateDisplay(): void {
    this.clearDisplay();
    this.drawSetup();

    if (State.mode === "jeu") {
      this.drawStateInteractive(State.towersState);
    } else if (State.moveDisplay) {
      this.drawMove(State.towersState, State.move);
    } else {
      this.drawState(State.towersState);
    }
  }

  private drawSetup(): void {
    for (let i = -1; i <= 1; i++) {
      const towerIdx = i + 1;

      // Base
      const baseGeo = new THREE.BoxGeometry(this.baseWidth, this.baseHeight, this.baseDepth);
      const baseMat = new THREE.MeshStandardMaterial({ color: this.colorBase });
      const base = new THREE.Mesh(baseGeo, baseMat);
      base.position.set(i * this.intervalle, this.baseHeight / 2, 0);
      this.hanoiGroup.add(base);

      // Tour (tige) — jaune si sélectionnée
      const towerGeo = new THREE.CylinderGeometry(this.towerRadius, this.towerRadius, this.towerHeight, 16);
      const isSelected = this.selectedTower === towerIdx;
      const towerMat = new THREE.MeshStandardMaterial({
        color: isSelected ? this.colorHighlight : this.colorTower
      });
      const tower = new THREE.Mesh(towerGeo, towerMat);
      tower.position.set(i * this.intervalle, this.baseHeight + this.towerHeight / 2, 0);
      this.hanoiGroup.add(tower);

      // Zone de clic invisible
      const hitGeo = new THREE.BoxGeometry(this.baseWidth, this.towerHeight + this.baseHeight + 5, this.baseDepth + 4);
      const hitMat = new THREE.MeshBasicMaterial({ visible: false });
      const hitZone = new THREE.Mesh(hitGeo, hitMat);
      hitZone.position.set(i * this.intervalle, (this.towerHeight + this.baseHeight) / 2, 0);
      hitZone.userData.towerIndex = towerIdx;
      this.hanoiGroup.add(hitZone);
      this.towerHitZones.push(hitZone);
    }
  }

  private getDiskWidth(diskNumber: number): number {
    return this.maxDiskWidth - this.diskIncrement * (20 - diskNumber);
  }

  private drawDisk(tower: number, heightIndex: number, diskNumber: number, colorOverride?: number): void {
    const width = this.getDiskWidth(diskNumber);
    const geo = new THREE.BoxGeometry(width, this.diskHeight, this.diskDepth);
    const color = colorOverride ?? this.colorDisk;
    const mat = new THREE.MeshStandardMaterial({ color });
    const mesh = new THREE.Mesh(geo, mat);

    const x = (tower - 1) * this.intervalle;
    const y = this.baseHeight + this.diskHeight / 2 + heightIndex * this.diskHeight;
    mesh.position.set(x, y, 0);
    this.hanoiGroup.add(mesh);

    this.addLabel(diskNumber.toString(), x, y, this.diskDepth / 2 + 0.1);
  }

  private addLabel(text: string, x: number, y: number, z: number): void {
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d')!;
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 40px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, 32, 32);

    const texture = new THREE.CanvasTexture(canvas);
    const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true });
    const sprite = new THREE.Sprite(spriteMat);
    sprite.position.set(x, y, z);
    sprite.scale.set(2, 2, 1);
    this.hanoiGroup.add(sprite);
  }

  private drawState(towers: Towers): void {
    for (let tower = 0; tower < 3; tower++) {
      for (let i = 0; i < towers[tower].length; i++) {
        this.drawDisk(tower, i, towers[tower][i]);
      }
    }
  }

  private drawStateInteractive(towers: Towers): void {
    for (let tower = 0; tower < 3; tower++) {
      for (let i = 0; i < towers[tower].length; i++) {
        const isTopOfSelected = (tower === this.selectedTower) && (i === towers[tower].length - 1);
        const color = isTopOfSelected ? this.colorDiskSelected : undefined;
        this.drawDisk(tower, i, towers[tower][i], color);
      }
    }
  }

  private drawMove(towers: Towers, move: Move): void {
    if (move === null) {
      this.drawState(towers);
      return;
    }

    for (let tower = 0; tower < 3; tower++) {
      for (let i = 0; i < towers[tower].length; i++) {
        const isOrigin = (tower === move[0]) && (i === towers[tower].length - 1);
        this.drawDisk(tower, i, towers[tower][i], isOrigin ? this.colorDiskOrigin : undefined);
      }
    }

    const diskToMove = towers[move[0]][towers[move[0]].length - 1];
    this.drawDisk(move[1], towers[move[1]].length, diskToMove, this.colorDiskDest);
    this.drawArrow(move[0], move[1]);
  }

  private drawArrow(origin: number, destination: number): void {
    const startX = (origin - 1) * this.intervalle;
    const endX = (destination - 1) * this.intervalle;
    const arrowY = this.baseHeight + this.towerHeight + 5;

    const points = [
      new THREE.Vector3(startX, arrowY - 3, 0),
      new THREE.Vector3(startX, arrowY, 0),
      new THREE.Vector3(endX, arrowY, 0),
      new THREE.Vector3(endX, arrowY - 3, 0),
    ];

    const curve = new THREE.CatmullRomCurve3(points);
    const geo = new THREE.TubeGeometry(curve, 32, 0.3, 8, false);
    const mat = new THREE.MeshStandardMaterial({ color: 0x000000 });
    const tube = new THREE.Mesh(geo, mat);
    this.hanoiGroup.add(tube);

    const coneGeo = new THREE.ConeGeometry(1.2, 3, 8);
    const coneMat = new THREE.MeshStandardMaterial({ color: 0x000000 });
    const cone = new THREE.Mesh(coneGeo, coneMat);
    cone.position.set(endX, arrowY - 4, 0);
    cone.rotation.z = Math.PI;
    this.hanoiGroup.add(cone);
  }
}