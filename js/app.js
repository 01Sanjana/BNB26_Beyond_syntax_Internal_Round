/* =====================================================
   SECTION NAVIGATION
===================================================== */

function showSection(sectionId) {

    const sections =
        document.querySelectorAll(".page-section");


    sections.forEach(function(section) {

        section.classList.add("hidden");

    });


    const selected =
        document.getElementById(sectionId);


    if (selected) {

        selected.classList.remove("hidden");

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }
}


/* =====================================================
   SELECT ANSWER
===================================================== */

function selectOption(button) {

    const buttons =
        button.parentElement.querySelectorAll("button");


    buttons.forEach(function(btn) {

        btn.classList.remove("selected");

    });


    button.classList.add("selected");
}


/* =====================================================
   RUN CODE
===================================================== */

function runCode() {

    const output =
        document.getElementById("output");


    output.classList.remove("hidden");


    output.innerHTML = `
        <strong>Output</strong>
        <br><br>
        [1, 2, 3, 4]
    `;
}


/* =====================================================
   SUBMIT CODE
===================================================== */

async function submitCode() {

    const code =
        document.getElementById("codeEditor").value;


    console.log("Submitted code:", code);


    /*
        FOR NOW:
        Dummy response.

        LATER:
        Replace this with:

        const result = await analyzeCode(
            1,
            code
        );
    */


    const result = {

        correct: false,

        misconception: "Variable References",

        confidence: 0.87,

        evidence:
            "You appear to be treating y = x as creating a separate list."

    };


    showDiagnosis(result);
}


/* =====================================================
   SHOW DIAGNOSIS
===================================================== */

function showDiagnosis(data) {

    document.getElementById(
        "misconception"
    ).innerText = data.misconception;


    document.getElementById(
        "confidence"
    ).innerText =
        "Confidence: " +
        Math.round(data.confidence * 100) +
        "%";


    document.getElementById(
        "evidence"
    ).innerText = data.evidence;


    showSection("diagnosis");
}


/* =====================================================
   SHOW REASSESSMENT
===================================================== */

function showReassessment() {

    showSection("reassessment");
}


/* =====================================================
   REASSESSMENT ANSWER
===================================================== */

function checkAnswer(button, correct) {

    const buttons =
        button.parentElement.querySelectorAll("button");


    buttons.forEach(function(btn) {

        btn.classList.remove("selected");

    });


    button.classList.add("selected");


    const result =
        document.getElementById("finalResult");


    result.classList.remove("hidden");


    if (correct) {

        result.innerHTML = `
            <strong>Concept understood.</strong>

            <p>
                You correctly identified that both variables
                refer to the same list.
            </p>

            <button
                class="primary-button"
                onclick="showSection('dashboard')">

                Back to Dashboard

            </button>
        `;

    } else {

        result.innerHTML = `
            <strong>The concept may still need practice.</strong>

            <p>
                Assigning one list variable to another does
                not automatically create a copy.
            </p>

            <button
                class="secondary-button"
                onclick="showSection('practice')">

                Try Again

            </button>
        `;
    }
}