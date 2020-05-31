import { EventEmitter, Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StatusMockService {
  notifier = new EventEmitter();
  constructor() {}

  getStatus(): Observable<any> {
    return of({});
  }
}
