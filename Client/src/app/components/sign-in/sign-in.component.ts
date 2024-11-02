import { Component } from '@angular/core';
import { NavBarComponent } from '../nav-bar/nav-bar.component';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpService } from 'src/app/services/http.service';
import { User } from 'src/app/user';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent {

  signInForm: FormGroup;
  hide = true;
  user!: User;
  errorMessage: string | null = null; // Added property for error message

  constructor(private parent: NavBarComponent, private formBuilder: FormBuilder, private httpService: HttpService) {
    this.signInForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  login() {
    this.errorMessage = null; // Clear any previous error message
    this.httpService.post<any>('login', this.signInForm.value).subscribe(
      res => {
        localStorage.setItem('token', res.token);
        localStorage.setItem('user', JSON.stringify(res.user));
        this.user = res.user;
        this.parent.user = this.user;
        this.isSignInVisible();
      },
      err => {
        this.errorMessage = 'Invalid username or password. Please try again.';
      }
    );
  }

  isSignInVisible() {
    this.parent.isSignInVisible = !this.parent.isSignInVisible;
  }
}
