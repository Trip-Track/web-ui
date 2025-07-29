// Handles *all* network traffic to the Django backend
const BASE_UI = '/trip_ui';

export async function getGraphData() {
    const r = await fetch(`${BASE_UI}/graph-data/`);
    return r.json();
}

export async function getPath(start, end) {
    const r = await fetch(`${BASE_UI}/path/?start=${start}&end=${end}`);
    return r.json();
}

export async function getCityInfo(city) {
    // /city_info?city=<name or code>
    const r = await fetch(`${BASE_UI}/city_info/?city=${encodeURIComponent(city)}`);
    return r.json();
}
