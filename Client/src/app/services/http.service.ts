import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  private baseUrl = 'http://127.0.0.1:5000/';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token') || '';
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  get<T>(url: string): Observable<T> {
    const headers = this.getHeaders();
    return this.http.get<T>(this.baseUrl + url, { headers });
  }

  post<T>(url: string, data: any): Observable<T> {
    const headers = this.getHeaders();
    return this.http.post<T>(this.baseUrl + url, data, { headers });
  }

  put<T>(url: string, data: any): Observable<T> {
    const headers = this.getHeaders();
    return this.http.put<T>(this.baseUrl + url, data, { headers });
  }

  delete<T>(url: string): Observable<T> {
    const headers = this.getHeaders();
    return this.http.delete<T>(this.baseUrl + url, { headers });
  }
}
