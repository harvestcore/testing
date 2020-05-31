import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

import { imports } from '../../../app.module';
import { ManageDialogComponent } from './manage-dialog.component';
import { DeployMockService } from '../../../../services/mocks/deploy-mock.service';
import { DeployService } from '../../../../services/deploy.service';

describe('ManageDialogComponent', () => {
  let component: ManageDialogComponent;
  let fixture: ComponentFixture<ManageDialogComponent>;
  const deployMockService = new DeployMockService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      declarations: [ ManageDialogComponent ],
      providers: [
        { provide: MAT_DIALOG_DATA, useValue: {} },
        { provide: DeployService, useValue: deployMockService }
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
