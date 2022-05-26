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
 * Prints the current timestamp and the given message. Use instead of console.log
 *
 * @param message {String}
 */
function log(message) {
    console.log(`${new Date().toLocaleTimeString()}: ${message}`)
}

window.onload = setup
