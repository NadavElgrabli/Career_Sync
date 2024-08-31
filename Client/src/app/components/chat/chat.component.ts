import { Component, OnInit } from '@angular/core';
import { SessionService } from 'src/app/services/sessionService';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})

export class ChatComponent implements OnInit {
  constructor(private sessionService: SessionService) {}

  ngOnInit(): void {}

  isLoggedIn(): boolean {
    return this.sessionService.getUserFromSession() !== null;
  }
}