import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from '../components/home-page/home-page.component';
import { AboutComponent } from '../components/about/about.component';
import { CareersPageComponent } from '../components/careers-page/careers-page.component';

const routes: Routes = [
  { path: 'home-page', component: HomePageComponent },
  { path: 'about', component: AboutComponent },
  { path: 'careers-page', component: CareersPageComponent },
  { path: '**', redirectTo: 'home-page' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
