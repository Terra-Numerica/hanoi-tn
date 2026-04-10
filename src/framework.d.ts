// Type declarations for the Terra Numerica Framework (JS)

declare module '../framework/js/framework.js' {
  interface MainParameters {
    scene: import('three').Scene;
    camera: import('three').PerspectiveCamera;
    renderer: import('three').WebGLRenderer;
  }

  interface ModalInstance {
    AddButtonToModal: (text: string, onClick: () => void, options?: Record<string, any>) => HTMLElement;
    AddSliderToModal: (label: string, min: number, max: number, value: number, onChange: (val: number) => void, options?: Record<string, any>) => { slider: HTMLInputElement; valueDisplay: HTMLElement; container: HTMLElement };
    AddCheckboxToModal: (label: string, checked: boolean, onChange: (val: boolean) => void) => { checkbox: HTMLInputElement; container: HTMLElement };
    AddDropDownToModal: (label: string, options: Array<{ value: string; label?: string }>, selectedValue: string, onChange: (val: string) => void) => { select: HTMLSelectElement; container: HTMLElement };
    AddColorPickerToModal: (label: string, initialColor: string, onChange: (val: string) => void) => { colorPicker: HTMLInputElement; valueDisplay: HTMLElement; container: HTMLElement };
    AddSeparatorToModal: () => HTMLElement;
    AddLabelToModal: (text: string, options?: { align?: string; bold?: boolean; fontSize?: string; color?: string }) => HTMLElement;
    ClearFormModal: () => void;
    ToggleCollapseModal: () => void;
    CollapseModal: () => void;
    ExpandModal: () => void;
  }

  class Framework {
    mainParameters: MainParameters;
    CTABannerParameter: any;

    constructor();

    onResize(options?: { renderer?: any; window?: Window; camera?: any; enabled?: boolean }): void;
    updateOcclusionVisibility(camera: any, threshold: number, raycaster: any, direction: any): void;
    attachLight(object: any, options?: { color?: string; intensity?: number; name?: string }): any;
    startLoadingScreen(): HTMLElement;
    removeLoadingScreen(): void;

    loadModel(path: string, name: string, options?: { size?: number; timeToWait?: number; visible?: boolean; position?: { x: number; y: number; z: number }; rotation?: { x: number; y: number; z: number } }): Promise<any>;
    create_copy(name: string, options?: { size?: number; counter?: number; timeToWait?: number; position?: { x: number; y: number; z: number }; rotation?: { x: number; y: number; z: number } }): Promise<any>;
    delete_copy(name: string): Promise<boolean>;
    delete_model(name: string): Promise<boolean>;
    loadTexture(path: string, options?: { repeatHorizontal?: number; repeatVertical?: number; repeat?: number }): any;

    addSimpleSceneWithTable(options?: any): any;
    addSimpleSceneWithoutTable(options?: any): void;
    addSceneFromJson(path: string): Promise<void>;
    addInteractiveCupboard(options?: { width?: number; depth?: number; height?: number }): any;

    update(camera: any): void;

    addButtonToNavbar(options?: { textButton?: string; onclickFunction?: () => void; hover?: boolean; classesOfTheButton?: string[] }): HTMLElement;
    addDropdownToNavbar(options?: { textButton?: string; dropdownList?: Array<{ text: string; onClick?: () => void }> }): HTMLElement;
    changeTextOfButton(buttonNumber: number, newText: string): void;
    changeTextOfDropdown(dropdownNumber: number, dropBoxToChange: number, newText: string): void;

    getWindowWidth(): number;
    getWindowHeight(): number;

    getPermanentModal(options?: {
      title?: string;
      draggable?: boolean;
      showCloseButton?: boolean;
      position?: { right?: number; top?: number };
      width?: string;
      visible?: boolean;
      id?: string;
      theme?: string;
    }): ModalInstance;
  }

  export default Framework;
}

declare module '../framework/js/CTABanner.js' {
  class CTABanner {
    constructor();
    getNavbar(): HTMLElement;
    getCanvas(): HTMLElement;
    getContainer(): HTMLElement;
    create_button(options: { text?: string; onClick?: () => void; position?: string; referenceElement?: HTMLElement | null; classes?: string[] }): HTMLElement;
    create_dropdown(options: { parentId?: string; buttonText: string; menuId: string }): void;
    create_dropdown_list(menuId: string, items: Array<{ text: string; href?: string; onClick?: () => void }>): void;
  }
  export default CTABanner;
}

declare module '../framework/js/modal.js' {
  class Modal {
    constructor(existingBanner?: any);
    getPermanentModal(options?: any): any;
  }
  export default Modal;
}

declare module '*.json' {
  const value: Record<string, string>;
  export default value;
}
