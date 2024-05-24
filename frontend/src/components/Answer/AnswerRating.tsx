import { IconButton } from "@fluentui/react";
import { useState } from 'react';

interface Props {
    onRating?: (value: boolean | undefined) => void;
    rating?: boolean | undefined;
}

export const AnswerRating = (props: Props) => {
    const [rating, setRating] = useState<boolean | undefined>(props.rating);
    const onRating = props.onRating || (() => { });
    const handleChange = (value: boolean | undefined) => {
        setRating(value);
        onRating(value);
    };
    return (
        <div>
            <IconButton iconProps={{ iconName: rating === true ? "LikeSolid" : "Like" }}
                title="Thumbs Up"
                ariaLabel="Thumbs Up"
                checked={rating === true}
                onClick={() => handleChange(rating === true ? undefined : true)} />
            <IconButton iconProps={{ iconName: rating === false ? "DislikeSolid" : "Dislike" }}
                title="Thumbs Down"
                ariaLabel="Thumbs Down"
                checked={rating === false}
                onClick={() => handleChange(rating === false ? undefined : false)} />
        </div>
    );
};