import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventStatusComponent } from './event-status.component';

describe('EventStatusComponent', () => {
  let component: EventStatusComponent;
  let fixture: ComponentFixture<EventStatusComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EventStatusComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EventStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
