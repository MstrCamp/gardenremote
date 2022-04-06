window.onload = () => {
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

    const evtSource = new EventSource("listen");
    evtSource.onmessage = (event) => {
        console.log(event)
    }

}

