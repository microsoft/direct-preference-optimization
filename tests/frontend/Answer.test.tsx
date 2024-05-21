import React from "react";
import { render, screen } from "@testing-library/react";
import { Answer } from "../../frontend/src/components/Answer/Answer";
import { ChatResponse } from "../../frontend/src/api";
import "@testing-library/jest-dom";
// NOTE: jest-dom adds handy assertions to Jest and is recommended, but not required

test("Answer component", () => {
  it("renders the answer text", () => {
    const answerText = "This is the answer";
    const response = new ChatResponse();
    render(
      <Answer
        chatResponse={response}
        onCitationClicked={() => {}}
        onThoughtProcessClicked={() => {}}
        onSupportingContentClicked={() => {}}
        retryable={false}
      />
    );
    const answerElement = screen.getByText(answerText);
    expect(answerElement).toBeInTheDocument();
  });
});
