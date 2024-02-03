import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

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
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
