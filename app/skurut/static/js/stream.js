function connect(url) {
    const stream = new EventSource(url)

    stream.addEventListener("data", function (e) {
        setData(JSON.parse(e.data))
    })

    stream.onopen = function (e) {
        console.log("Successfully connected to the EventSource.")
    }

    stream.onerror = function (err) {
        console.log("EventSource encountered an error")
        setTimeout(() => window.location.reload(), 1000)
    }

    return stream
}