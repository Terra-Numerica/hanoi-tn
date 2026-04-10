# Tours de Hanoï — Three.js + Framework Terra Numerica

Conversion du projet Python/Tkinter **hanoi-tn** en TypeScript + Three.js, utilisant le **Framework Terra Numerica**.

## Structure du projet

```
hanoi-project/
├── index.html                    # Point d'entrée HTML
├── package.json                  # Dépendances (three, vite, typescript)
├── tsconfig.json                 # Configuration TypeScript
├── vite.config.ts                # Configuration Vite (bundler)
│
├── src/                          # Code source TypeScript
│   ├── main.ts                   # Point d'entrée — init Framework, modals, boucle animate
│   ├── hanoiRenderer.ts          # Rendu 3D des tours (Three.js) — remplace hanoi_canvas.py
│   ├── state.ts                  # Gestion d'état global — remplace state.py
│   ├── towers.ts                 # Algorithme des tours de Hanoï — remplace towers.py
│   ├── temporality.ts            # Calculs temporels — remplace temporality.py
│   ├── data.ts                   # Persistance (localStorage) — remplace data.py
│   ├── colors.json               # Palette de couleurs
│   └── framework.d.ts            # Déclarations de types pour le framework JS
│
└── framework/                    # Framework Terra Numerica (inchangé)
    ├── js/
    │   ├── framework.js
    │   ├── CTABanner.js
    │   ├── modal.js
    │   ├── createScene.js
    │   ├── table.js
    │   ├── armoire.js
    │   └── products.js
    ├── css/
    │   ├── style.css
    │   ├── BannerStyle.css
    │   └── ModalStyle.css
    └── textures/
        ├── wall.jpg
        ├── roof.jpg
        └── wood_floor.jpg
```

## Correspondance Python → TypeScript

| Fichier Python original          | Fichier TypeScript               | Description                                  |
|----------------------------------|----------------------------------|----------------------------------------------|
| `logic/towers.py`               | `src/towers.ts`                  | Algorithme Hanoï (calcul d'états, mouvements) |
| `logic/state.py`                | `src/state.ts`                   | État global (singleton statique)              |
| `logic/temporality.py`          | `src/temporality.ts`             | Calculs de temps restant, dates               |
| `logic/data.py`                 | `src/data.ts`                    | Persistence (CSV → localStorage)              |
| `interface/hanoi_canvas.py`     | `src/hanoiRenderer.ts`           | Rendu visuel (Tkinter Canvas → Three.js 3D)   |
| `interface/right_frame.py`      | `src/main.ts` (modals)           | Panneau info/contrôles (CTk → Modal Framework) |
| `interface/bottom_frame.py`     | `src/main.ts` (controlModal)     | Boutons navigation (CTk → Modal Framework)    |
| `interface/auto_frame.py`       | `src/main.ts` (paramModal)       | Mode auto, vitesse                            |
| `interface/info_frame.py`       | `src/main.ts` (infoModal)        | Infos progression                             |
| `app.py`                        | `src/main.ts`                    | Application principale                        |

## Utilisation du Framework

Le projet utilise les fonctionnalités suivantes du Framework Terra Numerica :

- **`Framework()`** — Initialise la scène Three.js, caméra, renderer, navbar
- **`fw.getPermanentModal()`** — Crée les panneaux de contrôle (3 modals draggables)
- **`modal.AddButtonToModal()`** — Boutons de navigation ⏮ ◀ ▶ ⏭
- **`modal.AddSliderToModal()`** — Slider nombre de disques + vitesse
- **`modal.AddLabelToModal()`** — Labels de progression, état, temps restant
- **`fw.addButtonToNavbar()`** — Boutons "Mode Démo", "Mode Fil Rouge", "Sauvegarder"
- **`fw.onResize()`** — Gestion responsive de la fenêtre

## Installation & Lancement

```bash
# Installer les dépendances
npm install

# Lancer en mode développement
npm run dev

# Build production
npm run build
```

## Fonctionnalités

### Mode Démo
- Navigation libre entre les états (2 à 20 disques)
- Boutons ±1, ±10, ±100, ±10 000 mouvements
- Mode automatique avec vitesse réglable (1 à 1000 mouv/s)
- Affichage du temps restant estimé
- Bascule affichage États / Mouvements

### Mode Fil Rouge
- 20 disques fixes
- Sauvegarde de l'avancement (localStorage)
- Compteur de visiteurs

### Rendu 3D
- Tours et bases en bois (cylindres + boîtes)
- Disques colorés avec numéros (sprites texte)
- Disque d'origine en bleu, destination en rouge
- Flèche animée montrant le mouvement en cours
- Caméra orbitale (OrbitControls via le Framework)
