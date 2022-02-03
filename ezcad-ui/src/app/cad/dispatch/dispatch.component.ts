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
  callTableCols: string[] = ['icon', 'sub-type', 'location', 'modify', 'delete']
  tencodes: any;
  calls: any;
  callIcons: any = {0: "local_police", 1: "local_fire_department", 3: "medical_services"}

  ngOnInit(): void {
    this.api.getAllUnits().subscribe((response) => this.unitSource = response);
    this.api.getTenCodes().subscribe((response) => this.tencodes = response);
    this.api.getAllCalls().subscribe((resposne) => this.calls = resposne);

  }

  changeStatus(unitId: string, status: number) {
    this.api.changeUnitStatus(unitId, status).subscribe();
  }

  attachUnit(unitId: string, callId: string) {
    this.api.attachUnit(callId, unitId).subscribe();
  }

  deleteCall(callId: string) {
    this.api.deleteCall(callId).subscribe();
  }
  
}
