import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-areyousuredialog',
  templateUrl: './areyousuredialog.component.html',
  styleUrls: ['./areyousuredialog.component.css']
})
export class AreyousuredialogComponent implements OnInit {

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any
  ) { }

  ngOnInit(): void {
  }

}
