import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { MainContainerComponent } from './main-container.component';
import {imports} from '../app.module';
import {UserService} from '../../services/user.service';
import {StatusService} from '../../services/status.service';
import {CustomerService} from '../../services/customer.service';
import {UserMockService} from '../../services/mocks/user-mock.service';
import {StatusMockService} from '../../services/mocks/status-mock.service';
import {CustomerMockService} from '../../services/mocks/customer-mock.service';

describe('MainContainerComponent', () => {
  let component: MainContainerComponent;
  let fixture: ComponentFixture<MainContainerComponent>;
  const mockUserService = new UserMockService();
  const mockStatusService = new StatusMockService();
  const mockCustomerService = new CustomerMockService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      providers: [
        { provide: UserService, useValue: mockUserService },
        { provide: StatusService, useValue: mockStatusService },
        { provide: CustomerService, useValue: mockCustomerService }
      ],
      declarations: [ MainContainerComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MainContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
