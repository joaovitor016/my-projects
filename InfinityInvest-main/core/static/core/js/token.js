/*https://itnext.io/how-to-create-an-animated-countdown-timer-with-html-css-and-javascript-d0171d1fb6f7*/

const FULL_DASH_ARRAY = 283;

const TIME_LIMIT = 30;
let timePassed = 0;
let timeLeft = TIME_LIMIT;

function random(len) {
    let result = Math.floor(Math.random() * Math.pow(10, len));

    return (result.toString().length < len) ? random(len) : result;
}

function generateNumbers() {
    document.getElementById("base-timer-label").innerHTML = `${random(3)} ${random(3)}`;
}

function onTimesUp() {
    timePassed = 0;
    timeLeft = TIME_LIMIT;
    generateNumbers();
}

function startTimer() {
    generateNumbers();
    timerInterval = setInterval(() => {
        timePassed = timePassed += 1;
        timeLeft = TIME_LIMIT - timePassed;
        setCircleDasharray();
        if (timeLeft === 0) {
            onTimesUp();
        }
    }, 1000);
}

function calculateTimeFraction() {
    const rawTimeFraction = timeLeft / TIME_LIMIT;
    return rawTimeFraction - (1 / TIME_LIMIT) * (1 - rawTimeFraction);
}

function setCircleDasharray() {
    const newValue = calculateTimeFraction() * FULL_DASH_ARRAY;

    const circleDasharray = `${(
        newValue > 0 ? newValue : FULL_DASH_ARRAY
    ).toFixed(0)} ${FULL_DASH_ARRAY}`;
    document
        .getElementById("base-timer-path-remaining")
        .setAttribute("stroke-dasharray", circleDasharray);
}

startTimer();

