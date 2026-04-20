// components/progress-bar.js
class ProgressBar extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    
    connectedCallback() {
        this.value = parseInt(this.getAttribute('value')) || 0;
        this.max = parseInt(this.getAttribute('max')) || 100;
        this.label = this.getAttribute('label') || 'Progreso';
        this.showPercentage = this.hasAttribute('show-percentage');
        this.render();
    }
    
    render() {
        const percentage = (this.value / this.max) * 100;
        let color = '#27ae60';
        if (percentage < 30) color = '#e74c3c';
        else if (percentage < 70) color = '#f39c12';
        this.shadowRoot.innerHTML = `
            <style>
                .container { font-family: 'Segoe UI', sans-serif; margin: 10px 0; }
                .label { display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 14px; color: #555; }
                .bar-bg { background: #ecf0f1; border-radius: 10px; overflow: hidden; height: 20px; }
                .bar-fill { background: ${color}; width: ${percentage}%; height: 100%; border-radius: 10px; transition: width 0.5s ease; display: flex; align-items: center; justify-content: center; color: white; font-size: 11px; font-weight: bold; }
            </style>
            <div class="container">
                <div class="label"><span>${this.label}</span>${this.showPercentage ? `<span>${Math.round(percentage)}%</span>` : ''}</div>
                <div class="bar-bg"><div class="bar-fill" style="width: ${percentage}%">${this.showPercentage && percentage > 15 ? `${Math.round(percentage)}%` : ''}</div></div>
            </div>
        `;
    }
    
    setValue(value, max) { this.value = value; if (max) this.max = max; this.render(); }
}
customElements.define('progress-bar', ProgressBar);