import { Component } from '@angular/core';
import { AppComponent } from 'src/app/app.component';
import { Job } from 'src/app/interfaces/job';
import { SessionService } from 'src/app/services/sessionService';
import { User } from 'src/app/user';

@Component({
  selector: 'app-careers-page',
  templateUrl: './careers-page.component.html',
  styleUrls: ['./careers-page.component.css']
})
export class CareersPageComponent {
  user!: User;
  jobs: Job[] = [
    {
        title: 'Senior Software Engineer',
        url: 'https://example.com/apply',
        description: 'Develop and maintain software solutions.',
        organization: 'MyCompany',
        location: 'Tel Aviv',
        job_type: 'Full-time',
        job_preference: 'Remote',
        is_submitted: true
    },
    {
        title: 'Junior UI/UX Designer',
        url: 'https://example.com/apply',
        description: 'Design user interfaces and experiences.',
        organization: 'MyCompany',
        location: 'Haifa',
        job_type: 'Full-time',
        job_preference: 'On-Site',
        is_submitted: false
    }
  ];

  constructor(private sessionService: SessionService, private appComponentParent:AppComponent,) { }

  ngOnInit(){
    this.user = this.sessionService.getUserFromSession();
  }
}
