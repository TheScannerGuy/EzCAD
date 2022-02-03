import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from 'src/app/api.service';

@Component({
  selector: 'app-unit',
  templateUrl: './unit.component.html',
  styleUrls: ['./unit.component.css']
})
export class UnitComponent implements OnInit {
  constructor(private api: ApiService) { }

  tencodes: any;
  current: any;

  ngOnInit(): void {
    this.api.getTenCodes().subscribe((response) => this.tencodes = response);
    this.api.getCurrentUnit().subscribe((response) => this.current = response);
  }

}
