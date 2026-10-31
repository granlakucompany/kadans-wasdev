# Skill: chart scene

`{type:"chart", chart:"bar|line|pie|doughnut|area", title?, items[1-12] {label,value}}`.
Drawn with Chart.js (vendored, MIT) — the `chart` lib is added automatically. WASDEV palette.
```json
{"type":"chart","chart":"bar","title":"Growth","items":[{"label":"Jan","value":10},{"label":"Feb","value":25}]}
```
