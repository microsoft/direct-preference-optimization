import { RateRequest, RateResponse, ChatRequest, ChatResponse, RoleType, SearchSettings, UserProfile } from "./models";

export class ChatResponseError extends Error {
    public retryable: boolean;

    constructor(message: string, retryable: boolean) {
        super((message = message));
        this.message = message;
        this.retryable = retryable;
    }
}

export async function rateApi(request: RateRequest): Promise<RateResponse> {
    const response = await fetch("/rate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: request.userID,
            conversation_id: request.conversationID,
            dialog_id: request.dialogID,
            rating: request.rating || null,
            request: request.request ?? "no request",
            response: request.response ?? "no response"
        })
    });

    const json = await response.json();
    console.log("response", request, json);
    const parsedResponse: RateResponse = json;
    if (response.status > 299 || !response.ok) {
        throw new Error(parsedResponse.error ?? "An unknown error occurred.");
    }

    return parsedResponse;
}

export async function chatApi(request: ChatRequest): Promise<ChatResponse> {
    const overrides = request.overrides;
    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: request.userID,
            conversation_id: request.conversationID,
            dialog_id: request.dialogID,
            dialog: request.dialog,
            overrides: {
                semantic_ranker: overrides?.semanticRanker,
                semantic_captions: overrides?.semanticCaptions,
                top: overrides?.top,
                temperature: overrides?.temperature,
                exclude_category: overrides?.excludeCategory,
                suggest_followup_questions: overrides?.suggestFollowupQuestions,
                classification_override: overrides?.classificationOverride,
                vector_search: overrides?.vectorSearch
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
    return { vectorization_enabled: true };
}

export function getCitationFilePath(citation: string): string {
    return `/content/${citation}`;
}
