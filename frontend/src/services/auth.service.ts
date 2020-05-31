import { HttpClient } from '@angular/common/http';
import { EventEmitter, Injectable } from '@angular/core';
import { map, catchError } from 'rxjs/operators';
import { Observable, of } from 'rxjs';

import { JwtHelperService } from '@auth0/angular-jwt';
import * as Cookies from 'js-cookie';

import { AccessToken } from '../interfaces/access-token';
import { BasicAuth } from '../interfaces/basic-auth';
import { Router } from '@angular/router';
import { UrlService } from './url.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  loginPath = '/api/login';
  logoutPath = '/api/logout';

  private token: AccessToken;
  loginStateChangedNotifier = new EventEmitter();

  constructor(
    private router: Router,
    private httpClient: HttpClient,
    private urlService: UrlService
  ) { }

  getXAccessTokenHeader(): any {
    return this.token;
  }

  private loginAPICall(auth: BasicAuth): Observable<any> {
    return this.httpClient.get(this.urlService.getBackendUrl() + this.loginPath, {
      headers: {
        Authorization: 'Basic ' + btoa(auth.username + ':' + auth.password)
      }
    });
  }

  login(auth?: BasicAuth): Observable<any> {
    const localToken = Cookies.get('ipm-token');
    if (localToken) {
      const jwtHelper = new JwtHelperService();
      const decodedToken = jwtHelper.decodeToken(localToken);

      if ((decodedToken.exp * 1000) > Date.now()) {
        this.token = {
          'x-access-token': localToken
        };

        this.loginStateChangedNotifier.emit();

        return of({
          ok: true,
          token: this.token,
          fromLocal: true
        });
      }
    }

    if (auth) {
      this.urlService.setClient(auth.client);
      return this.loginAPICall(auth).pipe(
        map(data => {
          if ('token' in data) {
            this.token = {
              'x-access-token': data.token
            };

            // Set token that lasts half a day
            Cookies.set('ipm-token', data.token, { expires: 0.5 });
          }

          this.loginStateChangedNotifier.emit();

          return {
            ok: true,
            token: this.token,
            fromLocal: false
          };
        }),
        catchError(error => {
          return of({
            ok: false,
            token: this.token,
            fromLocal: false,
            error
          });
        })
      );
    }

    return of({
      ok: false,
      token: null,
      fromLocal: false
    });
  }

  logout(): Observable<any> {
    return this.httpClient.get(this.urlService.getBackendUrl() + this.logoutPath, {
      headers: this.getXAccessTokenHeader()
    }).pipe(map(() => {
      Cookies.remove('ipm-token', { path: '' });
      this.loginStateChangedNotifier.emit({logout: true});
    }));
  }
}
