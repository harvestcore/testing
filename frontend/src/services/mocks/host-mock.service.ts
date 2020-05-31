import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Host } from '../../interfaces/host';
import { Query } from '../../interfaces/query';

@Injectable({
  providedIn: 'root'
})
export class HostMockService {
  constructor() { }

  updateHost(name: string, hostData: Host): Observable<any> {
    return of({});
  }

  removeHost(name: string): Observable<any> {
    return of({});
  }

  getHost(name: string): Observable<any> {
    return of({});
  }

  queryHost(query: Query): Observable<any> {
    return of({});
  }

  addHost(host: Host): Observable<any> {
    return of({});
  }
}
