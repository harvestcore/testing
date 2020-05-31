import { Component, OnInit } from '@angular/core';

import provisionManager from '../../managers/provisionManager';

@Component({
  selector: 'app-provision',
  templateUrl: './provision.component.html',
  styleUrls: ['./provision.component.css']
})
export class ProvisionComponent implements OnInit {
  selectedTab = 0;

  constructor( ) { }

  ngOnInit(): void {
    provisionManager.notifier.subscribe(() => {
      this.selectedTab = provisionManager.getSelectedTab();
    });
  }

  changeTab(event: any) {
    provisionManager.setSelectedTab(event.index);
  }
}
