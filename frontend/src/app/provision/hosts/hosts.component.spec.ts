import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { imports } from '../../app.module';
import { HostsComponent } from './hosts.component';
import { HostService } from '../../../services/host.service';
import { PlaybookService } from '../../../services/playbook.service';
import { HostMockService } from '../../../services/mocks/host-mock.service';
import { PlaybookMockService } from '../../../services/mocks/playbook-mock.service';

describe('HostsComponent', () => {
  let component: HostsComponent;
  let fixture: ComponentFixture<HostsComponent>;
  const hostMockService = new HostMockService();
  const playbookMockService = new PlaybookMockService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports,
      providers: [
        { provide: HostService, useValue: hostMockService },
        { provide: PlaybookService, useValue: playbookMockService }
      ],
      declarations: [ HostsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HostsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
