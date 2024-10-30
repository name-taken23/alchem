import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { interval, Subscription } from 'rxjs';
import { EventService } from '../services/event-service.service';

interface EventData {
  id: number;
  event_name: string;
  status: string;
  last_updated: string;
}

@Component({
  selector: 'app-event-status',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './event-status.component.html',
  styleUrls: ['./event-status.component.css']
})
export class EventStatusComponent implements OnInit, OnDestroy {
  events: EventData[] = [];
  totalEvents = 0;
  currentPage = 1;
  itemsPerPage = 10;
  totalPages = 0;
  maxPageButtons = 5;
  private refreshInterval = 5000;
  private subscription: Subscription | undefined;

  constructor(private eventService: EventService) { }

  ngOnInit(): void {
    this.fetchEvents();
    this.subscription = interval(this.refreshInterval).subscribe(() => this.fetchEvents());
  }

  fetchEvents(): void {
    this.eventService.fetchEvents(this.currentPage, this.itemsPerPage)
      .subscribe(
        response => {
          this.events = response.events;
          this.totalEvents = response.total_count;
          this.totalPages = Math.ceil(this.totalEvents / this.itemsPerPage);
        },
        error => console.error('Error fetching events:', error)
      );
  }

  goToPreviousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.fetchEvents();
    }
  }

  goToNextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.fetchEvents();
    }
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.fetchEvents();
    }
  }

  getPageRange(): number[] {
    const start = Math.max(1, this.currentPage - Math.floor(this.maxPageButtons / 2));
    const end = Math.min(this.totalPages, start + this.maxPageButtons - 1);

    const adjustedStart = Math.max(1, end - this.maxPageButtons + 1);
    return Array.from({ length: end - adjustedStart + 1 }, (_, i) => adjustedStart + i);
  }

  updateEventStatus(eventId: number, newStatus: string): void {
    this.eventService.updateEventStatus(eventId, newStatus)
      .subscribe(
        () => {
          console.log(`Event ID ${eventId} updated to status: ${newStatus}`);
          this.fetchEvents();
        },
        error => console.error('Error updating event:', error)
      );
  }

  statusClass(status: string): string {
    switch (status) {
      case 'Pending':
        return 'status status-pending';
      case 'In Progress':
        return 'status status-in-progress';
      case 'Completed':
        return 'status status-completed';
      default:
        return 'status';
    }
  }

  ngOnDestroy(): void {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}
