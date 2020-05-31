import {Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';

import { FormControl } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSelectChange } from '@angular/material/select';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-ipmtable',
  templateUrl: './ipmtable.component.html',
  styleUrls: ['./ipmtable.component.css']
})
export class IpmtableComponent implements OnInit {
  filter: string;
  dataSource: MatTableDataSource<any>;
  displayedColumnsCopy: string[];
  selectedDisplayedRows: FormControl;

  @Input() title: string;
  @Input() displayedColumns: string[] = [];
  @Input() deselectedColumns: string[] = [];
  @Input() data: any;
  @Input() actions: string[] = [];
  @Output() playCallback = new EventEmitter<any>();
  @Output() detailCallback = new EventEmitter<any>();
  @Output() editCallback = new EventEmitter<any>();
  @Output() removeCallback = new EventEmitter<any>();

  @Input() customActionData: any = {};
  @Output() customActionCallback = new EventEmitter<any>();

  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
  @ViewChild(MatSort, {static: true}) sort: MatSort;

  constructor() {}

  ngOnInit(): void {
    if (this.detailCallback || this.editCallback || this.removeCallback) {
      if (!this.displayedColumns.includes('actions')) {
        this.displayedColumns.push('actions');
      }
    }
    this.displayedColumnsCopy = this.displayedColumns;
    const filteredColumns = this.displayedColumnsCopy.filter(col => !this.deselectedColumns.includes(col));
    this.displayedColumns = filteredColumns;
    this.selectedDisplayedRows = new FormControl(filteredColumns);
    this.dataSource = new MatTableDataSource<any>(this.data);
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
}

  handleColumnSelection(event: MatSelectChange): void {
    this.displayedColumns = event.value;
  }

  clearFilter() {
    this.filter = '';
    this.applyFilter();
  }

  actionEnabled(action: string) {
    return this.actions.includes(action);
  }

  applyFilter() {
    if (this.filter || this.filter === '') {
      this.dataSource.filter = this.filter.trim().toLowerCase();
      if (this.dataSource.paginator) {
        this.dataSource.paginator.firstPage();
      }
    }
  }

  emitPlayCallback(data: any) {
    this.playCallback.emit(data);
  }

  emitDetailCallback(data: any) {
    this.detailCallback.emit(data);
  }

  emitRemoveCallback(data: any) {
    this.removeCallback.emit(data);
  }

  emitEditCallback(data: any) {
    this.editCallback.emit(data);
  }

  emitCustomActionCallback(data: any) {
    this.customActionCallback.emit(data);
  }
}
