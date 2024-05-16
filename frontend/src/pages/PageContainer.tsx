import { useState, useEffect } from "react";

import { SearchSettings, UserProfile, getSearchSettings } from "../api";
import Chat from "./chat/Chat";
import { LoadingPanel } from "../components/LoadingPanel";
import { ErrorPanel } from "../components/ErrorPanel";

const PageContainer = () => {
    const [isDataLoading, setIsDataLoading] = useState<boolean>(true);
    const [dataError, setDataError] = useState<unknown>();

    const fetchData = async () => {
        try {
            setDataError(undefined);
        } catch (e) {
            setDataError(e);
        } finally {
            setIsDataLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            {isDataLoading ? (
                <LoadingPanel />
            ) : dataError ? (
                <ErrorPanel error={dataError.toString()} onRetry={() => fetchData()} />
            ) : (
                <Chat />
            )}
        </div>
    );
};

export default PageContainer;
