import { Component, OnInit } from '@angular/core';

import deployManager from '../../managers/deployManager';

@Component({
  selector: 'app-deploy',
  templateUrl: './deploy.component.html',
  styleUrls: ['./deploy.component.css']
})
export class DeployComponent implements OnInit {
  selectedTab = 0;

  constructor() { }

  ngOnInit(): void {
    deployManager.notifier.subscribe(() => {
      this.selectedTab = deployManager.getSelectedTab();
    });
  }

  changeTab(event: any) {
    deployManager.setSelectedTab(event.index);
  }

}
