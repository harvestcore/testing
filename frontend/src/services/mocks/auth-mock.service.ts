import { EventEmitter, Injectable, Output } from '@angular/core';
import { Observable, of } from 'rxjs';

import { AccessToken } from '../../interfaces/access-token';
import { BasicAuth } from '../../interfaces/basic-auth';

@Injectable({
  providedIn: 'root'
})
export class AuthMockService {

  private token: AccessToken;
  loginStateChangedNotifier = new EventEmitter();

  constructor() { }

  getXAccessTokenHeader(): any {
    return this.token;
  }

  login(auth?: BasicAuth): Observable<any> {
    return of({});
  }

  logout(): Observable<any> {
    return of({});
  }
}
