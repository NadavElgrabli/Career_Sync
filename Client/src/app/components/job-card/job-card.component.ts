import { Component, Input , Output, EventEmitter} from '@angular/core';
import { UserJob } from 'src/app/interfaces/job';
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
  @Output() removeJob = new EventEmitter<string>();

  onRemoveJob(): void {
    this.removeJob.emit(this.job.job_id);
  }

  constructor(
    private httpService: HttpService,
    private sessionService: SessionService
  ) {}

  ngOnInit(): void {
    this.user = this.sessionService.getUserFromSession();
    
  }

  getScoreClass(score: number): string {
    if (score >= 80) {
        return 'badge-high';
    } else if (score >= 50) {
        return 'badge-medium';
    } else {
        return 'badge-low';
    }
}



  toggleSubmitted(job: UserJob): void {
    this.httpService.put<any>(`jobs/${job.job_id}`, { username: this.user.username }).subscribe(res => {
        job.applied = res.job.applied;
        console.log(res.job.applied)
    });
}

}