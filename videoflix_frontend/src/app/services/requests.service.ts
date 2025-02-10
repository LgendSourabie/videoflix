import { Injectable, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { ApiService } from './api.service';
import { Video } from '../modules/interfaces';
import { HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class RequestsService {
  private token: string | null = null;

  private videoSubject = new BehaviorSubject<Video | null>(null);
  videos$ = this.videoSubject.asObservable();

  private isLoadingSubject = new BehaviorSubject<boolean>(true);
  isLoading$ = this.isLoadingSubject.asObservable();

  private isErrorSubject = new BehaviorSubject<boolean>(false);
  isError$ = this.isErrorSubject.asObservable();

  private errorMessageSubject = new BehaviorSubject<{
    error_type: string | string[] | null[];
    error_message: string | string[] | null[];
  }>({ error_type: [null], error_message: [null] });

  errorMessage$ = this.errorMessageSubject.asObservable();

  private apiService = inject(ApiService);

  constructor(private router: Router, private route: ActivatedRoute) {}

  emitVideos(data: Video | null) {
    this.videoSubject.next(data);
  }

  emitIsLoading(bool: boolean) {
    this.isLoadingSubject.next(bool);
  }

  emitError(bool: boolean) {
    this.isErrorSubject.next(bool);
  }

  emitErrorMessage(message: any) {
    this.errorMessageSubject.next(message);
  }

  /**
   *
   * @param endpoint: string - API endpoint for fetching all videos
   * @param token : string - token of the authenticated user
   */
  fetchVideos(endpoint: string, token: string) {
    this.emitIsLoading(true);
    this.apiService.getData(endpoint, token).subscribe({
      next: (response) => {
        console.log('RESPONSE Body', response.body);
        this.emitVideos(response.body);
      },
      error: (error) => {
        this.emitErrorMessage(error.message);
      },
      complete: () => {
        this.emitIsLoading(false);
      },
    });
  }

  /**
   * fetch videos after changes in the UI
   */
  fetchUpdatedVideoData() {
    this.token = sessionStorage.getItem('token');
    if (this.token) {
      this.fetchVideos('api/videos/', this.token);
    }
  }

  /**
   * Generic method for handling all post requests
   * @param data - payload for the post request
   */
  postData(
    endpoint: string,
    data: any,
    header: HttpHeaders,
    callback: () => void
  ) {
    this.apiService.postData(endpoint, data, header).subscribe({
      next: (response) => {
        if (response.token) {
          this.fetchVideos('api/videos/', response.token);
          sessionStorage.setItem('token', response.token);
          callback();
        }
      },
      complete: () => {
        this.resetLoading(5000);
      },
      error: (error) => {
        if (error.status === 400 || error.status === 404) {
          console.log('error 1', error.error);

          this.emitError(error.error);
          this.resetLoading(0);
          return error.error;
        } else {
          console.log('error 2', error.message);
          this.emitError(error.message);
          this.resetLoading(0);
          return error.message;
        }
      },
    });
  }

  resetLoading(timestamp: number) {
    setTimeout(() => {
      this.emitIsLoading(false);
    }, timestamp);
  }

  goToPage(pageRoute: string) {
    const returnUrl = this.route.snapshot.queryParams['returnUrl'] || pageRoute;
    this.router.navigate([returnUrl]);
  }
}
