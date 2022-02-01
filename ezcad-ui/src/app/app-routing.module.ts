import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CommonModule } from '@angular/common';

import { PortalComponent } from './portal/portal.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const appRoutes: Routes = [
  { path: '', redirectTo: '/portal', pathMatch: 'full' },
  {
    path: 'portal',
    component: PortalComponent
  },
  {
    path: 'cad',
    loadChildren: () => import('./cad/cad.module')
    .then(m => m.CadModule)
  },
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.module')
    .then(m => m.AdminModule)
  },

  // 404 Page - Keep at bottom
  { path: '**', pathMatch: 'full', component: PageNotFoundComponent},

]

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    )
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule { }