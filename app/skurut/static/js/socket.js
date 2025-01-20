let socket


function connect() {
    const socketProtocol = window.location.protocol === "https:" ? "wss://" : "ws://"
    socket = new WebSocket(socketProtocol + window.location.host + "/ws/location/")

    socket.onopen = function (e) {
        console.log("Successfully connected to the WebSocket.")
    }

    socket.onclose = function (e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...")
        setTimeout(function () {
            console.log("Reconnecting...")
            connect()
        }, 2000)
    };

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data)
        setData(data.location)
    }

    socket.onerror = function (err) {
        console.log("WebSocket encountered an error: " + err.message)
        console.log("Closing the socket.")
        socket.close()
    }

    socket.kill = function () {
        socket.onmessage = null
        socket.onclose = null
        socket.close()
    }
}

connect()