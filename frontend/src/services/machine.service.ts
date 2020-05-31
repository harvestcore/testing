import { Injectable } from '@angular/core';
import { catchError, map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { AuthService } from './auth.service';
import { UrlService } from './url.service';

import { Machine } from '../interfaces/machine';
import { Query } from '../interfaces/query';

@Injectable({
  providedIn: 'root'
})
export class MachineService {
  path = '/api/machine';

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService,
    private urlService: UrlService
  ) { }

  updateMachine(name: string, machineData: Machine): Observable<any> {
    return this.httpClient.put(this.urlService.getBackendUrl() + this.path, {
        name,
        data: machineData
      }, {
        headers: this.authService.getXAccessTokenHeader()
      }
    ).pipe(
      map(data => {
        return data;
      }),
      catchError(error => {
        return of({
          ok: false,
          error
        });
      })
    );
  }

  removeMachine(name: string): Observable<any> {
    const url = this.urlService.getBackendUrl() + this.path;
    return this.httpClient.request('delete', url, {
        body: {
          name
        },
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

  getMachine(name: string): Observable<any> {
    const url = this.urlService.getBackendUrl() + this.path + '/' + name;
    return this.httpClient.get(url, {
        headers: this.authService.getXAccessTokenHeader()
      }
    );
  }

  queryMachine(query: Query): Observable<any> {
    return this.httpClient.post(this.urlService.getBackendUrl() + this.path + '/query', {
        ...query
      }, {
        headers: this.authService.getXAccessTokenHeader()
      }
    );
  }

  addMachine(machine: Machine): Observable<any> {
    return this.httpClient.post(this.urlService.getBackendUrl() + this.path, {
        ...machine
      }, {
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
