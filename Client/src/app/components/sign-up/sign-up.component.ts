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
  hidePassword = true;
  hideConfirmPassword = true;
  errorMessage: string | null = null; // Add this property

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
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
    }, { validators: this.passwordMatchValidator });
  }

  passwordMatchValidator(form: FormGroup) {
    return form.get('password')?.value === form.get('confirmPassword')?.value ? null : { mismatch: true };
  }

  isFormInvalid(): boolean {
    return this.signUpForm.invalid;
  }

  createAccount() {
    if (this.signUpForm.valid) {
      this.user = {
        ...this.signUpForm.value,
      };
      this.httpService.post<User>('signup', this.user).subscribe({
        next: (res) => {
          this.router.navigate(['/']);
        },
        error: (err) => {
          this.errorMessage = 'Failed to create account. Please check your details and try again.';
        }
      });
    } else {
      this.errorMessage = 'Please fill out all required fields correctly.';
    }
  }

  togglePasswordVisibility() {
    this.hidePassword = !this.hidePassword;
  }

  toggleConfirmPasswordVisibility() {
    this.hideConfirmPassword = !this.hideConfirmPassword;
  }
}
