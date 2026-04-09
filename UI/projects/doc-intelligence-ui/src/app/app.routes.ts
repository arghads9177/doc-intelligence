import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/upload',
    pathMatch: 'full'
  },
  {
    path: 'upload',
    loadComponent: () =>
      import('./features/upload/upload.component').then(
        (m) => m.UploadComponent
      ),
    data: { title: 'Upload Documents' }
  },
  {
    path: 'process/:id',
    loadComponent: () =>
      import('./features/process/process.component').then(
        (m) => m.ProcessComponent
      ),
    data: { title: 'Processing' }
  },
  {
    path: 'results/:id',
    loadComponent: () =>
      import('./features/results/results.component').then(
        (m) => m.ResultsComponent
      ),
    data: { title: 'Results' }
  },
  {
    path: 'history',
    loadComponent: () =>
      import('./features/history/history.component').then(
        (m) => m.HistoryComponent
      ),
    data: { title: 'History' }
  },
  {
    path: 'settings',
    loadComponent: () =>
      import('./features/settings/settings.component').then(
        (m) => m.SettingsComponent
      ),
    data: { title: 'Settings' }
  },
  {
    path: '**',
    redirectTo: '/upload'
  }
];
