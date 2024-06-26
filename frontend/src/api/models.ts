export const enum ApproachType {
    Structured = "structured",
    Unstructured = "unstructured",
    ChitChat = "chit_chat"
}

export const enum RoleType {
    Engineer = "engineer"
}

export type ChatRequestOverrides = {
    semanticRanker?: boolean;
    semanticCaptions?: boolean;
    excludeCategory?: string;
    top?: number;
    temperature?: number;
    suggestFollowupQuestions?: boolean;
    classificationOverride?: ApproachType;
    vectorSearch?: boolean;
};

export interface DialogRequest {
    userID: string;
    conversationID: string;
    dialogID: string;
}

export interface RateRequest extends DialogRequest {
    rating?: boolean | undefined;
    response: string;
    request?: string;
}

export interface ChatRequest extends DialogRequest {
    dialog: string;
    overrides?: ChatRequestOverrides;
}

export type Citation = {
    id: string;
    url: string;
    title: string;
};

export type Answer = {
    formatted_answer: string;
    citations: Array<Citation>;
    query_generation_prompt?: string;
    query?: string;
    query_result?: string;
};

export type RateResponse = {
    error?: string;
    dialog_id: string;
    output: string[];
};

export type ChatResponse = {
    answer: Answer;
    classification?: ApproachType;
    data_points: string[];
    show_retry?: boolean;
    suggested_classification?: ApproachType;
    error?: string;
};

export type UserProfile = {
    user_id: string;
    user_name: string;
    description: string;
    sample_questions?: string[];
    role: RoleType;
};

export type ChatError = {
    retryable: boolean;
    message?: string;
};

export type UserQuestion = {
    question: string;
    classificationOverride?: ApproachType;
};

export type SearchSettings = {
    vectorization_enabled: boolean;
};
