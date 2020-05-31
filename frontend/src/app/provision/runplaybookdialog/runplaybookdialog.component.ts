import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

import { ProvisionService } from '../../../services/provision.service';

@Component({
  selector: 'app-runplaybookdialog',
  templateUrl: './runplaybookdialog.component.html',
  styleUrls: ['./runplaybookdialog.component.css']
})
export class RunplaybookdialogComponent implements OnInit {
  running = true;
  item: any = {};
  text = 'Please wait while the playbook is running.';

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private provisionService: ProvisionService
  ) { }

  ngOnInit(): void {
    if (this.data.item) {
      if (this.data.item.playbook) {
        const hosts = this.data.item.playbook[0].hosts;
        const name = this.data.item.name;
        this.provisionService.runPlaybook(hosts, name, {}).subscribe(result => {
          if (result.ok) {
            this.text = result.data.result;
          } else {
            this.text = 'There was an error while trying to run the playbook';
          }
          this.running = false;
        });
      }
    }
  }
}
