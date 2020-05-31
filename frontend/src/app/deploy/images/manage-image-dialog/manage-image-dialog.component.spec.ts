import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

import { imports } from '../../../app.module';
import { ManageImageDialogComponent } from './manage-image-dialog.component';
import { DeployMockService } from '../../../../services/mocks/deploy-mock.service';
import { DeployService } from '../../../../services/deploy.service';

describe('ManageImageDialogComponent', () => {
  let component: ManageImageDialogComponent;
  let fixture: ComponentFixture<ManageImageDialogComponent>;
  const deployMockService = new DeployMockService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      declarations: [ ManageImageDialogComponent ],
      providers: [
        { provide: MAT_DIALOG_DATA, useValue: {} },
        { provide: DeployService, useValue: deployMockService }
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageImageDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
