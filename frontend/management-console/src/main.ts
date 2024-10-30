import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter, Route } from '@angular/router';
import { importProvidersFrom } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app/app.component';
import { EventStatusComponent } from './app/event-status/event-status.component';

const routes: Route[] = [
  { path: '', redirectTo: '/event-status', pathMatch: 'full' },
  { path: 'event-status', component: EventStatusComponent }
];

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    importProvidersFrom(HttpClientModule)
  ]
}).catch(err => console.error(err));
