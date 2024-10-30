import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

interface EventData {
  id: number;
  event_name: string;
  status: string;
  last_updated: string;
}

interface PaginatedResponse {
  events: EventData[];
  total_count: number;
}

@Injectable({
  providedIn: 'root',
})
export class EventService {
  private readonly eventServiceUrl = 'http://127.0.0.1:8000/api/events';

  constructor(private http: HttpClient) {}

  fetchEvents(page: number, pageSize: number): Observable<PaginatedResponse> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());
    return this.http.get<PaginatedResponse>(this.eventServiceUrl, { params });
  }

  updateEventStatus(eventId: number, newStatus: string): Observable<any> {
    const updateData = { status: newStatus };
    return this.http.put(`${this.eventServiceUrl}/${eventId}`, updateData);
  }
}
