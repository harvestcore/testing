import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule } from '@angular/platform-browser';
import { FlexLayoutModule } from '@angular/flex-layout';
import { HttpClientModule } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatCardModule} from '@angular/material/card';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDividerModule } from '@angular/material/divider';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatPaginatorModule} from '@angular/material/paginator';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSelectModule } from '@angular/material/select';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule} from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { FontAwesomeIconsModule } from '../icons/FontAwesomeIconsModule';
import { MonacoEditorModule } from 'ngx-monaco-editor';

import { AppComponent } from './app.component';
import { AuthService } from '../services/auth.service';
import { CustomerService } from '../services/customer.service';
import { DeployService } from '../services/deploy.service';
import { HostService } from '../services/host.service';
import { MachineService } from '../services/machine.service';
import { PlaybookService } from '../services/playbook.service';
import { ProvisionService } from '../services/provision.service';
import { StatusService } from '../services/status.service';
import { UrlService } from '../services/url.service';
import { UserService } from '../services/user.service';

import { AreyousuredialogComponent } from './areyousuredialog/areyousuredialog.component';
import { EditorComponent } from './provision/editor/editor.component';
import { HostsComponent } from './provision/hosts/hosts.component';
import { HostsdialogComponent } from './provision/hosts/hostsdialog/hostsdialog.component';
import { IpmtableComponent } from './ipmtable/ipmtable.component';
import { LoginComponent } from './login/login.component';
import { MachinesComponent } from './machines/machines.component';
import { MachinesdialogComponent } from './machines/machinesdialog/machinesdialog.component';
import { MainContainerComponent } from './main-container/main-container.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { PlaybooksComponent } from './provision/playbooks/playbooks.component';
import { PlaybooksdialogComponent } from './provision/playbooksdialog/playbooksdialog.component';
import { ProvisionComponent } from './provision/provision.component';
import { RunplaybookdialogComponent } from './provision/runplaybookdialog/runplaybookdialog.component';
import { TopNavigatorComponent } from './top-navigator/top-navigator.component';
import { DeployComponent } from './deploy/deploy.component';
import { ContainersComponent } from './deploy/containers/containers.component';
import { ManageDialogComponent } from './deploy/containers/manage-dialog/manage-dialog.component';
import { ImagesComponent } from './deploy/images/images.component';
import { ManageImageDialogComponent } from './deploy/images/manage-image-dialog/manage-image-dialog.component';
import { ListImageDialogComponent } from './deploy/images/list-image-dialog/list-image-dialog.component';
import { AdminComponent } from './admin/admin.component';
import { UserDialogComponent } from './admin/user-dialog/user-dialog.component';

const providers = [
  AuthService,
  CustomerService,
  DeployService,
  HostService,
  MachineService,
  PlaybookService,
  ProvisionService,
  StatusService,
  UrlService,
  UserService
];

export const declarations = [
  AdminComponent,
  AppComponent,
  AreyousuredialogComponent,
  ContainersComponent,
  DeployComponent,
  EditorComponent,
  HostsComponent,
  HostsdialogComponent,
  ImagesComponent,
  IpmtableComponent,
  ListImageDialogComponent,
  LoginComponent,
  MachinesComponent,
  MachinesdialogComponent,
  MainContainerComponent,
  ManageDialogComponent,
  ManageImageDialogComponent,
  NotFoundComponent,
  PlaybooksComponent,
  PlaybooksdialogComponent,
  ProvisionComponent,
  RunplaybookdialogComponent,
  TopNavigatorComponent,
  UserDialogComponent
];

export const imports = [
  AppRoutingModule,
  BrowserAnimationsModule,
  BrowserModule,
  FlexLayoutModule,
  FontAwesomeIconsModule,
  FormsModule,
  HttpClientModule,
  MatButtonModule,
  MatButtonToggleModule,
  MatCardModule,
  MatDialogModule,
  MatDividerModule,
  MatExpansionModule,
  MatFormFieldModule,
  MatGridListModule,
  MatInputModule,
  MatListModule,
  MatMenuModule,
  MatPaginatorModule,
  MatProgressBarModule,
  MatSelectModule,
  MatSlideToggleModule,
  MatSnackBarModule,
  MatSortModule,
  MatTableModule,
  MatTabsModule,
  MatToolbarModule,
  MatTooltipModule,
  ReactiveFormsModule,

  MonacoEditorModule.forRoot()
];

@NgModule({
  declarations,
  imports,
  providers,
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor() {
  }
}
