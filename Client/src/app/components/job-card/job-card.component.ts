import { Component, Input } from '@angular/core';
import { Job } from 'src/app/interfaces/job';

@Component({
  selector: 'app-job-card',
  templateUrl: './job-card.component.html',
  styleUrls: ['./job-card.component.css'],
})

export class JobCardComponent {
  @Input() job !: Job;

  toggleSubmitted(job: any): void {
    job.is_submitted = !job.is_submitted;
  }
}










