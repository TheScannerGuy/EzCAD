import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/api.service';

@Component({
  selector: 'cad-create-job',
  templateUrl: './create-job.component.html',
  styleUrls: ['./create-job.component.css']
})
export class CreateJobComponent implements OnInit {
  constructor(private api: ApiService) { }

  callTypes: any;

  ngOnInit(): void {
    this.api.getCallTypes().subscribe((response) => this.callTypes = response);
  }

}
