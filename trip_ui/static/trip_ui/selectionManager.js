
const MAX = 2;
let selected = [];

export function init(svg) {
    svg.addEventListener('click', e => {
        if (!e.target.classList.contains('stop')) return;
        const code = e.target.dataset.code;

        if (!selected.includes(code)) {
            selected = selected.length === MAX ? [selected[1], code]
                                               : [...selected, code];
        } else {
            selected = selected.filter(c => c !== code);
        }
        updateVisuals(svg);
    });
}

export function getSelected() {
    return selected.slice();
}

function updateVisuals(svg) {
    svg.querySelectorAll('.stop').forEach(c => c.classList.remove('selected'));
    selected.forEach(code => {
        svg.querySelector(`.stop[data-code="${code}"]`)
           ?.classList.add('selected');
    });
}
