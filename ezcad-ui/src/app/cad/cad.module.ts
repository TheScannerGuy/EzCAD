import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CadRoutingModule } from './cad-routing.module';
import { FormsModule } from '@angular/forms';
import { AngularMaterialModule } from '../material.module';
import { MatTabsModule } from '@angular/material/tabs';

import { CadComponent } from './cad/cad.component';
import { DispatchComponent } from './dispatch/dispatch.component';
import { UnitComponent } from './unit/unit.component';
import { CallBlockComponent } from './call-block/call-block.component';
import { MdtComponent } from './mdt/mdt.component';
import { CreateJobComponent } from './create-job/create-job.component';


@NgModule({
  declarations: [
    CadComponent,
    DispatchComponent,
    UnitComponent,
    CallBlockComponent,
    MdtComponent,
    CreateJobComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    AngularMaterialModule,
    CadRoutingModule,
    MatTabsModule
  ]
})
export class CadModule { }
