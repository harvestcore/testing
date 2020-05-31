import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';

import { Playbook } from '../../../interfaces/playbook';

import { AreyousuredialogComponent } from '../../areyousuredialog/areyousuredialog.component';
import { RunplaybookdialogComponent } from '../runplaybookdialog/runplaybookdialog.component';

import { PlaybookService } from '../../../services/playbook.service';
import provisionManager from '../../../managers/provisionManager';

@Component({
  selector: 'app-playbooks',
  templateUrl: './playbooks.component.html',
  styleUrls: ['./playbooks.component.css']
})
export class PlaybooksComponent implements OnInit {
  displayedColumns: string[] = [
    'name',
    'hosts'
  ];

  data: Playbook[];

  constructor(
    private snackBar: MatSnackBar,
    public dialog: MatDialog,
    private playbookService: PlaybookService
  ) { }

  ngOnInit(): void {
    this.fetchData();
  }

  goToEditor(item?: Playbook) {
    if (item) {
      provisionManager.setPlaybookToEdit(item);
    }

    provisionManager.setSelectedTab(1);
  }

  fetchData(): void {
    this.data = null;
    this.playbookService.queryPlaybook({query: {}, filter: {}}).subscribe(items => {
      const data = 'total' in items ? items.items : (!Object.keys(items).length ? [] : [items]);
      data.forEach(item => item.hosts = item.playbook[0].hosts);
      this.data = data;
    });
  }

  editPlaybook(event: any) {
    provisionManager.setPlaybookToEdit({
      name: event.name,
      playbook: event.playbook
    });
  }

  removePlaybook(playbook: Playbook) {
    const ref = this.dialog.open(AreyousuredialogComponent, {});

    ref.afterClosed().subscribe(result => {
      if (result) {
        this.playbookService.removePlaybook(playbook.name).subscribe(response => {
          if (response.ok) {
            this.snack('Playbook deleted successfully');
            this.fetchData();
          } else {
            this.snack('The playbook could not be deleted');
          }
        });
      }
    });
  }

  runPlaybook(event: any) {
    const ref = this.dialog.open(RunplaybookdialogComponent, {
      width: '600px',
      data: {
        title: 'Running playbook',
        buttonLabel: 'Ok',
        item: event
      }
    });

    ref.afterClosed().subscribe(outputData => {
      if (!outputData) {
        return;
      }
    });
  }

  snack(msg: string) {
    this.snackBar.open(msg, null, {
      duration: 3000
    });
  }
}
