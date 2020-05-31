import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { imports } from '../../app.module';
import { ContainersComponent } from './containers.component';
import { DeployMockService } from '../../../services/mocks/deploy-mock.service';
import { DeployService } from '../../../services/deploy.service';

describe('ContainersComponent', () => {
  let component: ContainersComponent;
  let fixture: ComponentFixture<ContainersComponent>;
  const deployMockService = new DeployMockService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      declarations: [ ContainersComponent ],
      providers: [
        { provide: DeployService, useValue: deployMockService }
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ContainersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
