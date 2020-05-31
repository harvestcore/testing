import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { IpmtableComponent } from './ipmtable.component';

describe('IpmtableComponent', () => {
  let component: IpmtableComponent;
  let fixture: ComponentFixture<IpmtableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ IpmtableComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(IpmtableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
