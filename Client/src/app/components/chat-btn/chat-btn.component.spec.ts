import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChatBtnComponent } from './chat-btn.component';

describe('ChatBtnComponent', () => {
  let component: ChatBtnComponent;
  let fixture: ComponentFixture<ChatBtnComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChatBtnComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChatBtnComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
