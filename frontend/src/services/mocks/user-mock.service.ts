import { EventEmitter, Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { User } from '../../interfaces/user';
import { Query } from '../../interfaces/query';

@Injectable({
  providedIn: 'root'
})
export class UserMockService {
  private currentUser: User;
  userStateChangedNotifier = new EventEmitter();

  constructor() { }

  setCurrentUser(username: string) {
    return of({});
  }

  clearCurrentUser() {
    this.currentUser = null;
  }

  getCurrentUser(): User {
    return this.currentUser;
  }

  userLoggedIn(): boolean {
    return !!this.currentUser;
  }

  updateUser(email: string, userData: User): Observable<any> {
    return of({});
  }

  removeUser(email: string): Observable<any> {
    return of({});
  }

  getUser(username: string): Observable<any> {
    return of({});
  }

  queryUser(query: Query): Observable<any> {
    return of({});
  }

  addUser(user: User): Observable<any> {
    return of({});
  }
}
