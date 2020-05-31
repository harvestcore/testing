import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { StatusService } from '../../services/status.service';
import { UserService } from '../../services/user.service';

import { User } from '../../interfaces/user';

@Component({
  selector: 'app-top-navigator',
  templateUrl: './top-navigator.component.html',
  styleUrls: ['./top-navigator.component.scss']
})
export class TopNavigatorComponent implements OnInit {
  currentUser: User;
  dockerDisabled = false;
  currentStatus: any;

  constructor(
    private router: Router,
    private authService: AuthService,
    private userService: UserService,
    private statusService: StatusService
  ) {
    this.userService.userStateChangedNotifier.subscribe(() => {
      this.currentUser = null;
      this.updateToolbarData();
    });

    this.statusService.notifier.subscribe(response => {
      if (response.ok) {
        this.dockerDisabled = response.data.docker.disabled;
      }
    });

    this.updateStatus();
  }

  ngOnInit(): void {
  }

  updateToolbarData() {
    this.currentUser = this.userService.getCurrentUser();
  }

  handleLogout() {
    this.currentUser = null;
    this.authService.logout().subscribe(data => {
      this.userService.clearCurrentUser();
      this.router.navigateByUrl('/login');
    });
  }

  updateStatus() {
    if (this.userService.userLoggedIn()) {
      this.statusService.getStatus().subscribe(response => {
        if (response.ok) {
          this.dockerDisabled = response.data.docker.disabled;
        }
      });
    }
  }
}
