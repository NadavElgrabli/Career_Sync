import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  private baseUrl = 'http://127.0.0.1:5000/';
  constructor(private http: HttpClient) {}
  
  get<T>(url: string): Observable<T> {
    return this.http.get<T>(this.baseUrl + url);
  }

  post<T>(url: string, data: any): Observable<T> {
    return this.http.post<T>(this.baseUrl + url, data);
  }


  put<T>(url: string, data: any): Observable<T> {
    return this.http.put<T>(this.baseUrl + url, data);
  }

  delete<T>(url: string): Observable<T> {
    return this.http.delete<T>(this.baseUrl + url);
  }
}
