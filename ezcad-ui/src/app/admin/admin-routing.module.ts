import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, Routes } from '@angular/router';

import { AdminComponent } from './admin/admin.component';
import { UsersComponent } from './users/users.component';

const adminRoutes: Routes = [
    {
        path: '',
        component: AdminComponent,
        children: [
            {
                path: '',
                children: [
                    { path: '', component: UsersComponent }
                ]
            }
        ]
    }
]

@NgModule({
    declarations: [],
    imports: [
      CommonModule,
      RouterModule.forChild(adminRoutes)
    ],
    exports: [
      RouterModule
    ]
  
  })
  export class AdminRoutingModule { }