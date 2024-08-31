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
  gender!: string;
  hide = true;
  skills: string[] = [
    'Python',
    'JavaScript',
    'Java',
    'C++',
    'HTML/CSS',
    'SQL',
    'Git',
    'Data Structures',
    'Algorithms',
    'Object-Oriented Programming',
    'Web Development',
    'Backend Development',
    'Frontend Development',
    'Mobile Development',
    'React',
    'Angular',
    'Node.js',
    'Databases',
    'UI/UX Design',
    'DevOps',
    'Cloud Computing',
    'Cybersecurity',
  ];
  selectedSkills: string[] = [];

  constructor(
    private formBuilder: FormBuilder,
    private appComponentParent: AppComponent,
    private httpService: HttpService,
    private router: Router
  ) {
    this.appComponentParent.displayNavbar = false;

    this.signUpForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.pattern('.{6,}')]],
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
    });
  }

  toggleSelection(str: string): void {
    const index = this.selectedSkills.indexOf(str);
    if (index > -1) {
      this.selectedSkills.splice(index, 1);
    } else {
      this.selectedSkills.push(str);
    }
  }

  isSelected(str: string): boolean {
    return this.selectedSkills.includes(str);
  }

  isFormInvalid(): boolean {
    return this.signUpForm && this.signUpForm.invalid;
  }
  createAccount() {
    this.user = {
      ...this.signUpForm.value,
      gender: this.gender,
      skills: this.selectedSkills,
    };
    this.httpService.post<User>('signup', this.user).subscribe((res) => {
      this.router.navigate(['/']);
    });
  }
}
