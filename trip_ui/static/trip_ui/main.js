import { getGraphData, getPath, getCityInfo }   from './dataService.js';
import { drawGraph, highlightPath }             from './graphRenderer.js';
import { init as initSelection, getSelected }   from './selectionManager.js';
import { showPathResult, showCityInfo }         from './ui.js';

const graphDiv = document.getElementById('graph');
const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
graphDiv.appendChild(svg);

let edgeMap = {};

(async () => {
    const graphData = await getGraphData();
    const result    = drawGraph(svg, graphData);
    edgeMap         = result.edgeMap;

    initSelection(svg);
})();

document.getElementById('find-path')
        .addEventListener('click', async () => {
    const sel = getSelected();
    if (sel.length !== 2) {
        alert('Select two stops');
        return;
    }

    const pathResp = await getPath(sel[0], sel[1]);
    const stopCodes = pathResp.stops.map(s => s.code);
    showPathResult(pathResp.cost, stopCodes);
    highlightPath(edgeMap, stopCodes);

    try {
        const destCode = stopCodes.at(-1);
        const info = await getCityInfo(destCode);
        showCityInfo(info);
    } catch (err) {
        console.error(err);
        showCityInfo(null);
    }
});
