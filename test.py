from app.handler import handler

if __name__ == '__main__':
    mock_event = {
        'input': {
            'prompt': 'Who is the prime minister of Thailand?',
            'seconds': 2
        }
    }
    print(handler(mock_event))