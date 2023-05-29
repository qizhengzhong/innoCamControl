import axios from 'axios';
import { Component, ElementRef, ViewChild, OnInit } from '@angular/core';

interface Message {
  content: string;
  fromUser: boolean;
}

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss']
})
export class ChatbotComponent implements OnInit {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  public messages: Message[] = [];
  public question = '';
  public counter = 0;
  public response = [
    "I apologize, but the Mercedes Citaro model is not currently in our system. Would you like to add the Mercedes Citaro to our system?",
    "Alright, currently we have five production crafts available for similar models. Please select the corresponding crafts for manufacturing:<br>1. Bodywork<br>2. Engine manufacturing<br>3. Chassis manufacturing<br>4. Interior manufacturing<br>5. Final assembly and commissioning",
    "Okay, what is the desired quantity for this order?",
    "Please indicate the priority level for this order on a scale of 0 to 10, with 0 being the highest priority.",
    "Thank you, that's all I need. Please wait for a minute and I will generate the plan for you."]
  public apiUrl = 'https://api.openai.com/v1/chat/completions';
  public apiKey = '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';
  showImage: boolean = false;
  constructor() {}

  ngOnInit(): void {
    const message: Message = {
      content: "Hi this is Innocam chatbot, which type of bus model would you like to have manufactured?",
      fromUser: false
    };
    this.messages.push(message);
    this.scrollToBottom();
  }
  public async sendMessage(): Promise<void> {
    if (this.counter < this.response.length)
    {
      if (this.question.trim() === '') {
        return;
      }
      
      const message: Message = {
        content: this.question,
        fromUser: true
      };
  
      this.messages.push(message);
      this.scrollToBottom();
  
      const botResponse = this.response[this.counter];
      const botMessage: Message = {
        content: botResponse,
        fromUser: false
      };
  
      this.messages.push(botMessage);
      this.scrollToBottom();
      this.counter ++;
      this.question = '';
    }

    if (this.counter == this.response.length)
    {
      const allQuestions = [
        "A set of instructions on a bus factory assembly project  will be provided. You will store the provided information, and you won’t provide any answers to the initial prompt until asked otherwise.",
        "In a bus assembly factory, there are three separate production lines, which we call L1, L2 and L3. On the first production line (L1), there are five tasks, which we call T1, T2, T3a, T4a and T5, arranged in that order on the production line. On the second production line (L2), there are also five tasks, which we call T1, T2, T3b, T4b and T5, arranged in that order. On the third production line, there are six tasks, which we call T1, T2, T3a, T4b, T5 and T6, arranged in that order. The tasks that have the same names but placed on different production lines are the exact same tasks.\nAll tasks require at least one worker.  The baseline time required for a worker to complete each of the tasks is as follows: \n1.	T1 – 20 minutes\n2.	T2 – 15 minutes\n3.	T3a – 25 minutes\n4.	T3b – 20 minutes\n5.	T4a – 15 minutes\n6.	T4b – 12 minutes\n7.	T5 – 30 minutes\n8.	T6 – 60 minutes\nMore than one worker can work on a given task on any given line. If more than one worker works on a task, the baseline time to complete the task is reduced by dividing the number of workers working on that task by the baseline time required for a worker to complete the task.\nThe factory has 20 workers , which we call Wx, where x = (1,2,3,…20). The workers can move freely in the factory to all locations. The hourly wage rate is assumed to be $10/hour for all workers. However, for workers W19 and W20 they are paid $20/hour. Wages need to be paid even when workers are travelling between tasks and between production lines.  The workers are employed to operate the tasks on the production lines. Unless otherwise stated, all workers can work on all tasks on all production lines. Due to a lack of qualification and experience, workers W10-15 are not able to operate T6.  Workers W1-9 are specialised in tasks T3a and T4a, which means that they take 20% less time to complete these tasks the baseline time. However, for tasks T3b and T4b, they are hindered by their specialism, which means they will take 5% longer to complete these tasks than the baseline time. On the other hand, workers W10-18 specialise in the tasks of T3b and T4b, meaning they take 20% less time to complete these tasks than the baseline time. However, for tasks T3a and T4a, they are hindered by their specialism, which means they will take 3% longer to complete these tasks than the baseline time.  Workers T19 and T20 are very experienced, which means that they take 10% less time to complete any task than the baseline time. They are also leaders, hence if they work with any other workers on a given task on a given line, the particular task on that line will take 5% less time to complete, while all other tasks on that production line will take 2% less time to complete, compared to the baseline time.\nThe effects of worker specialisation and number of workers working on a task should be considered together when modelling the required time to complete a given task.\nEach bus goes on to the production line sequentially, and it takes 5 minutes  to load the bus onto any production line to prepare for production (setup time). As there are three production lines, at most only 3 new buses can be put on the production line at the same time. When one bus is in a more forward task on a given production line, buses cannot be placed in tasks further ahead on the production line. All new buses must start at the first task of any production line. It takes 30 minutes to remove a bus from a production line and costs $20 . When the bus is being removed from the line, all other tasks on that production line is temporarily halted. The removed bus can then be allocated to a new production line, starting at the first task on whichever line. Any task can be skipped if it had already been completed before, in which case the completion time would be 0 minutes. It does not take any time or cost to remove the bus when it reaches the final task of each line, as the production process is then complete.\nThere are four bus models that are to be manufactured. All models require a sequence of tasks to be applied in a specific order, and each task must be operated by at least one worker. The four models are:\n1.	A standard bus model, called B1. The assembly of B1 requires tasks T1, T2, either T3a or T3b (this means that T3a and T3b can substitute each other), either T4a or T4b (this means that T4a and T4b can substitute each other), and T5, in that order. \n2.	A long bus model, called B2. The assembly of B2 requires T1, T2, either T3a or T3b (this means that T3a and T3b can substitute each other), either T4a or T4b (this means that T4a and T4b can substitute each other), T5, and T6, in that order. \n3.	A double-decker bus model, called B3. The assembly of B3 requires T1, T2, T3a, T4b, either T5 or T6 (this means that T5 and T6 can substitute for each other). \n4.	A tourist double-decker bus model, called B4. The assembly of B3 requires T1, T2, T3a, T4b, T5, and T6.\nNow we have three customers who want to order some buses. Their orders are as follows:\n1.	Customer 1 orders 6 B1 buses\n\n2.	Customer 2 orders 1 B1 bus, 1 B2 bus and 2 B3 buses\n3.	Customer 3 orders 10 B1 buses, 1 B3 bus and 1 B4 bus\nCustomers’ orders can be mixed in production schedules.\nCan you come out with a production schedule in table format to assemble the buses, showing the tasks necessary and the workers allocated to each task, as well as the time taken for each task?\nPlease always proceed with generating the production schedule even if its taking time"
      ]

      const predefinedMessages: Message[] = [];
      var botResponse = "Line Task Workers Assigned Total TimeSpent(days) Cost<br>1 T1,B1 W1,W2,W3 20 20<br>1 T2+B1 W1,W2,W3 15 15<br>1 T3a/T3b+B1 W1,W2,W3,W10-15 15 15<br>1 T4a/T4b+B1 W1,W2,W3,W10-15 15 15<br>1 T5+B1 W1,W2,W3 30 30<br>2 T1+B1 W4,W5,W6 20 20<br>2 T2+B1+T1+B2 W4,W5,W6 15 20<br>2 T3a/T3b+B1+T2+B2 W4,W5,W6,W10-15 5 20<br>2 T4a/T4b+B1+T3a+B2 W4,W5,W6,W10-15 5 20<br>2 T5+B1+T4b+B2 W4,W5,W6 30 30<br>2 T6+B2 W4,W5,W6,W19,W20 60 60<br>3 T1+B1+T5+B3 W7,W8,W9,W10-15,W19,W20 20 25<br>3 T2+B1+T6+B3 W7,W8,W9,W10-15,W19,W20 60 75<br>3 T3a+B1+T1+B3 W7,W8,W9,W10-15 5 20<br>3 T4b+B3 W7,W8,W9,W10-15,W19,W20 20 20<br>3 T5+B3+T3a+B4 W7,W8,W9,W10-15,W19,W20 30 30<br>3 T6+B3+T4b+B4 W7,W8,W9,W10-15,W19,W20 60 60";
      // for (const question of allQuestions)
      // {
      //   const message: Message = {
      //     content: question,
      //     fromUser: true
      //   };
    
      //   predefinedMessages.push(message);
      //   this.scrollToBottom();
      //   try {
      //     const response = await axios.post(this.apiUrl, {
      //       model: "gpt-3.5-turbo",
      //       messages : predefinedMessages.map(msg => ({ role: msg.fromUser ? 'user' : 'assistant', content: msg.content }))
      //     }, {
      //       headers: {
      //         'Authorization': `Bearer ${this.apiKey}`,
      //         'Content-Type': 'application/json',
      //       },
      //     });
    
      //     botResponse = response.data.choices[0].message.content;
      //     console.log(botResponse);
      //   } catch (error) {
      //     console.error('Error:', error);
      //   }
      // }
      botResponse = botResponse.replaceAll("\n", "<br>");
      const botMessage: Message = {
        content: botResponse,
        fromUser: false
      };
      this.messages.push(botMessage);
      this.scrollToBottom();
      this.counter ++;
      this.question = '';
      this.showImage = true;
    }
    
    // if (this.counter > this.response.length)
    if (this.counter > 20)
    {
      if (this.question.trim() === '') {
        return;
      }
      
      const message: Message = {
        content: this.question,
        fromUser: true
      };
  
      this.messages.push(message);
      this.scrollToBottom();
  
      try {
        const response = await axios.post(this.apiUrl, {
          model: "gpt-3.5-turbo",
          messages : this.messages.map(msg => ({ role: msg.fromUser ? 'user' : 'assistant', content: msg.content }))
        }, {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json',
          },
        });
  
        const botResponse = response.data.choices[0].message.content;
        const botMessage: Message = {
          content: botResponse,
          fromUser: false
        };
  
        this.messages.push(botMessage);
        this.scrollToBottom();
      } catch (error) {
        console.error('Error:', error);
      }
      this.question = '';
    }
  }
  

  private scrollToBottom(): void {
    setTimeout(() => {
      this.messagesContainer.nativeElement.scrollTop = this.messagesContainer.nativeElement.scrollHeight;
    }, 0);
  }
}
