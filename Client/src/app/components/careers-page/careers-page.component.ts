import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { AppComponent } from 'src/app/app.component';
import {  UserJob } from 'src/app/interfaces/job';
import { SessionService } from 'src/app/services/sessionService';
import { HttpService } from 'src/app/services/http.service';
import { User } from 'src/app/user';

@Component({
  selector: 'app-careers-page',
  templateUrl: './careers-page.component.html',
  styleUrls: ['./careers-page.component.css']
})
export class CareersPageComponent {

 
  user!: User;
  jobs!: UserJob[] 

  constructor(private sessionService: SessionService, private appComponentParent:AppComponent,private httpService: HttpService) { }

  ngOnInit(){
    this.user = this.sessionService.getUserFromSession();
    this.httpService.post<any>('jobs',{username: this.user.username}).subscribe(response => {
      this.jobs = response.jobs;
    });
  }
}
