import { Component } from '@angular/core';
import { NavBarComponent } from '../nav-bar/nav-bar.component';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent {

  signInForm: FormGroup;
  hide = true;

  constructor(private parent: NavBarComponent, private formBuilder: FormBuilder){
    this.signInForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }
  
  isSignInVisible()
  {
    this.parent.isSignInVisible = !this.parent.isSignInVisible;
  }
}
