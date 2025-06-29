const graphDiv = document.getElementById('graph');
const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
graphDiv.appendChild(svg);
let graphData = null;
let selected = [];
let edgeMap = {}; // maps "from-to" -> svg line element for highlighting

function drawGraph(data) {
    svg.innerHTML = '';
    const stopMap = {};
    edgeMap = {};
    data.connections.forEach(c => {
        [c.id, c.from, c.to].forEach(s => {
            if (s && !stopMap[s.code]) {
                stopMap[s.code] = s;
            }
        });
    });
    const stops = Object.values(stopMap);
    const minLat = Math.min(...stops.map(s => s.lat));
    const maxLat = Math.max(...stops.map(s => s.lat));
    const minLng = Math.min(...stops.map(s => s.lng));
    const maxLng = Math.max(...stops.map(s => s.lng));
    function x(lng) { return (lng - minLng) / (maxLng - minLng) * svg.clientWidth; }
    function y(lat) { return svg.clientHeight - (lat - minLat) / (maxLat - minLat) * svg.clientHeight; }
    data.connections.forEach(c => {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x(c.from.lng));
        line.setAttribute('y1', y(c.from.lat));
        line.setAttribute('x2', x(c.to.lng));
        line.setAttribute('y2', y(c.to.lat));
        line.setAttribute('class', 'connection');
        svg.appendChild(line);
        edgeMap[`${c.from.code}-${c.to.code}`] = line;
        edgeMap[`${c.to.code}-${c.from.code}`] = line; // treat as undirected
    });
    stops.forEach(stop => {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', x(stop.lng));
        circle.setAttribute('cy', y(stop.lat));
        circle.setAttribute('r', 5);
        circle.setAttribute('data-code', stop.code);
        circle.setAttribute('class', 'stop');
        circle.addEventListener('click', () => {
            if (!selected.includes(stop.code)) {
                if (selected.length === 2) {
                    selected.shift();
                }
                selected.push(stop.code);
            } else {
                selected = selected.filter(s => s !== stop.code);
            }
            document.querySelectorAll('.stop').forEach(el => el.classList.remove('selected'));
            selected.forEach(code => {
                const el = document.querySelector(`.stop[data-code="${code}"]`);
                if (el) el.classList.add('selected');
            });
        });
        g.appendChild(circle);
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', x(stop.lng) + 8);
        text.setAttribute('y', y(stop.lat) - 8);
        text.setAttribute('class', 'stop-label');
        text.textContent = stop.name;
        g.appendChild(text);
        svg.appendChild(g);
    });
}

fetch('/trip_ui/graph-data/')
    .then(r => r.json())
    .then(data => { graphData = data; drawGraph(data); });

document.getElementById('find-path').addEventListener('click', () => {
    if (selected.length !== 2) {
        alert('Select two stops');
        return;
    }
    fetch(`/trip_ui/path/?start=${selected[0]}&end=${selected[1]}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById('path-result').textContent = `Cost: ${data.cost}, Stops: ${data.stops.map(s => s.code).join(' -> ')}`;
            // remove previous highlight
            Object.values(edgeMap).forEach(line => line.classList.remove('highlight'));
            if (data.stops && data.stops.length > 1) {
                for (let i = 0; i < data.stops.length - 1; i++) {
                    const a = data.stops[i].code;
                    const b = data.stops[i + 1].code;
                    const line = edgeMap[`${a}-${b}`];
                    if (line) line.classList.add('highlight');
                }
            }
        });
});