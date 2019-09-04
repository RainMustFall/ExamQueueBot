# ExamQueueBot

The project is a Telegram bot, which will generate a queue for exams/credits in our chat room and so on, to prevent discrimination on the first letter of the surname.

## Why am I even doing this?

Because you often have to queue up somewhere, and it's really annoying when everyone starts doing it, and you're not there or you're slow to react and get to the end. Or if everybody decides to go in alphabetical order and you are always at the very end/start/other awkward place. 
Random is the guardian of justice!

## How to use it?

Just put my monster (@exam_queue_bot) in a group chat room and have fun.

### Add group list:
```
/setlist
Name1
Name2
...
NameN
```
### Generate a new queue:
```/generate```

### Show the last line generated:
```/show```

### Swap two people:
```swap 1 2```

```swap Petrov Ivanov```

```swap 1 Ivanov```

```swap Petrov 2```

and so on

### Move the dude to a new position:
```/move 1 2```

```/move Petrov Ivanov```

```/move 1 Ivanov```

```/move Petrov 2```

## How can I run this code on my computer?
You will need to [create a new bot and get a token](https://core.telegram.org/bots#6-botfather) for it. After that, for example, for local work, just enter 

```python script.py INSERT_YOUR_TOKEN_HERE```
