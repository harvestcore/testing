import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

import { AreyousuredialogComponent } from '../areyousuredialog/areyousuredialog.component';
import { UserDialogComponent } from './user-dialog/user-dialog.component';

import { User } from '../../interfaces/user';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  displayedColumns: string[] = [
    'type',
    'username',
    'email',
    'public_id',
    'first_name',
    'last_name'
  ];

  data: User[];

  constructor(
    private snackBar: MatSnackBar,
    public dialog: MatDialog,
    private userService: UserService
  ) { }

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.data = null;
    this.userService.queryUser({ query: {}, filter: { deleted: false } }).subscribe(response => {
      if (response.ok) {
        this.data = 'total' in response.data ? response.data.items : (!Object.keys(response.data).length ? [] : [response.data]);
      }
    });
  }

  createUser(user: User) {
    this.userService.addUser(user).subscribe(response => {
      if (response.ok) {
        this.snack('User created successfully');
        this.fetchData();
      } else {
        this.snack('The user could not be created');
      }
    });
  }

  editUser(user: User) {
    delete user.public_id;
    this.userService.updateUser(user.email, user).subscribe(response => {
      if (response.ok) {
        this.fetchData();
        this.snack('User updated successfully');
      } else {
        this.snack('The user could not be updated');
      }
    });
  }

  removeUser(user: User) {
    const ref = this.dialog.open(AreyousuredialogComponent, {});

    ref.afterClosed().subscribe(result => {
      if (result) {
        this.userService.removeUser(user.email).subscribe(response => {
          if (response.ok) {
            this.snack('User deleted successfully');
            this.fetchData();
          } else {
            this.snack('The user could not be deleted');
          }
        });
      }
    });
  }

  openDialog(item?: User) {
    const ref = this.dialog.open(UserDialogComponent, {
      data: {
        title: item ? 'Edit user' : 'Add new user',
        buttonLabel: item ? 'Save' : 'Create',
        item: item ? this.parseData(item) : null
      }
    });

    ref.afterClosed().subscribe(result => {
      if (!result) {
        return;
      }

      if (!item) {
        this.createUser(this.parseData(result));
      } else {
        this.editUser(this.parseData(result));
      }
    });
  }

  parseData(machine: User): User {
    for (const key in machine) {
      if (!machine[key] || machine[key] === '-') {
        delete machine[key];
      }
    }

    return machine;
  }

  snack(msg: string) {
    this.snackBar.open(msg, null, {
      duration: 3000
    });
  }
}
