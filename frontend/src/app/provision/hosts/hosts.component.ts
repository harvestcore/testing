import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';

import { Host } from '../../../interfaces/host';

import { AreyousuredialogComponent } from '../../areyousuredialog/areyousuredialog.component';
import { HostsdialogComponent } from './hostsdialog/hostsdialog.component';

import { HostService } from '../../../services/host.service';
import { MachineService } from '../../../services/machine.service';

@Component({
  selector: 'app-hosts',
  templateUrl: './hosts.component.html',
  styleUrls: ['./hosts.component.css']
})
export class HostsComponent implements OnInit {
  displayedColumns: string[] = [
    'name',
    'ips'
  ];

  data: Host[];

  constructor(
    private snackBar: MatSnackBar,
    public dialog: MatDialog,
    private hostService: HostService,
    private machineService: MachineService
  ) { }

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.data = null;
    this.hostService.queryHost({query: {}, filter: {}}).subscribe(items => {
      this.data = 'total' in items ? items.items : (!Object.keys(items).length ? [] : [items]);
    });
  }

  createHost(machine: Host) {
    this.hostService.addHost(machine).subscribe(response => {
      if (response.ok) {
        this.snack('Host created successfully');
        this.fetchData();
      } else {
        this.snack('The host could not be created');
      }
    });
  }

  editHost(host: Host) {
    this.hostService.updateHost(host.name, host).subscribe(response => {
      if (response.ok) {
        this.fetchData();
        this.snack('Host updated successfully');
      } else {
        this.snack('The host could not be updated');
      }
    });
  }

  removeHost(machine: Host) {
    const ref = this.dialog.open(AreyousuredialogComponent, {});

    ref.afterClosed().subscribe(result => {
      if (result) {
        this.hostService.removeHost(machine.name).subscribe(response => {
          if (response.ok) {
            this.snack('Host deleted successfully');
            this.fetchData();
          } else {
            this.snack('The host could not be deleted');
          }
        });
      }
    });
  }

  openDialog(item?: Host) {
    this.machineService.queryMachine({query: {}, filter: {}}).subscribe(result => {
      const items = 'total' in result ? result.items : [result];
      const ref = this.dialog.open(HostsdialogComponent, {
        width: '600px',
        data: {
          title: item ? 'Edit host' : 'Add new host group',
          buttonLabel: item ? 'Save' : 'Create',
          item: item ? item : null,
          availableIps: items.filter(machine => !!machine.ipv4)
        }
      });

      ref.afterClosed().subscribe(outputData => {
        if (!outputData) {
          return;
        }

        if (!item) {
          this.createHost(outputData);
        } else {
          this.editHost(outputData);
        }
      });
    });
  }

  snack(msg: string) {
    this.snackBar.open(msg, null, {
      duration: 3000
    });
  }
}
