import { Component } from '@angular/core';
import { AppComponent } from 'src/app/app.component';
import { SessionService } from 'src/app/services/sessionService';
import { User } from 'src/app/user';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent {
  isSignInVisible : boolean = false;
  user !: User;

  constructor(private sessionService: SessionService, private appComponentParent:AppComponent,) { }

  ngOnInit(){
    this.user = this.sessionService.getUserFromSession();
    console.log(this.user);
  }

  logout(){
    this.sessionService.logout();
    this.user = this.sessionService.getUserFromSession();
    this.appComponentParent.user = this.user;
  }
}
