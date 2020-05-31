import { Injectable } from '@angular/core';
import { catchError, map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { AuthService } from './auth.service';
import { UrlService } from './url.service';

import { Playbook } from '../interfaces/playbook';
import { Query } from '../interfaces/query';

@Injectable({
  providedIn: 'root'
})
export class PlaybookService {
  path = '/api/provision/playbook';

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService,
    private urlService: UrlService
  ) { }

  updatePlaybook(name: string, hostPlaybook: Playbook): Observable<any> {
    return this.httpClient.put(this.urlService.getBackendUrl() + this.path, {
        name,
        data: hostPlaybook
      }, {
        headers: this.authService.getXAccessTokenHeader()
      }
    ).pipe(
      map(data => {
        return {
          ok: true,
          ...data
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

  removePlaybook(name: string): Observable<any> {
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

  getPlaybook(name: string): Observable<any> {
    const url = this.urlService.getBackendUrl() + this.path + '/' + name;
    return this.httpClient.get(url, {
        headers: this.authService.getXAccessTokenHeader()
      }
    );
  }

  queryPlaybook(query: Query): Observable<any> {
    return this.httpClient.post(this.urlService.getBackendUrl() + this.path + '/query', {
        ...query
      }, {
        headers: this.authService.getXAccessTokenHeader()
      }
    ).pipe(
      map(data => {
        return {
          ok: true,
          ...data
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

  addPlaybook(playbook: Playbook): Observable<any> {
    return this.httpClient.post(this.urlService.getBackendUrl() + this.path, {
        ...playbook
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
