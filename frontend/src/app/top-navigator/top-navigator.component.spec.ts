import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { imports } from '../app.module.js';
import { TopNavigatorComponent } from './top-navigator.component';

import { AuthMockService } from '../../services/mocks/auth-mock.service';
import { AuthService } from '../../services/auth.service';
import { StatusMockService } from '../../services/mocks/status-mock.service';
import { StatusService } from '../../services/status.service';
import { UserMockService } from '../../services/mocks/user-mock.service';
import { UserService } from '../../services/user.service';

describe('TopNavigatorComponent', () => {
  let component: TopNavigatorComponent;
  let fixture: ComponentFixture<TopNavigatorComponent>;
  const mockAuthService = new AuthMockService();
  const mockUserService = new UserMockService();
  const mockStatusService = new StatusMockService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      providers: [
        { provide: UserService, useValue: mockUserService },
        { provide: StatusService, useValue: mockStatusService },
        { provide: AuthService, useValue: mockAuthService }
      ],
      declarations: [ TopNavigatorComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopNavigatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
