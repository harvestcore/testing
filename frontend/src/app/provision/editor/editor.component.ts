import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

import * as YAML2JSON from 'js-yaml';
import * as JSON2YAML from 'json2yaml';

import { AreyousuredialogComponent } from '../../areyousuredialog/areyousuredialog.component';
import { PlaybooksdialogComponent } from '../playbooksdialog/playbooksdialog.component';

import { PlaybookService } from '../../../services/playbook.service';
import { HostService } from '../../../services/host.service';

import provisionManager from '../../../managers/provisionManager';

@Component({
  selector: 'app-editor',
  templateUrl: './editor.component.html',
  styleUrls: ['./editor.component.css']
})
export class EditorComponent implements OnInit {
  editorOptions = {theme: 'vs-light', language: 'YAML'};
  code = '';

  constructor(
    private snackBar: MatSnackBar,
    private hostService: HostService,
    private playbookService: PlaybookService,
    public dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.resetCurrentPlaybook();
  }

  resetCurrentPlaybook() {
    if (provisionManager.hasPlaybookToEdit()) {
      this.code = JSON2YAML.stringify(provisionManager.playbookToEdit.playbook);
    }
  }

  clearEditor() {
    const ref = this.dialog.open(AreyousuredialogComponent, {});

    ref.afterClosed().subscribe(result => {
      if (result) {
        this.code = '';
      }
    });
  }

  openDialog() {
    const item = provisionManager.playbookToEdit;
    this.hostService.queryHost({query: {}, filter: {}}).subscribe(result => {
      const items = 'total' in result ? result.items : [result];
      const ref = this.dialog.open(PlaybooksdialogComponent, {
        width: '600px',
        data: {
          title: item ? 'Edit playbook' : 'Save new playbook',
          buttonLabel: item ? 'Save' : 'Create',
          item: item ? item : null,
          availableHosts: items
        }
      });

      ref.afterClosed().subscribe(outputData => {
        if (!outputData) {
          return;
        }
        console.log('outputData', outputData);

        if (!item) {
          try {
            const playbooks = YAML2JSON.load(this.code);
            if (playbooks.length > 0) {
              const playbook = playbooks[0];
              playbook.hosts = outputData.hosts;
              this.playbookService.addPlaybook({
                name: outputData.name,
                playbook
              }).subscribe(res => {
                if (res.ok) {
                  this.snack('Playbook created successfully');
                } else {
                  this.snack('The playbook could not be created');
                }
              });
            }
          } catch (e) {
            console.error(e);
            this.snack('An error ocurred when parsing the playbook');
          }
        } else {
          try {
            const playbooks = YAML2JSON.load(this.code);
            if (playbooks.length > 0) {
              const playbook = playbooks[0];
              playbook.hosts = outputData.hosts;
              this.playbookService.updatePlaybook(item.name, {
                name: outputData.name,
                playbook
              }).subscribe(res => {
                if (res.ok) {
                  this.snack('Playbook updated successfully');
                } else {
                  this.snack('The playbook could not be updated');
                }
              });
            }
          } catch (e) {
            console.error(e);
            this.snack('An error ocurred when parsing the playbook');
          }
        }
      });
    });
  }

  snack(msg: string) {
    this.snackBar.open(msg, null, {
      duration: 3000
    });
  }

  loadExample() {
    const ref = this.dialog.open(AreyousuredialogComponent, {});

    ref.afterClosed().subscribe(result => {
      if (result) {
        this.code = `---
- hosts: Please, always set a value to the hosts key.
  remote_user: root
  tasks:
    - name: This is an example
      ping:
      remote_user: user`;
      }
    });
  }
}
