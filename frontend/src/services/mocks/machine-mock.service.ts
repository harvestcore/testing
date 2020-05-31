import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Machine } from '../../interfaces/machine';
import { Query } from '../../interfaces/query';

@Injectable({
  providedIn: 'root'
})
export class MachineMockService {
  path = '/api/machine';

  constructor() { }

  updateMachine(name: string, machineData: Machine): Observable<any> {
    return of({});
  }

  removeMachine(name: string): Observable<any> {
    return of({});
  }

  getMachine(name: string): Observable<any> {
    return of({});
  }

  queryMachine(query: Query): Observable<any> {
    return of({});
  }

  addMachine(machine: Machine): Observable<any> {
    return of({});
  }
}
