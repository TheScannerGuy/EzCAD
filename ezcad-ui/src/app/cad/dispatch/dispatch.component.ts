import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/api.service';


@Component({
  selector: 'app-dispatch',
  templateUrl: './dispatch.component.html',
  styleUrls: ['./dispatch.component.css']
})
export class DispatchComponent implements OnInit {
  constructor(private api: ApiService) { }
  socket: any;

  unitSource: any;
  unitTableCols: string[] = ['unitId', 'status', 'assignment']
  tencodes: any;

  ngOnInit(): void {
    this.api.getAllUnits().subscribe((response) => this.unitSource = response);
    this.api.getTenCodes().subscribe((response) => this.tencodes = response);
  }
  
}
