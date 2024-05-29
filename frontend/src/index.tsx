import React from "react";
import ReactDOM from "react-dom/client";
import { initializeIcons } from "@fluentui/react";
import { PublicClientApplication, EventType, EventMessage, AuthenticationResult } from "@azure/msal-browser";

import { msalConfig } from "./authconfig";
import App from "./App";

import "./index.css";

initializeIcons();

export const msalInstance = new PublicClientApplication(msalConfig);

msalInstance.initialize().then(() => {
    // Account selection logic is app dependent. Adjust as needed for different use cases.
    const accounts = msalInstance.getAllAccounts();
    if (accounts.length > 0) {
        console.log(accounts);
        msalInstance.setActiveAccount(accounts[0]);
    }

    msalInstance.addEventCallback((event: EventMessage) => {
        if (event.eventType === EventType.LOGIN_SUCCESS && event.payload) {
            const payload = event.payload as AuthenticationResult;
            const account = payload.account;
            msalInstance.setActiveAccount(account);
        }
    });

    const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);
    root.render(
        <React.StrictMode>
            <App pca={msalInstance} />
        </React.StrictMode>
    );
});
