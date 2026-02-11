let stream


function connect(url) {
    stream = new EventSource(url)

    stream.addEventListener("data", function (e) {
        setData(JSON.parse(e.data))
    })

    stream.onopen = function (e) {
        console.log("Successfully connected to the EventSource.")
    }

    stream.onclose = function (e) {
        console.log("EventSource connection closed unexpectedly")
    }

    stream.onerror = function (err) {
        console.log("EventSource encountered an error")
        window.location.reload()
    }

    stream.kill = function () {
        stream.onmessage = null
        stream.onclose = null
        stream.close()
    }
}