import { Injectable } from '@angular/core';

import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UrlService {
  client: string;
  url: string;

  constructor() {
    this.computeUrl();
  }

  private computeUrl() {
    // tslint:disable-next-line:no-string-literal
    const env = window['__env'] || null;
    let protocol = 'http://';
    let client = '';
    let backendUrl: string;

    if (env && env.backendUrl) {
      backendUrl = env.backendUrl;
      if (env.httpsEnabled) {
        protocol = 'https://';
      }
    } else {
      backendUrl = environment.backendUrl;
      if (environment.httpsEnabled) {
        protocol = 'https://';
      }
    }

    if (this.client) {
      client = this.client + '.';
    }

    this.url = protocol + client + backendUrl;
  }

  setClient(client: string) {
    this.client = client;
    this.computeUrl();
  }

  getBackendUrl(): string {
    return this.url;
  }
}
