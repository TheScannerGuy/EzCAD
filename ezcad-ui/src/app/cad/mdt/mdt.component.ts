import { Component, OnInit, Pipe, PipeTransform } from '@angular/core';
import { ApiService } from 'src/app/api.service';


@Component({
  selector: 'mdt',
  templateUrl: './mdt.component.html',
  styleUrls: ['./mdt.component.css'],
})
export class MdtComponent {
  constructor(private api: ApiService) { }
  fnValue=''; lnValue=''; plateValue='';
  personDetails = {
    'First Name': 'first_name',
    'Last Name': 'last_name',
    'Date of Birth': 'date_of_birth',
    'Address': 'address',
    'Eyes': 'eyes',
    'Height': 'height',
    'Race': 'race',
    'Sex': 'sex'
  }
  personResult: any;
  vehicleResult: any;

  queryRecords(type: number, data: any) {
    switch (type) {
      // Person Query
      case 0:
        this.api.getPerson(data["firstName"], data["lastName"]).subscribe(
          (response) => this.personResult = response
        );

        break;

      // Vehicle Query
      case 1:
        this.api.getVehicle(data["plate"]).subscribe(
          (response) => this.vehicleResult = response
        );

        break;

    }
  }



}
