import { EventEmitter } from '@angular/core';

class DeployManager {
  notifier = new EventEmitter();
  selectedTab = 0;

  constructor() {
  }

  setSelectedTab(tab: number): void {
    this.selectedTab = tab;
    this.notifier.emit();
  }

  getSelectedTab(): number {
    return this.selectedTab;
  }
}

export default new DeployManager();
