import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatStepperModule } from '@angular/material/stepper';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatCardModule } from '@angular/material/card';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from '../app.component';
import { HomePageComponent } from '../components/home-page/home-page.component';
import { NavBarComponent } from '../components/nav-bar/nav-bar.component';
import { SignUpComponent } from '../components/sign-up/sign-up.component';
import { CareersPageComponent } from '../components/careers-page/careers-page.component';
import { AboutComponent } from '../components/about/about.component';
import { ChatComponent } from '../components/chat/chat.component';
import { SignInComponent } from '../components/sign-in/sign-in.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { JobCardComponent } from '../components/job-card/job-card.component';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    NavBarComponent,
    SignUpComponent,
    CareersPageComponent,
    AboutComponent,
    ChatComponent,
    SignInComponent,
    JobCardComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatStepperModule,
    MatInputModule,
    MatButtonModule,
    MatFormFieldModule,
    BrowserAnimationsModule,
    MatIconModule,
    ReactiveFormsModule,
    MatPaginatorModule,
    MatCardModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
