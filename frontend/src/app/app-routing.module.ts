import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from '../guard/auth.guard';

import { AdminComponent } from './admin/admin.component';
import { DeployComponent } from './deploy/deploy.component';
import { LoginComponent } from './login/login.component';
import { MachinesComponent } from './machines/machines.component';
import { MainContainerComponent } from './main-container/main-container.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { ProvisionComponent } from './provision/provision.component';

const routes: Routes = [
  { path: '', canActivate: [AuthGuard], component: MainContainerComponent},
  { path: 'login', component: LoginComponent},
  { path: 'admin', canActivate: [AuthGuard], component: AdminComponent},
  { path: 'machines', canActivate: [AuthGuard], component: MachinesComponent},
  { path: 'provision', canActivate: [AuthGuard], component: ProvisionComponent},
  { path: 'deploy', canActivate: [AuthGuard], component: DeployComponent},
  { path: '**', canActivate: [AuthGuard], component: NotFoundComponent} // 404 component
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
