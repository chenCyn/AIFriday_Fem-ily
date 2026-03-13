# from src.db import init_db
# from src.api import get_conversation_chain
# from src.frontend import create_ui

# def main():
#     db = init_db()
#     qa_chain = get_conversation_chain(db)
#     demo = create_ui(qa_chain)
#     demo.launch(css=".gradio-container {background-color: lightblue}", debug=True)

# if __name__ == "__main__":
#     main()
from src.db import init_db
from src.api import get_conversation_chain
from src.frontend import create_ui

def main():
    db = init_db()
    qa_chain = get_conversation_chain(db)
    create_ui(qa_chain)

if __name__ == "__main__":
    main()
