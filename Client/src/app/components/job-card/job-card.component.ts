import { Component, Input } from '@angular/core';
import { Job, UserJob } from 'src/app/interfaces/job';
import { HttpService } from 'src/app/services/http.service';
import { SessionService } from 'src/app/services/sessionService';
import { User } from 'src/app/user';

@Component({
  selector: 'app-job-card',
  templateUrl: './job-card.component.html',
  styleUrls: ['./job-card.component.css'],
})

export class JobCardComponent {
  @Input() job !: UserJob;
  user!: User;

  constructor(
    private httpService: HttpService,
    private sessionService: SessionService
  ) {}

  ngOnInit(): void {
    this.user = this.sessionService.getUserFromSession();
    
  }

  toggleSubmitted(job: UserJob): void {
    this.httpService.put<any>(`jobs/${job.job_id}`, { username: this.user.username }).subscribe(res => {
        job.applied = res.job.applied;
        console.log(res.job.applied)
    });
}

}