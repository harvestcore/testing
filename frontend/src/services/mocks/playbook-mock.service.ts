import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Playbook } from '../../interfaces/playbook';
import { Query } from '../../interfaces/query';

@Injectable({
  providedIn: 'root'
})
export class PlaybookMockService {
  constructor() { }

  updatePlaybook(name: string, hostPlaybook: Playbook): Observable<any> {
    return of({});
  }

  removePlaybook(name: string): Observable<any> {
    return of({});
  }

  getPlaybook(name: string): Observable<any> {
    return of({});
  }

  queryPlaybook(query: Query): Observable<any> {
    return of({});
  }

  addPlaybook(playbook: Playbook): Observable<any> {
    return of({});
  }
}
