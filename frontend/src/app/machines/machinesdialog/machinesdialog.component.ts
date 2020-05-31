import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-machinesdialog',
  templateUrl: './machinesdialog.component.html',
  styleUrls: ['./machinesdialog.component.css']
})
export class MachinesdialogComponent implements OnInit {
  machineForm: FormGroup;

  types: string[] = ['local', 'remote'];
  item: any = {};

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any
  ) { }

  ngOnInit(): void {
    if (this.data.item) {
      this.item = this.data.item;
    }

    this.machineForm = new FormGroup({
      name: new FormControl(this.item.name, [
        Validators.required,
        Validators.minLength(1)
      ]),
      description: new FormControl(this.item.description, []),
      type: new FormControl(this.item.type, [
        Validators.required
      ]),
      ipv4: new FormControl(this.item.ipv4, []),
      ipv6: new FormControl(this.item.ipv6, []),
      mac: new FormControl(this.item.mac, []),
      broadcast: new FormControl(this.item.broadcast, []),
      gateway: new FormControl(this.item.gateway, []),
      netmask: new FormControl(this.item.netmask, []),
      network: new FormControl(this.item.network, [])
    });
  }
}
