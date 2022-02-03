import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminRoutingModule } from './admin-routing.module';

import { AdminComponent } from './admin/admin.component';
import { UsersComponent } from './users/users.component';

import { AngularMaterialModule } from '../material.module';


@NgModule({
  declarations: [
    AdminComponent,
    UsersComponent
  ],
  imports: [
    CommonModule,
    AdminRoutingModule,
    AngularMaterialModule
  ]
})
export class AdminModule { }
