import { EventEmitter, Injectable } from '@angular/core';
import { catchError, map, distinctUntilChanged } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { interval, Observable, of } from 'rxjs';

import { AuthService } from './auth.service';
import { UrlService } from './url.service';
import { UserService } from './user.service';

@Injectable({
  providedIn: 'root'
})
export class StatusService {
  heartbeatInterval = 30000;
  notifier = new EventEmitter();
  path = '/api/status';

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService,
    private urlService: UrlService,
    private userService: UserService
  ) {
    interval(this.heartbeatInterval).pipe(
      distinctUntilChanged()
    ).subscribe(() => {
        if (this.userService.userLoggedIn()) {
          this.getStatus().subscribe(hbResponse => {
              this.notifier.emit({
                online: true,
                ...hbResponse
              });
          });
        }
      },
      error => {
        if (this.userService.userLoggedIn()) {
          this.notifier.emit({
            online: false,
            error
          });
        }
      });
  }

  executeCallbacks(data?: any) {
      this.notifier.emit(data);
  }

  getStatus(): Observable<any> {
    return this.httpClient.get(
      this.urlService.getBackendUrl() + this.path,
      {
        headers: this.authService.getXAccessTokenHeader()
      }
    ).pipe(
      map(data => {
        return {
          ok: true,
          data
        };
      }),
      catchError(error => {
        return of({
          ok: false,
          error
        });
      })
    );
  }
}
