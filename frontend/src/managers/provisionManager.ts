import { EventEmitter } from '@angular/core';
import { Playbook } from '../interfaces/playbook';

class ProvisionManager {
  notifier = new EventEmitter();
  selectedTab = 0;
  playbookToEdit: Playbook = null;

  constructor() {
  }

  setSelectedTab(tab: number): void {
    this.selectedTab = tab;
    if (tab === 0) {
      this.playbookToEdit = null;
    }
    this.notifier.emit();
  }

  getSelectedTab(): number {
    return this.selectedTab;
  }

  setPlaybookToEdit(value: Playbook) {
    this.playbookToEdit = value;
    this.setSelectedTab(1);
  }

  hasPlaybookToEdit() {
    return !!this.playbookToEdit;
  }
}

export default new ProvisionManager();
