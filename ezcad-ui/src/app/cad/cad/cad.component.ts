import { Component, OnInit } from '@angular/core';
import { SkThreeBounceComponent } from 'ng-http-loader';
import { ApiService } from 'src/app/api.service';


@Component({
  selector: 'app-cad',
  templateUrl: './cad.component.html',
  styleUrls: ['./cad.component.css']
})
export class CadComponent implements OnInit {
  constructor(private api: ApiService) { }

  current: any = null; // Current unit
  tencodes: any;
  disabledButtons: any;

  ngOnInit(): void {
    this.api.getTenCodes().subscribe((response) => this.tencodes = response);
    this.api.getCurrentUnit().subscribe((response) => {
      this.current = response;
      this.disabledButtons = {
        0: (this.current.status == 0),
        1: (this.current.status == 1),
        2: (this.current.status == 2),
        3: (this.current.status == 3),
        4: this.current.status == 4,
        5: this.current.currentCall == null,
        6: this.current.currentCall == null,
        7: this.current.currentCall == null
      }
    });
  
  }

  changeStatus(statusId: number) {
    this.current.status = statusId;
    this.api.changeCurrentUnitStatus(statusId).subscribe();
    this.disabledButtons = {
      0: (this.current.status == 0),
      1: (this.current.status == 1),
      2: (this.current.status == 2),
      3: (this.current.status == 3),
      4: this.current.status == 4,
      5: this.current.currentCall == null,
      6: this.current.currentCall == null,
      7: this.current.currentCall == null
    }
  }  

}
