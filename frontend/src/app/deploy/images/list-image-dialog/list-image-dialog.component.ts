import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

import { DockerHubImage } from '../../../../interfaces/dockerhubimage';
import { DeployService } from '../../../../services/deploy.service';

@Component({
  selector: 'app-list-image-dialog',
  templateUrl: './list-image-dialog.component.html',
  styleUrls: ['./list-image-dialog.component.css']
})
export class ListImageDialogComponent implements OnInit {
  listForm: FormGroup;
  displayedColumns = [
    'name',
    'star_count',
    'is_official',
    'is_automated',
    'description'
  ];

  manageContainerCustomActionData = {
    icon: 'download',
    tooltip: 'Pull image'
  };

  pullingImage = false;
  results: DockerHubImage[];

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private snackBar: MatSnackBar,
    private deployService: DeployService
  ) { }

  ngOnInit(): void {
    this.listForm = new FormGroup({
      searchTerm: new FormControl('', [
        Validators.required,
        Validators.minLength(1)
      ])
    });
  }

  search() {
    this.deployService.imageOperation({
      operation: 'search',
      data: {
        term: this.listForm.value.searchTerm
      }
    }).subscribe(response => {
      if (response.ok) {
        this.results = null;
        this.results = response.data.items;
      } else {
        this.snack('There was an error while searching');
      }
    });
  }

  pull(item: any) {
    this.pullingImage = true;
    this.deployService.imageOperation({
      operation: 'pull',
      data: {
        repository: item.name
      }
    }).subscribe(response => {
      if (response.ok) {
        this.snack('Image pulled');
      } else {
        this.snack('There was an error while pulling the image');
      }
      this.pullingImage = false;
    });
  }

  snack(msg: string) {
    this.snackBar.open(msg, null, {
      duration: 3000
    });
  }
}
