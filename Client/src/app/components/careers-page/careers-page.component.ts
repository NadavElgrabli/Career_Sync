import { Component, OnInit } from '@angular/core';
import { UserJob } from 'src/app/interfaces/job';
import { SessionService } from 'src/app/services/sessionService';
import { HttpService } from 'src/app/services/http.service';
import { User } from 'src/app/user';
import { HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-careers-page',
  templateUrl: './careers-page.component.html',
  styleUrls: ['./careers-page.component.css'],
})
export class CareersPageComponent implements OnInit {
  user!: User;
  jobs!: UserJob[];

  constructor(
    private sessionService: SessionService,
    private httpService: HttpService
  ) {}

  ngOnInit(): void {
    this.user = this.sessionService.getUserFromSession();
    this.httpService
      .post<any>('jobs', { username: this.user.username })
      .subscribe((response) => {
        this.jobs = response.jobs;
      });
  }

  removeJob(job_id: string): void {
    this.jobs = this.jobs.filter((job) => job.job_id !== job_id);

    const headers = new HttpHeaders({
      username: this.user.username,
    });

    this.httpService.post(`jobs/${job_id}`, { username: this.user.username }).subscribe(
      () => {
        console.log(`Job ${job_id} deleted successfully.`);
      },
      (error) => {
        console.error(`Error deleting job ${job_id}:`, error);
      }
    );
  }
}
