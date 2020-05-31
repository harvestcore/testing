import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

import { imports } from '../../../app.module';
import { ListImageDialogComponent } from './list-image-dialog.component';
import { DeployMockService } from '../../../../services/mocks/deploy-mock.service';
import { DeployService } from '../../../../services/deploy.service';

describe('ListImageDialogComponent', () => {
  let component: ListImageDialogComponent;
  let fixture: ComponentFixture<ListImageDialogComponent>;
  const deployMockService = new DeployMockService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      declarations: [ ListImageDialogComponent ],
      providers: [
        { provide: MAT_DIALOG_DATA, useValue: {} },
        { provide: DeployService, useValue: deployMockService }
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ListImageDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
