import { Component } from '@angular/core';
import { NavBarComponent } from '../nav-bar/nav-bar.component';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent {
  constructor(private parent: NavBarComponent){}
  isSignInVisible()
  {
    this.parent.isSignInVisible = !this.parent.isSignInVisible;
  }
}
