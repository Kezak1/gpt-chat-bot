# LLM-app
made a chat bot, using [this tutorial](https://alejandro-ao.com/how-to-use-streaming-in-langchain-and-streamlit/).

## Setup
1. Clone the repository:
    ```bash
    git clone git@github.com:Kezak1/LLM-app.git
    cd LLM-app
    ```
2. Make in directory a file ".env" and put your OpenAI API key there.

3. For running the program use command:
    ```bash
    streamlit run .\src\app.py
    ```

## Note:
- You can change the promt of the chat bot (modify):
    ```python
    template = """
        You are a helpful assistant. Answer the foollowing questions considering the history of the conversation:

        Chat history: {chat_history}

        User question: {user_question}

    """
    ``` 

## Future Enchancements:
- Add more features.
