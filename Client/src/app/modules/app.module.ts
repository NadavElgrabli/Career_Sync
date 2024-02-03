import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatStepperModule } from '@angular/material/stepper';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from '../app.component';
import { HomePageComponent } from '../components/home-page/home-page.component';
import { NavBarComponent } from '../components/nav-bar/nav-bar.component';
import { SignUpComponent } from '../components/sign-up/sign-up.component';
import { ChatBtnComponent } from '../components/chat-btn/chat-btn.component';
import { CareersPageComponent } from '../components/careers-page/careers-page.component';
import { AboutComponent } from '../components/about/about.component';
import { ChatComponent } from '../components/chat/chat.component';
import { SignInComponent } from '../components/sign-in/sign-in.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    NavBarComponent,
    SignUpComponent,
    ChatBtnComponent,
    CareersPageComponent,
    AboutComponent,
    ChatComponent,
    SignInComponent,
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
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
