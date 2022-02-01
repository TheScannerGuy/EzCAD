import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/api.service';
import { AngularMaterialModule } from 'src/app/material.module';
import { last, lastValueFrom } from 'rxjs';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {
  constructor(private api: ApiService) { }


  ngOnInit(): void {
  }

}
