import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

import { AreyousuredialogComponent } from '../areyousuredialog/areyousuredialog.component';
import { Machine } from '../../interfaces/machine';
import { MachinesdialogComponent } from './machinesdialog/machinesdialog.component';
import { MachineService } from '../../services/machine.service';

@Component({
  selector: 'app-machines',
  templateUrl: './machines.component.html',
  styleUrls: ['./machines.component.css']
})
export class MachinesComponent implements OnInit {
  displayedColumns: string[] = [
    'name',
    'description',
    'type',
    'ipv4',
    'ipv6',
    'mac',
    'broadcast',
    'gateway',
    'netmask',
    'network'
  ];

  deselectedColumns: string[] = [
    'description'
  ];

  data: Machine[];

  constructor(
    private snackBar: MatSnackBar,
    public dialog: MatDialog,
    private machineService: MachineService
  ) { }

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.data = null;
    this.machineService.queryMachine({query: {}, filter: {}}).subscribe(items => {
      this.data = 'total' in items ? items.items : (!Object.keys(items).length ? [] : [items]);
    });
  }

  createMachine(machine: Machine) {
    this.machineService.addMachine(machine).subscribe(response => {
      if (response.ok) {
        this.snack('Machine created successfully');
        this.fetchData();
      } else {
        this.snack('The machine could not be created');
      }
    });
  }

  editMachine(machine: Machine) {
    this.machineService.updateMachine(machine.name, machine).subscribe(response => {
      if (response.ok) {
        this.fetchData();
        this.snack('Machine updated successfully');
      } else {
        this.snack('The machine could not be updated');
      }
    });
  }

  removeMachine(machine: Machine) {
    const ref = this.dialog.open(AreyousuredialogComponent, {});

    ref.afterClosed().subscribe(result => {
      if (result) {
        this.machineService.removeMachine(machine.name).subscribe(response => {
          if (response.ok) {
            this.snack('Machine deleted successfully');
            this.fetchData();
          } else {
            this.snack('The machine could not be deleted');
          }
        });
      }
    });
  }

  openDialog(item?: Machine) {
    const ref = this.dialog.open(MachinesdialogComponent, {
      data: {
        title: item ? 'Edit machine' : 'Add new machine',
        buttonLabel: item ? 'Save' : 'Create',
        item: item ? this.parseData(item) : null
      }
    });

    ref.afterClosed().subscribe(result => {
      if (!result) {
        return;
      }

      if (!item) {
        this.createMachine(this.parseData(result));
      } else {
        this.editMachine(this.parseData(result));
      }
    });
  }

  parseData(machine: Machine): Machine {
    for (const key in machine) {
      if (!machine[key] || machine[key] === '-') {
        delete machine[key];
      }
    }

    return machine;
  }

  snack(msg: string) {
    this.snackBar.open(msg, null, {
      duration: 3000
    });
  }
}
