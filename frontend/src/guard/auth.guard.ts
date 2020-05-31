import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';

import { AuthService } from '../services/auth.service';
import { StatusService } from '../services/status.service';
import { UserService } from '../services/user.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  dockerDisabled = false;

  constructor(
    private userService: UserService,
    private authService: AuthService,
    private statusService: StatusService,
    private router: Router
  ) {
    this.statusService.notifier.subscribe(response => {
      if (response.ok) {
        this.dockerDisabled = response.data.docker.disabled;
      }
    });
  }

  canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    return this.checkAccess(state.url);
  }

  checkAccess(url: string): boolean {
    let canAccess = false;

    if (url.includes('login')) {
      this.authService.login().subscribe(response => {
        if (response.ok) {
          this.router.navigateByUrl('/');
        }
      });

      canAccess = true;
    } else {
      if (this.userService.userLoggedIn()) {
        if (url === 'admin') {
          const user = this.userService.getCurrentUser();
          canAccess = user.type === 'admin';
        } else {
          if (url === 'deploy') {
            this.checkDocker();
            canAccess = !this.dockerDisabled;
          } else {
            canAccess = true;
          }
        }
      } else {
        this.authService.login().subscribe(response => {
          if (!response.ok) {
            this.router.navigateByUrl('/login');
          } else {
            if (url === 'deploy') {
              this.checkDocker();
              canAccess = !this.dockerDisabled;
            } else {
              canAccess = true;
            }
          }
        });
      }
    }

    return canAccess;
  }

  checkDocker() {
    this.statusService.getStatus().subscribe(response => {
      if (response.ok) {
        this.dockerDisabled = response.data.docker.disabled;
      }
    });
  }
}
