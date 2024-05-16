import { ChatRequest, ChatResponse, RoleType, SearchSettings, UserProfile } from "./models";

export class ChatResponseError extends Error {
    public retryable: boolean;

    constructor(message: string, retryable: boolean) {
        super((message = message));
        this.message = message;
        this.retryable = retryable;
    }
}

export async function chatApi(options: ChatRequest): Promise<ChatResponse> {
    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: options.userID,
            conversation_id: options.conversationID,
            dialog_id: options.dialogID,
            dialog: options.dialog,
            overrides: {
                semantic_ranker: options.overrides?.semanticRanker,
                semantic_captions: options.overrides?.semanticCaptions,
                top: options.overrides?.top,
                temperature: options.overrides?.temperature,
                exclude_category: options.overrides?.excludeCategory,
                suggest_followup_questions: options.overrides?.suggestFollowupQuestions,
                classification_override: options.overrides?.classificationOverride,
                vector_search: options.overrides?.vectorSearch
            }
        })
    });

    const parsedResponse: ChatResponse = await response.json();
    if (response.status > 299 || !response.ok) {
        throw new ChatResponseError(parsedResponse.error ?? "An unknown error occurred.", parsedResponse.show_retry ?? false);
    }

    return parsedResponse;
}

export async function getSearchSettings(): Promise<SearchSettings> {
    const searchSettings: SearchSettings = {vectorization_enabled: true};
    return searchSettings;
}

export function getCitationFilePath(citation: string): string {
    return `/content/${citation}`;
}
