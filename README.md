# Project

### Multi-Index Search Flow
![alt text](./assets/chain.png "LangChain Flow")

When trying to retrieve documents and information to add to an LLM's context, they can be stored in multiple locations. In this example, we search two indexes in AI Search and utilize scoring as well as semantic ranking to retrieve the highest-rated information possible. When searching against a vector store such as AI Search, a hybrid search is recommended to increase the chances of finding information that will help set context. Typically, this will lower the overall RRF score, causing the results to be weighted differently than a semantic search. This is where re-ranking can help. By re-ranking the values and sorting them, you can evaluate the results and pull the topmost documents based on your data.

### Direct Preference optimization
![alt text](./assets/user-flows.png "LangChain Flow")

Since we are using re-ranking and answers can potentially be in either index, we implemented a pattern called [direct preference optimization](https://arxiv.org/abs/2305.18290) which can help add additional context for both positive and negative responses provided by the LLM. This data can be added to the context with notations on whether this is a good response or a bad response and help provide better responses. Additionally, the data can be searched and ranked to potentially avoid the LLM if the prompt has a high enough ranking.

In the user interface, when a response is returned, there is a thumbs up and thumbs down button provided to the user. They can rate the response, which will then be stored in AI Search. The prompt will be stored as text and vectorized, and the response will be stored as well.

### Citations

When searching for data, both internally within your company and externally, it is important to provide citations to the user so they can identify the source of the information. During the index search, documents are added to the chain, formatted, and the system prompt is used to tell the LLM to utilize the provided context to cite the answers provided. The LLM responds back with an answer in a format that can be parsed, allowing for a user to click on the link and view the cited document.

## Architecture

Storage Blob Delegator





## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.





