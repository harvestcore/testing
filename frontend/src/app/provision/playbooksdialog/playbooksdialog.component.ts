import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-playbooksdialog',
  templateUrl: './playbooksdialog.component.html',
  styleUrls: ['./playbooksdialog.component.css']
})
export class PlaybooksdialogComponent implements OnInit {
  playbookForm: FormGroup;
  item: any = {};
  availableHosts: any[] = [];
  selectedHosts: any[] = [];

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any
  ) { }

  ngOnInit(): void {
    if (this.data.item) {
      this.item = this.data.item;

      this.item.ips.forEach(ip => {
        this.selectedHosts.push(this.data.availableHosts.find(item => item.name === ip));
      });
    }

    if (this.data.availableHosts) {
      this.availableHosts = this.data.availableHosts;
    }

    this.playbookForm = new FormGroup({
      name: new FormControl(this.item.name, [
        Validators.required,
        Validators.minLength(1)
      ]),
      hosts: new FormControl(this.item.hosts, [])
    });
  }

  selectHost(event: any) {
    if (event.value && !this.selectedHosts.includes(event.value)) {
      this.selectedHosts.push(event.value);
      this.playbookForm.value.hosts = this.selectedHosts.map(it => it.name);
    }
  }

  removeHost(event: any) {
    this.selectedHosts = this.selectedHosts.filter(it => it.name !== event.name);
    this.playbookForm.value.hosts = this.selectedHosts.map(it => it.name);
  }
}
