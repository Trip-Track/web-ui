// All SVG-drawing logic lives here
const NS = 'http://www.w3.org/2000/svg';

export function drawGraph(svg, data) {
    svg.innerHTML = '';
    const edgeMap = {};

    const stopMap = {};
    data.connections.forEach(c => {
        [c.from, c.to].forEach(s => stopMap[s.code] ??= s);
    });
    const stops = Object.values(stopMap);

    const [minLat, maxLat] = [Math.min(...stops.map(s => s.lat)),
                              Math.max(...stops.map(s => s.lat))];
    const [minLng, maxLng] = [Math.min(...stops.map(s => s.lng)),
                              Math.max(...stops.map(s => s.lng))];

    const x = lng => (lng - minLng) / (maxLng - minLng) * svg.clientWidth;
    const y = lat => svg.clientHeight -
                     (lat - minLat) / (maxLat - minLat) * svg.clientHeight;

    data.connections.forEach(c => {
        const line = document.createElementNS(NS, 'line');
        line.setAttribute('class', 'connection');
        line.setAttribute('x1', x(c.from.lng));
        line.setAttribute('y1', y(c.from.lat));
        line.setAttribute('x2', x(c.to.lng));
        line.setAttribute('y2', y(c.to.lat));
        svg.appendChild(line);

        edgeMap[`${c.from.code}-${c.to.code}`] = line;
        edgeMap[`${c.to.code}-${c.from.code}`] = line;   // undirected
    });

    stops.forEach(s => {
        const g = document.createElementNS(NS, 'g');
        g.innerHTML = `
           <circle class="stop" data-code="${s.code}"
                   cx="${x(s.lng)}" cy="${y(s.lat)}" r="5"></circle>
           <text   class="stop-label"
                   x="${x(s.lng) + 8}" y="${y(s.lat) - 8}">${s.name}</text>`;
        svg.appendChild(g);
    });

    return { stopMap, edgeMap };
}

export function highlightPath(edgeMap, stops) {
    Object.values(edgeMap).forEach(el => el.classList.remove('highlight'));

    for (let i = 0; i < stops.length - 1; i++) {
        const line = edgeMap[`${stops[i]}-${stops[i + 1]}`];
        line?.classList.add('highlight');
    }
}
