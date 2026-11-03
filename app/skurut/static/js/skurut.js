const map = L.map('map').setView([60.18, 24.95], 13)

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map)

function createTramMarker(lat, lng, direction, tramLine) {
    const icon = L.divIcon({
        className: 'tram-icon',
        html: `
                <img src="/static/images/circle_with_caret_small.png" style="transform: rotate(${direction}deg);">
                <div class="tram-line">${tramLine}</div>
            `,
        iconSize: [50, 50], // Match the size of the PNG
        iconAnchor: [25, 25], // Anchor at the center
    })

    const marker = L.marker([lat, lng], {icon}).addTo(map)
    return marker
}

const tramMarkers = {},
    tramSet = new Set()

function setData(payload) {
    const {lat, long, hdg, desi, veh} = payload // `desi` is the tram line
    if (!lat || !long) return

    if (!tramSet.has(desi)) {
        tramSet.add(desi)
        addTramButtons()
    }

    if (!tramMarkers[veh]) {
        tramMarkers[veh] = {
            marker: createTramMarker(lat, long, hdg, desi),
            tramLine: desi,
        }
    } else {
        tramMarkers[veh].marker.setLatLng([lat, long])
        tramMarkers[veh].tramLine = desi
        try {
            const img = tramMarkers[veh].marker._icon.querySelector('img')
            if (img) img.style.transform = `rotate(${hdg}deg)`
        } catch (err) {
        }
    }
    updateFilters()
}

function updateFilters() {
    const visibleLines = Array.from(document.querySelectorAll('.tgl:checked'))
        .map(input => input.value)

    for (const veh in tramMarkers) {
        const {marker, tramLine} = tramMarkers[veh]
        if (visibleLines.includes(tramLine) || !visibleLines.length) {
            map.addLayer(marker) // Show marker
        } else {
            map.removeLayer(marker) // Hide marker
        }
    }
}

if (navigator.geolocation) {
    function showPosition(position) {
        L.marker([position.coords.latitude, position.coords.longitude], {title: "Olet tässä"}).addTo(map)
        map.setView([position.coords.latitude, position.coords.longitude], 16)
    }

    navigator.geolocation.getCurrentPosition(showPosition)
}

function addTramButtons() {
    function lineSort(a, b) {
        return String(a).localeCompare(String(b), 'fi', {numeric: true})
    }

    const filterContent = document.querySelector("#filter")
    const selectedLines = new Set(Array.from(filterContent.querySelectorAll('.tgl:checked'))
        .map(input => input.value))
    filterContent.innerHTML = ""
    Array.from(tramSet).sort(lineSort).forEach(line => {
        const clone = document.getElementById('tram-button').content.cloneNode(true)
        const input = clone.querySelector('input')
        const label = clone.querySelector('label')
        input.value = line
        input.id = `cb3-${line}`
        input.checked = selectedLines.has(String(line))
        input.addEventListener('change', updateFilters)
        label.setAttribute('for', `cb3-${line}`)
        label.textContent = line
        filterContent.appendChild(clone)
    })
}
