import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { ApiService } from './api.service';
import { NgHttpLoaderModule } from 'ng-http-loader';
import { CommonModule } from '@angular/common';
import { AngularMaterialModule } from './material.module';
import { MatTabsModule } from '@angular/material/tabs';

import { AppComponent } from './app.component';
import { PortalComponent } from './portal/portal.component';

import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

@NgModule({
  declarations: [
    AppComponent,
    PortalComponent,
    PageNotFoundComponent,
  ],
  imports: [
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    BrowserModule,
    HttpClientModule,
    NgHttpLoaderModule.forRoot(),
    CommonModule,
    AngularMaterialModule
  ],
  providers: [
    ApiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
