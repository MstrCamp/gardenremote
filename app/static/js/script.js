let reconDurationSSE = 1; // duration in seconds between sse reconnection tries
let evtSource; // SSE event source

/**
 * Performs initial setup of all required functions and eventhandlers, only if current page is /remote
 */
function setup() {
    if (window.location.pathname !== "/remote") return;

    log("Setting up remote...")
    for (let i = 0; i < 11; i++) {
        const checkBox = document.getElementById('checkbox' + i);
        if (checkBox !== null) {
            checkBox.onchange = () => {
                checkBox.disabled = true
                checkBox.indeterminate = true
                setTimeout(() => {
                    checkBox.disabled = false
                    checkBox.indeterminate = false
                    checkBox.checked = Math.random() < 0.5
                }, 2000)
            }
        }
    }

    // listen to server sent events for changes in relay states or other events
    setupEventSource();

    // reload weather forecast every hour
    setInterval(reloadWeatherForecast, 60 * 60 * 1000 /* every hour */);
}

/**
 * Establishes a robust, autoreconnecting connection to SSE source
 */
function setupEventSource() {
    evtSource = new EventSource("listen");
    evtSource.onmessage = handleSSE
    evtSource.onopen = () => {
        log("SSE connection established.")
        reconDurationSSE = 1;
    };
    evtSource.onerror = () => {
        evtSource.close();
        log(`SSE connection failed. Will try to reconnect in ${reconDurationSSE} seconds...`)
        setTimeout(() => {
            log("trying to reconnect to server...");
            setupEventSource();
            reconDurationSSE *= 2;
            if (reconDurationSSE >= 64) {
                reconDurationSSE = 64;
            }
        }, reconDurationSSE * 1000)
    };
}

/**
 * Handles all receieved SSE events
 *
 * @param event {MessageEvent}
 */
function handleSSE(event) {
    //console.log(event)
    log(event.data)
}

/**
 * Reloads the small weather forecast image
 */
function reloadWeatherForecast() {
    log("Reloading weather forecast...")
    let url = 'https://w.bookcdn.com/weather/picture/26_18251_1_2_34495e_250_2c3e50_ffffff_ffffff_1_2071c9_ffffff_0_6.png?scode=2&domid=591&anc_id=69752';
    const img = document.getElementById('weather_img');
    url = url + '?' + new Date().getTime(); // append timestamp to ensure that image is really refetched and not taken from cache
    img.src = url;
}

/**
 * Prints the current timestamp and the given message. Use instead of console.log
 *
 * @param message {String}
 */
function log(message) {
    console.log(`${new Date().toLocaleTimeString()}: ${message}`)
}

window.onload = setup
