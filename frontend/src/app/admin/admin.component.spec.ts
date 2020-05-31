import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { imports } from '../app.module';
import { AdminComponent } from './admin.component';
import { UserService } from '../../services/user.service';
import { UserMockService } from '../../services/mocks/user-mock.service';

describe('AdminComponent', () => {
  let component: AdminComponent;
  let fixture: ComponentFixture<AdminComponent>;
  const userMockService = new UserMockService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      providers: [ { provide: UserService, useValue: userMockService } ],
      declarations: [ AdminComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
