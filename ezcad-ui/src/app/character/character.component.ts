import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

let allCharacters: any;


@Component({
  selector: 'app-character',
  templateUrl: './character.component.html',
  styleUrls: ['./character.component.css']
})
export class CharacterComponent implements OnInit {
  constructor(private api: ApiService, private dialog: MatDialog) { }

  selectedCharacter: any;

  openDialog(): void {
    const dialogRef = this.dialog.open(CharacterComponent, {
      width: '250px',
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.selectedCharacter = result;
    });
  }

  ngOnInit(): void {
    this.api.getCurrentUserCharacters().subscribe(
      (response) => {
        allCharacters = response;
        this.openDialog();
      }
    );
  }

}
