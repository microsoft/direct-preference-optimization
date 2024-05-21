from operator import itemgetter


from langchain_core.runnables import (RunnablePassthrough, RunnableLambda)


from models.chat_response import Answer
from models.chat_response import ChatResponse
from approaches.multi_index_chat_builder import MultiIndexChatBuilder

class ChatConversation:
    """ Class used to manage the chat conversation and chain runnables together for 
        the chat conversation"""
    def __init__(
            self,
            system_prompt: str,
            default_return_message: str,
            builder: MultiIndexChatBuilder
        ):
        self._system_prompt = system_prompt
        self._default_return_message = default_return_message
        self._builder = builder


    def _route(self, info):
        if not info["context"]:
            return self._builder.default_return_message(self._default_return_message)

        # Creating a chat template with a system message and a human message.
        # Both messages are passed as templates.
        model = self._builder.llm()
        chat_template = self._builder.chat_template(self._system_prompt)
        general_chain = chat_template | model

        return general_chain


    def chat(self, prompt: str) -> ChatResponse:
        """ Creating a chain of runnables that will fill the context variable
            in the template. Initially, this chain will get primary index
            documents and append the secondary index documents to the list.
            Then, it will sort and filter."""
        chain = (
            {
                "context": {
                    "primary_documents": itemgetter("question")
                    | RunnableLambda(self._builder.get_primary_documents),
                    "secondary_documents": itemgetter("question") 
                    | RunnableLambda(self._builder.get_secondary_documents),
                }
                | RunnableLambda(self._builder.sort_and_filter_documents)
                | self._builder.format_docs,
                "question": RunnablePassthrough(),
            }
            | RunnableLambda(self._route)
        )

        answer = chain.invoke({"question": prompt})
        chat_answer = Answer(formatted_answer=answer.content)

        return ChatResponse(answer=chat_answer)
