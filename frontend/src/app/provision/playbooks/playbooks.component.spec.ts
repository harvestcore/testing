import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaybooksComponent } from './playbooks.component';
import { imports } from '../../app.module';
import { PlaybookService } from '../../../services/playbook.service';
import { PlaybookMockService } from '../../../services/mocks/playbook-mock.service';

describe('PlaybooksComponent', () => {
  let component: PlaybooksComponent;
  let fixture: ComponentFixture<PlaybooksComponent>;
  const playbookMockService = new PlaybookMockService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      providers: [
        { provide: PlaybookService, useValue: playbookMockService }
      ],
      declarations: [ PlaybooksComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PlaybooksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
