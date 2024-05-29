import { BrowserRouter, Routes, Route } from "react-router-dom";
import { MsalProvider, MsalAuthenticationTemplate, useMsal } from "@azure/msal-react";
import { IPublicClientApplication, InteractionType } from "@azure/msal-browser";

import Layout from "./pages/layout/Layout";
import NoPage from "./pages/NoPage";
import PageContainer from "./pages/PageContainer";
import { loginRequest } from "./authconfig";

type AppProps = {
    pca: IPublicClientApplication;
};

const MainContent = () => {
    const { instance } = useMsal();

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<PageContainer />} />
                    <Route path="*" element={<NoPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
};

const App = ({ pca }: AppProps) => {
    const authRequest = {
        ...loginRequest
    };
    return (
        <MsalProvider instance={pca}>
            <MsalAuthenticationTemplate interactionType={InteractionType.Redirect} authenticationRequest={authRequest}>
                <MainContent />
            </MsalAuthenticationTemplate>
        </MsalProvider>
    );
};

export default App;
