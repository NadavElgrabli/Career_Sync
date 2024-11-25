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
  filteredJobs!: UserJob[];
  filterOption: string = 'all';
  loading: boolean = false;

  constructor(
    private sessionService: SessionService,
    private httpService: HttpService
  ) {}

  ngOnInit(): void {
    this.user = this.sessionService.getUserFromSession();
    this.get_jobs()
  }

  get_jobs(): void {
    this.httpService
      .post<any>('jobs', { username: this.user.username })
      .subscribe((response) => {
        this.jobs = response.jobs;
        this.filteredJobs = [...this.jobs]; 
      });
  }

  filterJobs(): void {
    if (this.filterOption === 'applied') {
      this.filteredJobs = this.jobs.filter((job) => job.applied);
    } else if (this.filterOption === 'not-applied') {
      this.filteredJobs = this.jobs.filter((job) => !job.applied);
    } else {
      this.filteredJobs = [...this.jobs];
    }
  }

  newJobSearch(): void {
    this.loading = true;
    this.httpService.get('user/newjobs').subscribe(
      () => {
        this.get_jobs();
        this.loading = false;
      },
      (error) => {
        console.error(`Error:`, error);
        this.loading = false;
      }
    );
  }

  removeJob(job_id: string): void {
    this.jobs = this.jobs.filter((job) => job.job_id !== job_id);
    this.filterJobs();
    
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
