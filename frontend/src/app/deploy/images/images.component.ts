import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';

import { AreyousuredialogComponent } from '../../areyousuredialog/areyousuredialog.component';
import { ListImageDialogComponent } from './list-image-dialog/list-image-dialog.component';
import { ManageImageDialogComponent } from './manage-image-dialog/manage-image-dialog.component';
import { DeployService } from '../../../services/deploy.service';

@Component({
  selector: 'app-images',
  templateUrl: './images.component.html',
  styleUrls: ['./images.component.css']
})
export class ImagesComponent implements OnInit {
  displayedColumns: string[] = [
    'id',
    // 'labels',
    'short_id',
    'tags'
  ];

  manageContainerCustomActionData = {
    icon: 'cogs',
    tooltip: 'Manage image'
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
    this.deployService.imageOperation({ operation: 'list', data: { all: true } }).subscribe(response => {
      if (response.data) {
        const data = 'total' in response.data ? response.data.items : (!Object.keys(response.data).length ? [] : [response.data]);
        this.data = data.filter(item => item.tags.length > 0);
      }
    });
  }

  manageImage(data: any) {
    const ref = this.dialog.open(ManageImageDialogComponent, {
      data: {
        title: 'Manage: ' + data.short_id,
        item: data
      }
    });

    ref.afterClosed().subscribe(result => {
      this.fetchData();
    });
  }

  searchImages() {
    const ref = this.dialog.open(ListImageDialogComponent, {
      minWidth: '700px',
      data: {
        title: 'Search and pull images'
      }
    });
    ref.afterClosed().subscribe(result => {
      this.fetchData();
    });
  }

  removeImage(data: any) {
    const ref = this.dialog.open(AreyousuredialogComponent, {});
    ref.afterClosed().subscribe(result => {
      if (result) {
        this.deployService.imageOperation({
          operation: 'remove',
          data: {
            image: data.id.split('sha256:')[1],
            force: true
          }
        }).subscribe(res => {
          if (res.ok) {
            this.snack('Image removed');
          } else {
            this.snack('The image could not be removed');
          }
          this.fetchData();
        });
      }
    });
  }

  pruneImages() {
    const ref = this.dialog.open(AreyousuredialogComponent, {});
    ref.afterClosed().subscribe(result => {
      if (result) {
        this.deployService.imageOperation({
          operation: 'prune',
          data: {}
        }).subscribe(res => {
          if (res.ok) {
            this.fetchData();
            this.snack('Images pruned');
          } else {
            this.snack('The images could not be pruned');
          }
        });
      }
    });
  }

  runImage(item: any) {
    if (item) {
      this.deployService.containerOperation({
        operation: 'run',
        data: {
          image: item && item.tags[0]
        }
      }).subscribe(response => {
        if (response.ok) {
          this.snack('Image running');
        } else {
          this.snack('There was an error while trying to run the image');
        }
      });
    }
  }

  snack(msg: string) {
    this.snackBar.open(msg, null, {
      duration: 3000
    });
  }
}
