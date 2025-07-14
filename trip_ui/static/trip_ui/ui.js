export function showPathResult(cost, stops) {
    document.getElementById('path-result').textContent =
        `Cost: ${cost}, Stops: ${stops.join(' → ')}`;
}

export function showCityInfo(info) {
    const div = document.getElementById('city-info');

    if (!info || !info.area) {
        div.textContent = 'No info for this city 😞';
        return;
    }

    div.innerHTML = `
      <h2>Destination city facts</h2>
      <ul>
        <li><strong>Area:</strong> ${info.area.value} km²</li>
        <li><strong>Population:</strong> ${info.population.value}</li>
        <li><strong>Fun fact:</strong> ${info.fun_fact.text}</li>
      </ul>`;
}
