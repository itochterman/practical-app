<script lang="ts">
import { onMount } from 'svelte';
import Chart from 'chart.js/auto';

let pieChartCanvas: HTMLCanvasElement;
let lineChartCanvas: HTMLCanvasElement;

onMount(() => {
  // Pie Chart
  new Chart(pieChartCanvas, {
    type: 'pie',
    data: {
      labels: ['Red', 'Blue', 'Yellow'],
      datasets: [{
        data: [300, 50, 100],
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    }
  });

  // Line Chart
  new Chart(lineChartCanvas, {
    type: 'line',
    data: {
      labels: ['January', 'February', 'March', 'April', 'May', 'June'],
      datasets: [{
        label: 'Sales',
        data: [12, 19, 3, 5, 2, 3],
        borderColor: '#4BC0C0',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    }
  });
});
</script>

<h1>Cool Charts</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<div class="chart-grid">
  <div class="chart-container">
    <h2>Pie Chart</h2>
    <canvas bind:this={pieChartCanvas}></canvas>
  </div>
  <div class="chart-container">
    <h2>Line Chart</h2>
    <canvas this={lineChartCanvas}></canvas>
  </div>
</div>

<style>
  .chart-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
  }

  .chart-container {
    height: 300px;
    width: 100%;
  }

  canvas {
    width: 100% !important;
    height: 100% !important;
  }
</style>
