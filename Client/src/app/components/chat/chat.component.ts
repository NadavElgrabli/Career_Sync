import { Component, OnInit } from '@angular/core';
import { Msg } from 'src/app/interfaces/msg';
import { HttpService } from 'src/app/services/http.service';
import { SessionService } from 'src/app/services/sessionService';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  messages: Msg[] = [];
  newMessage: string = '';

  constructor(
    private httpService: HttpService,
    private sessionService: SessionService
  ) {}

  ngOnInit(): void {
    this.httpService.post<any>('chat', { message: "start" }).subscribe(response => {
      const botMessage: Msg = { text: response.response, sender: 'bot' };
      this.messages.push(botMessage);
    });
  }

  isLoggedIn(): boolean {
    return this.sessionService.isLoggedIn();
  }

  sendMessage() {
    if (this.newMessage.trim() !== '') {
      const userMessage: Msg = { text: this.newMessage.trim(), sender: 'user' };
      this.messages.push(userMessage);

      this.httpService.post<any>('chat', { message: userMessage.text }).subscribe(response => {
        const botMessage: Msg = { text: response.response, sender: 'bot' };
        this.messages.push(botMessage);
      });

      this.newMessage = '';
    }
  }

  isUserMessage(message: Msg): boolean {
    return message.sender === 'user';
  }

  isBotMessage(message: Msg): boolean {
    return message.sender === 'bot';
  }
}
