# ExamQueueBot

The project is a Telegram bot, which will generate a queue for exams/credits in our chat room and so on, to prevent discrimination on the first letter of the surname.

## Getting Started

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
```/swap 1 2```

```/swap Petrov Ivanov```

```/swap 1 Ivanov```

```/swap Petrov 2```

and so on

### Move a person to a new position:
```/move 1 2```

```/move Petrov Ivanov```

```/move 1 Ivanov```

```/move Petrov 2```

## Run this code

To install all the required dependencies, use

```pip install --upgrade -r requirements.txt```

You will need to [create a new bot and get a token](https://core.telegram.org/bots#6-botfather) for it. After that, the code can be run by

```BOT_TOKEN=<token> DB_URL=<URL of your Redis database> DB_TOKEN=<password for your Redis database> python3 -m src```

To run unit tests for this code, use

```pytest```

To launch type checking, use

```mypy src```