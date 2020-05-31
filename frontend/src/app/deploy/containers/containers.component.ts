import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';

import deployManager from '../../../managers/deployManager';
import { AreyousuredialogComponent } from '../../areyousuredialog/areyousuredialog.component';
import { ManageDialogComponent } from './manage-dialog/manage-dialog.component';
import { DeployService } from '../../../services/deploy.service';

@Component({
  selector: 'app-containers',
  templateUrl: './containers.component.html',
  styleUrls: ['./containers.component.css']
})
export class ContainersComponent implements OnInit {
  displayedColumns: string[] = [
    'status',
    'name',
    'short_id',
    'image_tag',
    'id'
  ];

  manageContainerCustomActionData = {
    icon: 'cogs',
    tooltip: 'Manage container'
  };

  data: any[];

  constructor(
    private snackBar: MatSnackBar,
    public dialog: MatDialog,
    private deployService: DeployService
  ) { }

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.data = null;
    this.deployService.containerOperation({ operation: 'list', data: { all: true } }).subscribe(response => {
      if (!response || !response.data) {
        this.data = [];
      } else {
        if (response.data) {
          this.data = 'total' in response.data ? response.data.items : (!Object.keys(response.data).length ? [] : [response.data]);
          this.data.forEach(container => container.image_tag = container.image.tags[0] || '-');
        }
      }
    });
  }

  pruneContainers() {
    const ref = this.dialog.open(AreyousuredialogComponent, {});
    ref.afterClosed().subscribe(result => {
      if (result) {
        this.deployService.containerOperation({
          operation: 'prune',
          data: {}
        }).subscribe(res => {
          if (res.ok) {
            this.fetchData();
            this.snack('Containers pruned');
          } else {
            this.snack('The containers could not be pruned');
          }
        });
      }
    });
  }

  manageContainer(data: any) {
    const ref = this.dialog.open(ManageDialogComponent, {
      data: {
        title: 'Manage: ' + data.name,
        item: data
      }
    });

    ref.afterClosed().subscribe(result => {
      this.fetchData();
    });
  }

  goToImages() {
    deployManager.setSelectedTab(1);
  }

  snack(msg: string) {
    this.snackBar.open(msg, null, {
      duration: 3000
    });
  }
}
