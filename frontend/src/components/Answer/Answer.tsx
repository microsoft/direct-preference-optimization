import { useMemo } from "react";
import { Stack, IconButton, PrimaryButton, Label } from "@fluentui/react";
import DOMPurify from "dompurify";

import styles from "./Answer.module.css";

import { ChatResponse, DialogRequest, getCitationFilePath, rateApi } from "../../api";
import { parseAnswerToHtml } from "./AnswerParser";
import { AnswerIcon } from "./AnswerIcon";
import { AnswerRating } from "./AnswerRating";
import { ErrorCircle20Regular } from "@fluentui/react-icons";

interface Props {
    chatResponse: ChatResponse;
    isSelected?: boolean;
    rating?: boolean | undefined;
    onCitationClicked: (filePath: string) => void;
    onThoughtProcessClicked: () => void;
    onSupportingContentClicked: () => void;
    onFollowupQuestionClicked?: (question: string) => void;
    showFollowupQuestions?: boolean;
    onRetryClicked?: () => void;
    onRating?: (value: boolean | undefined) => void;
    retryable: boolean;
    dialogInfo: DialogRequest;
}

export const Answer = ({
    chatResponse,
    isSelected,
    rating,
    onCitationClicked,
    onThoughtProcessClicked,
    onSupportingContentClicked,
    onFollowupQuestionClicked,
    showFollowupQuestions,
    onRetryClicked,
    onRating,
    retryable,
    dialogInfo
}: Props) => {
    const parsedAnswer = useMemo(() => parseAnswerToHtml(chatResponse, onCitationClicked), [chatResponse]);
    const sanitizedAnswerHtml = DOMPurify.sanitize(parsedAnswer.answerHtml);
    const answer = chatResponse.answer;
    onRating = onRating || (() => {});
    const rate = (value: boolean | undefined) => {
        rateApi({
            userID: dialogInfo.userID,
            conversationID: dialogInfo.conversationID,
            dialogID: dialogInfo.dialogID,
            rating: value,
            request: answer.query,
            response: answer.formatted_answer
        }).then(() => onRating(value));
    };
    const shouldNotShowThoughtProcess = !chatResponse.classification && !answer.query && !answer.query_generation_prompt && !answer.query_result;
    return (
        <Stack className={`${styles.answerContainer} ${isSelected && styles.selected}`} verticalAlign="space-between">
            <Stack.Item>
                <Stack horizontal horizontalAlign="space-between">
                    <AnswerIcon />
                    <div>
                        <IconButton
                            style={{ color: "black" }}
                            iconProps={{ iconName: "Lightbulb" }}
                            title="Show thought process"
                            ariaLabel="Show thought process"
                            onClick={() => onThoughtProcessClicked()}
                            disabled={shouldNotShowThoughtProcess}
                        />
                        <IconButton
                            style={{ color: "black" }}
                            iconProps={{ iconName: "ClipboardList" }}
                            title="Show supporting content"
                            ariaLabel="Show supporting content"
                            onClick={() => onSupportingContentClicked()}
                            disabled={!chatResponse.data_points.length}
                        />
                    </div>
                </Stack>
            </Stack.Item>

            <Stack.Item grow>
                <div className={styles.answerText} dangerouslySetInnerHTML={{ __html: sanitizedAnswerHtml }}></div>
                {retryable && onRetryClicked && (
                    <div className={styles.retryContainer}>
                        <ErrorCircle20Regular />
                        <Label className={styles.retryText}>
                            Looks like this search ran into an issue. Would you like me to try again with an expanded scope?
                        </Label>
                        <PrimaryButton className={styles.retryButton} onClick={onRetryClicked} text="Retry" />
                    </div>
                )}
            </Stack.Item>

            <Stack.Item>
                <AnswerRating onRating={value => rate(value)} rating={rating} />
            </Stack.Item>

            {!!parsedAnswer.citations.length && (
                <Stack.Item>
                    <Stack horizontal wrap tokens={{ childrenGap: 5 }}>
                        <span className={styles.citationLearnMore}>Citations:</span>
                        {parsedAnswer.citations.map((x, i) => {
                            return (
                                <a key={i} className={styles.citation} title={x.title} onClick={() => onCitationClicked(x.url)}>
                                    {`${++i}. ${x.title}`}
                                </a>
                            );
                        })}
                    </Stack>
                </Stack.Item>
            )}

            {!!parsedAnswer.followupQuestions.length && showFollowupQuestions && onFollowupQuestionClicked && (
                <Stack.Item>
                    <Stack horizontal wrap className={`${!!parsedAnswer.citations.length ? styles.followupQuestionsList : ""}`} tokens={{ childrenGap: 6 }}>
                        <span className={styles.followupQuestionLearnMore}>Follow-up questions:</span>
                        {parsedAnswer.followupQuestions.map((x, i) => {
                            return (
                                <a key={i} className={styles.followupQuestion} title={x} onClick={() => onFollowupQuestionClicked(x)}>
                                    {`${x}`}
                                </a>
                            );
                        })}
                    </Stack>
                </Stack.Item>
            )}
        </Stack>
    );
};
