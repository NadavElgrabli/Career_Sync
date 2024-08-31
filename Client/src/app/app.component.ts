import { Component } from '@angular/core';
import { SessionService } from './services/sessionService';
import { User } from './user';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Career_Sync';
  displayNavbar = true;
  user !: User;
  
  constructor(private sessionService: SessionService) { 
    this.user = this.sessionService.getUserFromSession();
  }
}
