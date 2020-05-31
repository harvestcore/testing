import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

import { Image } from '../../../../interfaces/image';
import { DeployService } from '../../../../services/deploy.service';

@Component({
  selector: 'app-manage-image-dialog',
  templateUrl: './manage-image-dialog.component.html',
  styleUrls: ['./manage-image-dialog.component.css']
})
export class ManageImageDialogComponent implements OnInit {

  runningOperation = false;
  fetchingHistory = false;
  historyText = 'Please wait while we are fetching the history.';
  item: Image;
  step = 0;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private snackBar: MatSnackBar,
    private deployService: DeployService
  ) { }

  ngOnInit(): void {
    this.item = this.data.item;
  }

  setStep(step: number) {
    this.step = step;
    if (step === 1) {
      this.history();
    }
  }

  history() {
    this.fetchingHistory = true;
    if (this.item) {
      this.deployService.singleImageOperation({
        name: this.item.tags.length && this.item.tags[0],
        operation: 'history',
        data: {}
      }).subscribe(response => {
        if (response.ok) {
          this.historyText = response.data.data;
        } else {
          this.snack('The history could not be fetched');
        }
        this.fetchingHistory = false;
      });
    }
  }

  reload() {

  }

  snack(msg: string) {
    this.snackBar.open(msg, null, {
      duration: 3000
    });
  }
}
