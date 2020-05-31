import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Customer } from '../../interfaces/customer';
import { Query } from '../../interfaces/query';

@Injectable({
  providedIn: 'root'
})
export class CustomerMockService {
  constructor() { }

  updateCustomer(domain: string, customerData: Customer): Observable<any> {
    return of({});
  }

  removeCustomer(domain: string): Observable<any> {
    return of({});
  }

  queryCustomer(query: Query): Observable<any> {
    return of({});
  }

  addCustomer(customer: Customer): Observable<any> {
    return of({});
  }
}
