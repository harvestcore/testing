import { Component, OnInit } from '@angular/core';

import { CustomerService } from '../../services/customer.service';
import { StatusService } from '../../services/status.service';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-main-container',
  templateUrl: './main-container.component.html',
  styleUrls: ['./main-container.component.scss']
})
export class MainContainerComponent implements OnInit {
  nonUsefulDbs = ['system', 'config', 'local', 'admin'];

  dockerDisabled = false;
  dockerMalfunctioning = false;
  dockerIconStyle = {
    color: 'red'
  };

  mongoIconStyle = {
    color: 'red'
  };

  serverIconStyle = {
    color: 'red'
  };

  docker: any;
  mongo: any;
  server: any;
  data: any;

  constructor(
    private customerService: CustomerService,
    private userService: UserService,
    private statusService: StatusService
  ) {}

  ngOnInit(): void {
    this.statusService.notifier.subscribe(response => {
      this.updateStatusByHeartbeat(response);
    });

    if (!this.data) {
      this.updateStatus();
    }
  }

  updateStatus() {
    this.statusService.getStatus().subscribe(response => {
      if (response.ok) {
        this.statusService.executeCallbacks(response);
        this.updateStatusByHeartbeat(response);
      }
    });

  }

  updateStatusByHeartbeat(heartbeat: any) {
    if (heartbeat) {
      this.data = null;

      this.data = heartbeat;
      const serverUp = heartbeat.online || heartbeat.ok;

      this.docker = null;
      if ('status' in heartbeat.data.docker) {
        if (heartbeat.data.docker.disabled) {
          this.dockerDisabled = true;
          this.dockerIconStyle.color = 'red';
        } else {
          this.dockerMalfunctioning = true;
          this.dockerIconStyle.color = 'orange';
        }
      } else {
        this.dockerDisabled = false;
        this.dockerMalfunctioning = false;
        this.docker = heartbeat.data.docker;
        this.dockerIconStyle.color = (serverUp && heartbeat.data.docker.is_up) ? 'green' : 'red';

        this.server = null;
        this.serverIconStyle.color = (serverUp && heartbeat.data.docker.is_up) ? 'green' : 'red';
        this.server = {
          name: this.docker.info.Name,
          os: this.docker.info.OperatingSystem,
          time: this.docker.info.SystemTime,
          cores: this.docker.info.NCPU,
          memory: Math.round(this.docker.info.MemTotal / 1073741824)
        };
      }

      let mongo = heartbeat.data.mongo;
      mongo = {
        ...mongo,
        databases: mongo.data_usage.filter(item => !this.nonUsefulDbs.includes(item.name))
      };
      this.mongoIconStyle.color = (serverUp && heartbeat.data.mongo.is_up) ? 'green' : 'red';

      if (!this.mongo || (this.mongo && this.mongo.databases.length !== mongo.databases.length)) {
        this.mongo = {};
        this.customerService.queryCustomer({query: {}, filter: {}}).subscribe(res => {
          if (res.ok) {
            mongo = {
              ...mongo,
              customers: res.data.total
            };

            this.userService.queryUser({query: {}, filter: {}}).subscribe(r => {
              if (r.ok) {
                mongo = {
                  ...mongo,
                  users: r.data.total
                };
                this.mongo = null;
                this.mongo = mongo;
              }
            });
          }
        });
      }
    }
  }

}
