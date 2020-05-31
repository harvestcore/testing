import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

import { Container } from '../../../../interfaces/container';
import { DeployService } from '../../../../services/deploy.service';

@Component({
  selector: 'app-manage-dialog',
  templateUrl: './manage-dialog.component.html',
  styleUrls: ['./manage-dialog.component.css']
})
export class ManageDialogComponent implements OnInit {
  containerForm: FormGroup;

  runningOperation = false;
  fetchingLogs = false;
  logsText = 'Please wait while we are fetching the logs.';
  item: Container;
  step = 0;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private snackBar: MatSnackBar,
    private deployService: DeployService
  ) { }

  ngOnInit(): void {
    this.item = (this.data && this.data.item) || {};

    this.containerForm = new FormGroup({
      name: new FormControl(this.item.name, [
        Validators.required,
        Validators.minLength(2)
      ])
    });
  }

  setStep(step: number) {
    this.step = step;
    if (step === 2) {
      this.logs();
    }
  }

  fetchCurrentItem() {
    this.deployService.containerOperation({
      operation: 'get',
      data: {
        container_id: this.item.id
      }
    }).subscribe(response => {
      if (response.ok) {
        this.item = response.data;
      }
    });
  }

  commonOperation(operation: string) {
    this.runningOperation = true;
    this.deployService.singleContainerOperation({
      container_id: this.item.id,
      operation,
      data: {}
    }).subscribe(response => {
      if (response.ok) {
        this.snack('Operation successful');
        this.fetchCurrentItem();
      } else {
        this.snack('Unsuccessful operation');
      }
      this.runningOperation = false;
    });
  }

  rename() {
    this.deployService.singleContainerOperation({
      container_id: this.item.id,
      operation: 'rename',
      data: {
        name: this.containerForm.value.name
      }
    }).subscribe(response => {
      if (response.ok) {
        this.data.title = 'Manage: ' + this.containerForm.value.name;
        this.snack('Container name changed sucessfully');
      } else {
        this.snack('The container name could not be changed');
      }
    });
  }

  logs() {
    this.fetchingLogs = true;
    this.deployService.singleContainerOperation({
      container_id: this.item.id,
      operation: 'logs',
      data: {}
    }).subscribe(response => {
      if (response.ok) {
        this.logsText = response.data.data;
      } else {
        this.snack('The logs name could not be fetched');
      }
      this.fetchingLogs = false;
    });
  }

  snack(msg: string) {
    this.snackBar.open(msg, null, {
      duration: 3000
    });
  }
}
