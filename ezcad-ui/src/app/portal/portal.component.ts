import { Injectable } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { ApiService } from '../api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-portal',
  templateUrl: './portal.component.html',
  styleUrls: ['./portal.component.css']
})

export class PortalComponent implements OnInit {
  constructor(private api: ApiService, private router: Router) { }

  submitted = false;
  ready = false;

  current: any;

  onSubmit(data: any) { 
    this.api.registerUnit(data.department, data.unit).subscribe();
    this.api.getDepartment(data.department).subscribe(
      (response: any) => {
        switch (response.type) {
          case 0:
            this.router.navigateByUrl('/cad/unit')
            break;
          case 2:
            this.router.navigateByUrl('/cad/dispatch');
            break;
        }
      }
    )
  }

  ngOnInit(): void {
    this.api.getCurrentUser().subscribe(data => this.current = data);    
    this.ready = true;
  }
}
