import { Injectable } from '@angular/core';
import { catchError, map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { AuthService} from './auth.service';
import { UrlService } from './url.service';

import { ContainerOperation, SingleContainerOperation } from '../interfaces/container';
import { ImageOperation, SingleImageOperation } from '../interfaces/image';

@Injectable({
  providedIn: 'root'
})
export class DeployService {
  path = '/api/deploy';

  constructor(
    private httpClient: HttpClient,
    private authService: AuthService,
    private urlService: UrlService
  ) { }

  containerOperation(containerOperation: ContainerOperation): Observable<any> {
    return this.httpClient.post(this.urlService.getBackendUrl() + this.path + '/container', {
        ...containerOperation
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

  singleContainerOperation(singleContainerOperation: SingleContainerOperation): Observable<any> {
    return this.httpClient.post(this.urlService.getBackendUrl() + this.path + '/container/single', {
        ...singleContainerOperation
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

  imageOperation(imageOperation: ImageOperation): Observable<any> {
    return this.httpClient.post(this.urlService.getBackendUrl() + this.path + '/image', {
        ...imageOperation
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

  singleImageOperation(singleImageOperation: SingleImageOperation): Observable<any> {
    return this.httpClient.post(this.urlService.getBackendUrl() + this.path + '/image/single', {
        ...singleImageOperation
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
