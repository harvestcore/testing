import { Component, Inject, OnInit} from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-hostsdialog',
  templateUrl: './hostsdialog.component.html',
  styleUrls: ['./hostsdialog.component.css']
})
export class HostsdialogComponent implements OnInit {
  hostForm: FormGroup;
  item: any = {};
  availableIps: any[] = [];
  selectedIps: any[] = [];

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any
  ) { }

  ngOnInit(): void {
    if (this.data.item) {
      this.item = this.data.item;

      this.item.ips.forEach(ip => {
        this.selectedIps.push(this.data.availableIps.find(item => item.ipv4 === ip));
      });
    }

    if (this.data.availableIps) {
      this.availableIps = this.data.availableIps;
    }

    this.hostForm = new FormGroup({
      name: new FormControl(this.item.name, [
        Validators.required,
        Validators.minLength(1)
      ]),
      ips: new FormControl(this.item.ips, [])
    });
  }

  selectIp(event: any) {
    if (event.value && !this.selectedIps.includes(event.value)) {
      this.selectedIps.push(event.value);
      this.hostForm.value.ips = this.selectedIps.map(it => it.ipv4);
    }
  }

  removeIp(event: any) {
    this.selectedIps = this.selectedIps.filter(it => it.ipv4 !== event.ipv4);
    this.hostForm.value.ips = this.selectedIps.map(it => it.ipv4);
  }
}
