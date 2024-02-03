import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AppComponent } from 'src/app/app.component';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent {

  signUpForm: FormGroup;
  gender!: string;
  hide = true;
  skills: string[] = ["Python", "JavaScript", "Java", "C++", "HTML/CSS", "SQL", "Git", "Data Structures", "Algorithms", "Object-Oriented Programming", "Web Development", "Backend Development", "Frontend Development", "Mobile Development", "React", "Angular", "Vue.js", "Node.js", "Express.js", "RESTful APIs", "Databases", "UI/UX Design", "Test-Driven Development", "Agile Methodologies", "CI/CD", "DevOps", "Cloud Computing", "Cybersecurity", "Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision", "Big Data", "Blockchain", "IoT"];
  selectedSkills: string[] = [];
  
  constructor(private formBuilder: FormBuilder, private appComponentParent: AppComponent) {
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
      this.selectedSkills.splice(index, 1); // Deselect the button if already selected
    } else {
      this.selectedSkills.push(str); // Select the button if not already selected
    }
  }

  isSelected(str: string): boolean {
    return this.selectedSkills.includes(str);
  }

  isFormInvalid(): boolean {
    return this.signUpForm && this.signUpForm.invalid;
  }
}
