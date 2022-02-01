import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';


import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatBadgeModule } from '@angular/material/badge';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule } from '@angular/material/dialog';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatTabsModule } from '@angular/material/tabs';


@NgModule( {
    imports: [
        CommonModule,
        MatCheckboxModule,
        MatCheckboxModule,
        MatButtonModule,
        MatInputModule,
        MatAutocompleteModule,
        MatDatepickerModule,
        MatFormFieldModule,
        MatRadioModule,
        MatSelectModule,
        MatSidenavModule,
        MatBadgeModule,
        MatToolbarModule,
        MatListModule,
        MatGridListModule,
        MatStepperModule,
        MatExpansionModule,
        MatButtonToggleModule,
        MatChipsModule,
        MatIconModule,
        MatProgressSpinnerModule,
        MatProgressBarModule,
        MatDialogModule,
        MatTooltipModule,
        MatSnackBarModule,
        MatTableModule,
        MatSortModule,
        MatPaginatorModule

    ],
    exports: [
        MatTabsModule,
        MatButtonModule,
        MatToolbarModule,
        MatIconModule,
        MatSidenavModule,
        MatBadgeModule,
        MatListModule,
        MatGridListModule,
        MatInputModule,
        MatFormFieldModule,
        MatSelectModule,
        MatRadioModule,
        MatDatepickerModule,
        MatChipsModule,
        MatTooltipModule,
        MatTableModule,
        MatPaginatorModule,
        MatCardModule,
    ],
    providers: [
        MatDatepickerModule,
    ]
} )

export class AngularMaterialModule { }
