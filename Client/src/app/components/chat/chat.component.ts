import { Component, OnInit } from '@angular/core';
import { Msg } from 'src/app/interfaces/msg';
import { SessionService } from 'src/app/services/sessionService';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})

export class ChatComponent implements OnInit {
  messages: Msg[] = [];
  newMessage: string = '';

  constructor(private sessionService: SessionService) {}

  ngOnInit(): void {}

  isLoggedIn(): boolean {
    return this.sessionService.getUserFromSession() !== null;
  }

  sendMessage() {
    if (this.newMessage.trim() !== '') {
      const message: Msg = { text: this.newMessage.trim() };
      this.messages.push(message);
      console.log(message);
      this.newMessage = '';
    }
  }
}