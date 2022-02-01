import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, Routes } from '@angular/router';

import { CadComponent } from './cad/cad.component';
import { DispatchComponent } from './dispatch/dispatch.component';
import { UnitComponent } from './unit/unit.component';

export const cadRoutes: Routes = [
    {
        path: '',
        component: CadComponent,
        children: [
            {
                path: '',
                children: [
                    { path: 'unit', component: UnitComponent },
                    { path: 'dispatch', component: DispatchComponent }
                ]
            }
        ]
    }
]

@NgModule({
    declarations: [],
    imports: [
      CommonModule,
      RouterModule.forChild(cadRoutes)
    ],
    exports: [
      RouterModule
    ]
  })
  export class CadRoutingModule { }