import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProvisionMockService {
  constructor() { }

  runPlaybook(hosts: [string], playbook: string, passwords: any): Observable<any> {
    return of({});
  }
}
