import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { ContainerOperation, SingleContainerOperation } from '../../interfaces/container';
import { ImageOperation, SingleImageOperation } from '../../interfaces/image';

@Injectable({
  providedIn: 'root'
})
export class DeployMockService {
  constructor() { }

  containerOperation(containerOperation: ContainerOperation): Observable<any> {
    return of({});
  }

  singleContainerOperation(singleContainerOperation: SingleContainerOperation): Observable<any> {
    return of({});
  }

  imageOperation(imageOperation: ImageOperation): Observable<any> {
    return of({});
  }

  singleImageOperation(singleImageOperation: SingleImageOperation): Observable<any> {
    return of({});
  }
}
