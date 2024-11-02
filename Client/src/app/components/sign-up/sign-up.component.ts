import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AppComponent } from 'src/app/app.component';
import { HttpService } from 'src/app/services/http.service';
import { User } from 'src/app/user';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
})
export class SignUpComponent {
  user!: User;
  signUpForm: FormGroup;
  hidePassword = true; // Track password visibility
  hideConfirmPassword = true; // Track confirm password visibility

  constructor(
    private formBuilder: FormBuilder,
    private appComponentParent: AppComponent,
    private httpService: HttpService,
    private router: Router
  ) {
    this.appComponentParent.displayNavbar = false;

    this.signUpForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.pattern('^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{6,}$')]],
      confirmPassword: ['', Validators.required],
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
    }, { validators: this.passwordMatchValidator }); // Custom validator for matching passwords
  }

  // Custom validator to check if passwords match
  passwordMatchValidator(form: FormGroup) {
    return form.get('password')?.value === form.get('confirmPassword')?.value ? null : { mismatch: true };
  }

  isFormInvalid(): boolean {
    return this.signUpForm.invalid; // Return true if the form is invalid
  }

  createAccount() {
    // Ensure the form is valid before creating the account
    if (this.signUpForm.valid) {
      this.user = {
        ...this.signUpForm.value,
      };
      this.httpService.post<User>('signup', this.user).subscribe((res) => {
        this.router.navigate(['/']);
      });
    } else {
      console.error('Form is invalid'); // Optional: log the error
    }
  }

  togglePasswordVisibility() {
    this.hidePassword = !this.hidePassword;
  }

  toggleConfirmPasswordVisibility() {
    this.hideConfirmPassword = !this.hideConfirmPassword;
  }
}
