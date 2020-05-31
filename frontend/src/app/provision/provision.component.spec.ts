import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { imports } from '../app.module';
import { ProvisionComponent } from './provision.component';

describe('ProvisionComponent', () => {
  let component: ProvisionComponent;
  let fixture: ComponentFixture<ProvisionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      declarations: [ ProvisionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProvisionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
