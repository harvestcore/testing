import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { imports } from '../../app.module';
import { ImagesComponent } from './images.component';
import { DeployMockService } from '../../../services/mocks/deploy-mock.service';
import { DeployService } from '../../../services/deploy.service';

describe('ImagesComponent', () => {
  let component: ImagesComponent;
  let fixture: ComponentFixture<ImagesComponent>;
  const deployMockService = new DeployMockService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      declarations: [ ImagesComponent ],
      providers: [
        { provide: DeployService, useValue: deployMockService }
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
