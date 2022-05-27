let reconDurationSSE = 1; // duration in seconds between sse reconnection tries
let evtSource; // SSE event source

/**
 * Performs initial setup of all required functions and eventhandlers, only if current page is /remote
 */
function setup() {
    if (window.location.pathname !== "/remote") return;

    log("Setting up remote...")
    // register ajax calls to the correct api endpoints for all toggle switches
    //configureLabels();
    setupRelays();
    setupShutters();

    // listen to server sent events for changes in relay states or other events
    setupEventSource();

    // reload weather forecast every hour
    setInterval(reloadWeatherForecast, 60 * 60 * 1000 /* every hour */);
}

/*function configureLabels() {
    const labels = document.querySelectorAll(`[id^="label_"]`)
    labels.forEach(label => {
        label.onclick = (evt) => {
            evt.preventDefault();
        }
    })
}*/

/**
 * registers Ajax calls to server api for every checkbox
 */
function setupRelays() {
    const checkboxes = document.querySelectorAll(`[id^="relay_"]`)
    checkboxes.forEach(box => {
        box.onchange = () => {
            const targetState = box.checked
            box.disabled = true
            box.indeterminate = true
            const xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    const relay = JSON.parse(xhr.responseText);
                    box.disabled = false
                    box.indeterminate = false
                    box.checked = relay.state === 'ON'
                }
            };
            xhr.open('GET', `relay/${box.id}/${targetState ? 'on' : 'off'}`);
            xhr.send()
        }
    })
}

/**
 * registers Ajax calls to server api for shutter control
 */
function setupShutters() {
    const checkboxes = document.querySelectorAll(`[id^="checkbox_shutter_"]`)
    checkboxes.forEach(box => {
        box.onchange = () => {
            const targetState = box.checked
            box.disabled = true
            box.indeterminate = true
            const xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    const relay = JSON.parse(xhr.responseText);
                    box.disabled = false
                    box.indeterminate = false
                    box.checked = relay["management_state"] === 'AUTO'
                }
            };
            xhr.open('GET', `shutter/${box.id.slice("checkbox_".length)}/${targetState ? 'auto' : 'manual'}`);
            xhr.send()
        }
    })
    const buttons = document.querySelectorAll(`[id^="button_shutter_"]`)
    buttons.forEach(button => {
        button.onclick = () => {
            const xhr = new XMLHttpRequest();
            const func = button.id.endsWith("open") ? "open" : "close";
            const id = button.id.slice("button_".length, button.id.length-(func.length + 1))
            xhr.onreadystatechange = function () {};
            xhr.open('GET', `shutter/${id}/${func}`);
            xhr.send()
        }
    })
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
    try {
        const data = JSON.parse(event.data)
        if (data['type'] === 'SENSOR') {
            applySensorData(data['content'])
        } else if (data['type'] === 'RELAY') {
            applyRelayState(data['content'])
        } else if (data['type'] === 'SHUTTER') {
            applyShutterState(data['content'])
        } else {
            log(`Cannot handle data type ${data['type']}`)
        }
    } catch (e) {
        log(`Error while trying to parse event: ${e.message}`)
        log(event.data)
    }
}

/**
 * Update the sensor display with the given values
 *
 * @param data
 */
function applySensorData(data) {
    for (const [key, value] of Object.entries(data)) {
        document.getElementById(key).innerHTML = `${value['name']}: ${value['temperature']}° / ${value['humidity']}%`;
    }
}

/**
 * Update the relay switches to the given states
 *
 * @param data
 */
function applyRelayState(data) {
    for (const [key, value] of Object.entries(data)) {
        const box = document.getElementById(key)
        box.checked = value['state'] === 'ON';
        box.disabled = false;
    }
}

/**
 * Update the shutter switches to the given states
 *
 * @param data
 */
function applyShutterState(data) {
    for (const [key, value] of Object.entries(data)) {
        const box = document.getElementById(`checkbox_${key}`)
        box.checked = value['management_state'] === 'AUTO';
        box.disabled = false;
    }
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
