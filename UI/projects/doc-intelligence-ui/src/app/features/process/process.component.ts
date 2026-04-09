import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { Subject, interval, takeUntil } from 'rxjs';
import { DocumentService } from '../../shared/services/document.service';
import { NotificationService } from '../../shared/services/notification.service';
import { ProcessingStatus } from '../../shared/models';

interface PipelineStage {
  id: string;
  name: string;
  icon: string;
  status: 'pending' | 'active' | 'complete' | 'error';
  progress: number;
  duration: number;
}

@Component({
  selector: 'app-process',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div class="max-w-5xl mx-auto px-4 py-12">
        <!-- Header -->
        <div class="mb-10">
          <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent mb-2">
            Processing Pipeline
          </h1>
          <p class="text-gray-600" *ngIf="documentId">Document ID: <code class="bg-blue-50 text-blue-700 px-3 py-1 rounded text-sm font-mono">{{ documentId }}</code></p>
        </div>

        <!-- Overall Progress Card -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-12 hover:shadow-md transition-shadow">
          <div class="bg-gradient-to-r from-blue-50 to-cyan-50 px-8 py-6 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-blue-900">Overall Progress</h2>
                <p class="text-sm text-blue-700 mt-1">{{ overallProgress }}% Complete</p>
              </div>
              <div class="text-right">
                <p class="text-5xl font-bold text-blue-600">{{ overallProgress }}%</p>
              </div>
            </div>
          </div>

          <div class="p-8">
            <!-- Main Progress Bar -->
            <div class="mb-8">
              <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden shadow-sm">
                <div
                  class="bg-gradient-to-r from-blue-500 to-blue-600 h-4 rounded-full transition-all duration-500 shadow-lg"
                  [style.width.%]="overallProgress"
                ></div>
              </div>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="bg-gradient-to-br from-green-50 to-emerald-50 p-6 rounded-lg border border-green-200 hover:shadow-md transition-all">
                <p class="text-sm font-semibold text-green-700 uppercase tracking-wide">Stages Completed</p>
                <div class="flex items-end gap-2 mt-3">
                  <p class="text-4xl font-bold text-green-600">{{ completedStages }}<span class="text-xl text-green-500">/{{ totalStages }}</span></p>
                </div>
                <p class="text-xs text-green-700 mt-2">✓ Done</p>
              </div>

              <div class="bg-gradient-to-br from-blue-50 to-cyan-50 p-6 rounded-lg border border-blue-200 hover:shadow-md transition-all">
                <p class="text-sm font-semibold text-blue-700 uppercase tracking-wide">In Progress</p>
                <div class="flex items-end gap-2 mt-3">
                  <p class="text-4xl font-bold text-blue-600">{{ activeStages }}</p>
                </div>
                <p class="text-xs text-blue-700 mt-2">⏳ Processing</p>
              </div>

              <div class="bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-lg border border-purple-200 hover:shadow-md transition-all">
                <p class="text-sm font-semibold text-purple-700 uppercase tracking-wide">Time Remaining</p>
                <div class="flex items-end gap-1 mt-3">
                  <p class="text-4xl font-bold text-purple-600">{{ remainingTime }}<span class="text-lg text-purple-500">s</span></p>
                </div>
                <p class="text-xs text-purple-700 mt-2">Estimated</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Pipeline Stages -->
        <div class="space-y-4 mb-12">
          <div
            *ngFor="let stage of stages; let i = index"
            class="bg-white rounded-xl shadow-sm border-l-4 overflow-hidden hover:shadow-md transition-all duration-200 group"
            [ngClass]="{
              'border-l-blue-600': stage.status === 'active',
              'border-l-green-600': stage.status === 'complete',
              'border-l-gray-300': stage.status === 'pending',
              'border-l-red-600': stage.status === 'error'
            }"
          >
            <div class="p-6">
              <!-- Stage Header -->
              <div class="flex items-start justify-between mb-6">
                <div class="flex items-center gap-4">
                  <!-- Status Icon -->
                  <div class="w-14 h-14 rounded-xl flex items-center justify-center text-2xl font-semibold group-hover:scale-110 transition-transform"
                    [ngClass]="{
                      'bg-blue-100 text-blue-600': stage.status === 'active',
                      'bg-green-100 text-green-600': stage.status === 'complete',
                      'bg-gray-100 text-gray-600': stage.status === 'pending',
                      'bg-red-100 text-red-600': stage.status === 'error'
                    }">
                    <span *ngIf="stage.status === 'active'">⏳</span>
                    <span *ngIf="stage.status === 'complete'">✓</span>
                    <span *ngIf="stage.status === 'pending'">{{ i + 1 }}</span>
                    <span *ngIf="stage.status === 'error'">✕</span>
                  </div>

                  <!-- Stage Info -->
                  <div class="flex-1">
                    <h3 class="text-lg font-bold text-gray-900">{{ stage.name }}</h3>
                    <p class="text-sm text-gray-600 mt-1">
                      <span *ngIf="stage.status === 'active'" class="text-blue-600 font-semibold">⟳ Processing...</span>
                      <span *ngIf="stage.status === 'complete'" class="text-green-600 font-semibold">✓ Completed in {{ stage.duration }}s</span>
                      <span *ngIf="stage.status === 'pending'" class="text-gray-500">⏸ Waiting to start</span>
                      <span *ngIf="stage.status === 'error'" class="text-red-600 font-semibold">✕ Failed</span>
                    </p>
                  </div>
                </div>

                <!-- Progress Percentage Badge -->
                <div class="text-right">
                  <div class="inline-block px-4 py-2 rounded-lg font-bold text-lg"
                    [ngClass]="{
                      'bg-blue-100 text-blue-600': stage.status === 'active',
                      'bg-green-100 text-green-600': stage.status === 'complete',
                      'bg-gray-100 text-gray-600': stage.status === 'pending',
                      'bg-red-100 text-red-600': stage.status === 'error'
                    }">
                    {{ stage.progress }}%
                  </div>
                </div>
              </div>

              <!-- Progress Bar -->
              <div class="mb-4">
                <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden shadow-sm">
                  <div
                    class="h-3 rounded-full transition-all duration-500"
                    [style.width.%]="stage.progress"
                    [ngClass]="{
                      'bg-gradient-to-r from-blue-400 to-blue-600': stage.status === 'active',
                      'bg-gradient-to-r from-green-400 to-green-600': stage.status === 'complete',
                      'bg-gray-300': stage.status === 'pending',
                      'bg-gradient-to-r from-red-400 to-red-600': stage.status === 'error'
                    }"
                  ></div>
                </div>
              </div>

              <!-- Loading Animation for Active Stage -->
              <div *ngIf="stage.status === 'active'" class="flex gap-2">
                <div class="w-2 h-2 rounded-full bg-blue-600 animate-bounce" style="animation-delay: 0s"></div>
                <div class="w-2 h-2 rounded-full bg-blue-600 animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 rounded-full bg-blue-600 animate-bounce" style="animation-delay: 0.2s"></div>
                <span class="text-sm text-blue-600 font-medium ml-2">Processing...</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Processing Statistics -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <div class="bg-gradient-to-br from-blue-50 to-cyan-50 p-8 rounded-xl border border-blue-200 shadow-sm hover:shadow-md transition-all">
            <p class="text-sm font-bold text-blue-700 uppercase tracking-wider">Total Elapsed Time</p>
            <p class="text-5xl font-bold text-blue-600 mt-4">{{ totalElapsedTime }}<span class="text-2xl text-blue-500">s</span></p>
            <div class="mt-4 pt-4 border-t border-blue-200">
              <p class="text-xs text-blue-700">All stages combined</p>
            </div>
          </div>

          <div class="bg-gradient-to-br from-purple-50 to-pink-50 p-8 rounded-xl border border-purple-200 shadow-sm hover:shadow-md transition-all">
            <p class="text-sm font-bold text-purple-700 uppercase tracking-wider">Current Stage</p>
            <p class="text-2xl font-bold text-purple-600 mt-4 capitalize">{{ currentStageStatus }}</p>
            <div class="mt-4 pt-4 border-t border-purple-200">
              <p class="text-xs text-purple-700">Stage {{ completedStages + activeStages + 1 }} of {{ totalStages }}</p>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-4">
          <button
            *ngIf="!isComplete"
            (click)="cancelProcessing()"
            class="flex-1 px-6 py-4 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-bold transition-all transform hover:scale-105 shadow-sm"
          >
            ✕ Cancel Processing
          </button>
          <button
            *ngIf="isComplete"
            (click)="goToResults()"
            class="flex-1 px-6 py-4 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-lg hover:from-green-700 hover:to-green-800 font-bold transition-all transform hover:scale-105 shadow-md hover:shadow-lg"
          >
            → View Results
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      @keyframes bounce {
        0%, 100% {
          transform: translateY(0);
        }
        50% {
          transform: translateY(-4px);
        }
      }

      .animate-bounce {
        animation: bounce 1.4s infinite;
      }

      :host {
        display: block;
      }
    `
  ]
})
export class ProcessComponent implements OnInit, OnDestroy {
  documentId: string | null = null;
  stages: PipelineStage[] = [
    { id: 'extract', name: 'Text Extraction', icon: '📝', status: 'pending', progress: 0, duration: 0 },
    { id: 'classify', name: 'Document Classification', icon: '🏷️', status: 'pending', progress: 0, duration: 0 },
    { id: 'extract-fields', name: 'Field Extraction', icon: '📋', status: 'pending', progress: 0, duration: 0 },
    { id: 'validate', name: 'Data Validation', icon: '✓', status: 'pending', progress: 0, duration: 0 },
    { id: 'summarize', name: 'Generate Summary', icon: '📄', status: 'pending', progress: 0, duration: 0 }
  ];

  overallProgress = 0;
  completedStages = 0;
  activeStages = 0;
  totalStages = 5;
  remainingTime = 0;
  totalElapsedTime = 0;
  currentStageStatus = 'pending';
  isComplete = false;

  private destroy$ = new Subject<void>();
  private simulationSubscription: any;
  private currentStageIndex = 0;

  constructor(
    private route: ActivatedRoute,
    private documentService: DocumentService,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      this.documentId = params.get('id');
    });

    // Start processing simulation
    this.startProcessingSimulation();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    if (this.simulationSubscription) {
      this.simulationSubscription.unsubscribe();
    }
  }

  private startProcessingSimulation(): void {
    let stageDurations = [8, 5, 12, 6, 4]; // seconds per stage
    this.currentStageIndex = 0;

    interval(100)
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        if (this.currentStageIndex < this.stages.length) {
          const currentStage = this.stages[this.currentStageIndex];
          const stageDuration = stageDurations[this.currentStageIndex];

          // Start stage if not already started
          if (currentStage.status === 'pending') {
            currentStage.status = 'active';
            this.activeStages = 1;
            this.currentStageStatus = currentStage.name;
            this.notificationService.info(`Started: ${currentStage.name}`);
          }

          // Update progress
          if (currentStage.status === 'active') {
            currentStage.progress = Math.min(currentStage.progress + Math.random() * 15, 95);
            this.totalElapsedTime = Math.round(this.totalElapsedTime + 0.1);

            // Check if stage should complete
            const stageProgress = (currentStage.progress + Math.random() * 10) / 100;
            const expectedProgress = (this.totalElapsedTime) / (stageDurations.reduce((a, b) => a + b, 0));

            if (stageProgress > 0.9 || this.totalElapsedTime > stageDuration * this.currentStageIndex + stageDuration) {
              currentStage.progress = 100;
              currentStage.status = 'complete';
              currentStage.duration = stageDuration;
              this.completedStages++;
              this.activeStages = 0;
              this.currentStageIndex++;

              if (this.currentStageIndex < this.stages.length) {
                this.notificationService.success(`Completed: ${currentStage.name}`);
              }
            }
          }

          // Calculate overall progress
          this.overallProgress = Math.round(
            (this.stages.reduce((sum, s) => sum + s.progress, 0) / (this.totalStages * 100)) * 100
          );

          // Calculate remaining time
          const remainingStages = this.stages.slice(this.currentStageIndex);
          this.remainingTime = Math.max(0, Math.round(
            remainingStages.reduce((sum, _, i) => sum + (stageDurations[this.currentStageIndex + i] || 0), 0) - 
            (this.totalElapsedTime - stageDurations.slice(0, this.currentStageIndex).reduce((a, b) => a + b, 0))
          ));
        } else if (!this.isComplete) {
          // All stages complete
          this.isComplete = true;
          this.overallProgress = 100;
          this.activeStages = 0;
          this.remainingTime = 0;
          this.notificationService.success('All processing stages completed!');
        }
      });
  }

  cancelProcessing(): void {
    this.destroy$.next();
    this.notificationService.warning('Processing cancelled');
  }

  goToResults(): void {
    // Navigate to results page (would use Router in real implementation)
    this.notificationService.info('Navigating to results...');
  }
}
