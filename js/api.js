const API_URL = "http://localhost:5000";


async function analyzeCode(questionId, code) {

    const response = await fetch(
        `${API_URL}/analyze`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                question_id: questionId,

                code: code

            })
        }
    );


    if (!response.ok) {

        throw new Error(
            "Backend request failed"
        );

    }


    return await response.json();
}