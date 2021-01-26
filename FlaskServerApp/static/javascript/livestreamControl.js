function load(key) {
    span = document.getElementById("streamkey");
    span.onmouseover = () => {
        if (span.innerHTML == "Stream Key") {
            span.innerHTML = "Click To See Your Stream Key. You have 30 secondes."
        }
    }
    span.onmouseout = () => {
        if (span.innerHTML == "Click To See Your Stream Key. You have 30 secondes.") {
            span.innerHTML = "Stream Key"
        }
    }

    span.onclick = () => {
        if (span.innerHTML == "Click To See Your Stream Key. You have 30 secondes.")
        {
            span.innerHTML = key
            setTimeout( () => {
                span.innerHTML = "Stream Key"
            }, 30000);
        } else if (span.innerHTML == key) {
            span.innerHTML = "Stream Key"
        }
    }
}