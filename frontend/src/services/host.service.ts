import { Injectable } from '@angular/core';
import { catchError, map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { AuthService } from './auth.service';
import { UrlService } from './url.service';

import { Host } from '../interfaces/host';
import { Query } from '../interfaces/query';

@Injectable({
  providedIn: 'root'
})
export class HostService {
  path = '/api/provision/hosts';

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService,
    private urlService: UrlService
  ) { }

  updateHost(name: string, hostData: Host): Observable<any> {
    return this.httpClient.put(this.urlService.getBackendUrl() + this.path, {
        name,
        data: hostData
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

  removeHost(name: string): Observable<any> {
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

  getHost(name: string): Observable<any> {
    const url = this.urlService.getBackendUrl() + this.path + '/' + name;
    return this.httpClient.get(url, {
        headers: this.authService.getXAccessTokenHeader()
      }
    );
  }

  queryHost(query: Query): Observable<any> {
    return this.httpClient.post(this.urlService.getBackendUrl() + this.path + '/query', {
        ...query
      }, {
        headers: this.authService.getXAccessTokenHeader()
      }
    );
  }

  addHost(host: Host): Observable<any> {
    return this.httpClient.post(this.urlService.getBackendUrl() + this.path, {
        ...host
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
