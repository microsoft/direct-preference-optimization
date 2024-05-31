import { renderToStaticMarkup } from "react-dom/server";
import { ApproachType, ChatResponse, Citation, getCitationFilePath } from "../../api";

type HtmlParsedAnswer = {
    answerHtml: string;
    citations: Citation[];
    followupQuestions: string[];
};

export function parseAnswerToHtml(chatResponse: ChatResponse, onCitationClicked: (citationFilePath: string) => void): HtmlParsedAnswer {
    const citations: Citation[] = [];
    const followupQuestions: string[] = [];

    // Extract any follow-up questions that might be in the answer
    let parsedAnswer = chatResponse.answer.formatted_answer.replace(/<<<([^>>>]+)>>>/g, (match, content) => {
        followupQuestions.push(content);
        return "";
    });

    // trim any whitespace from the end of the answer after removing follow-up questions
    parsedAnswer = parsedAnswer.trim();
    chatResponse.answer.citations.map((citation, index) => {
        citations.push(citation);
    });

    return {
        answerHtml: parsedAnswer,
        citations,
        followupQuestions
    };
}
