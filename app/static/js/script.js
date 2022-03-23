window.onload = () => {
    const checkBox = document.getElementById('checkbox1');
    if (checkBox !== null) {
        checkBox.onchange = (event) => {
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

