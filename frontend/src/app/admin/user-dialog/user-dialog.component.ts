import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-user-dialog',
  templateUrl: './user-dialog.component.html',
  styleUrls: ['./user-dialog.component.css']
})
export class UserDialogComponent implements OnInit {
  userForm: FormGroup;

  types: string[] = ['admin', 'regular'];
  item: any = {};

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any
  ) { }

  ngOnInit(): void {
    if (this.data.item) {
      this.item = this.data.item;
    }

    this.userForm = new FormGroup({
      type: new FormControl(this.item.type, [
        Validators.required
      ]),
      username: new FormControl(this.item.username, [
        Validators.required,
        Validators.minLength(1)
      ]),
      password: new FormControl('', [
        Validators.required,
        Validators.minLength(5)
      ]),
      email: new FormControl(this.item.email, [
        Validators.required,
        Validators.minLength(1),
        Validators.email
      ]),
      public_id: new FormControl(this.item.public_id, []),
      first_name: new FormControl(this.item.first_name, [
        Validators.required,
        Validators.minLength(1)
      ]),
      last_name: new FormControl(this.item.last_name, [
        Validators.required,
        Validators.minLength(1)
      ])
    });
  }

}
