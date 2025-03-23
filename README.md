# OpenAI Chat Bot Clone

Simple chat bot. Made the app using [this tutorial](https://alejandro-ao.com/how-to-use-streaming-in-langchain-and-streamlit/) and expand the source code. It has database with accounts (user id, password, user history). The program can be run only locally.

## Setup

1. Clone the repository:

	```bash
	git clone git@github.com:Kezak1/gpt-chat-bot.git
	cd gpt-chat-bot
	```

2. Make, in repo directory, a file ".env" and put your OpenAI API key there:

	```
	# .env file
	OPENAI_API_KEY=your_api_key
	```

3. Setup your virtual environment

4. Install requirements:

	```bash
	pip install -r requirements.txt
	```

5. To run the program use command:

	```bash
	streamlit run .\src\app.py
	```

## Future Enchancements

- Add more features
- Deployment
