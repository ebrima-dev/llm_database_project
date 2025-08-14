import {useState} from 'react';
import { Box, Input, Button, Typography } from '@mui/joy';

export default function QueryForm() {
    const [query, setQuery] = useState('');
    const [answer, setAnswer] = useState('');

    const sendQuery = async () => {
        const res = await fetch('http://localhost:8000/ask', {
            method: 'POST',
            headers : {"Content-Type": "application/json"},
            body: JSON.stringify({query, type: "rag"}) // or "sql"
        });
        const data = await res.json();
        setAnswer(data.answer);
    };

    return (
        <Box sx={{p:2}}>
            <Typography level="h4">Ask My Data</Typography>
            <Input
                placeholder="Ask a question..."
                value={query}
                onChange={(e) =>  setQuery(e.target .value)}
            />
            <Button onClick={sendQuery} sx={{ mt: 1 }}>
                Submit
            </Button>
            {answer && <Typography level="body1" sx={{ mt:2 }}>{answer}</Typography>}
        </Box>
    );
}