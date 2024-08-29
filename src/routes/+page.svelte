<script lang="ts">
	import { onMount } from 'svelte';
	import Chart from 'chart.js/auto';

	let pieChartCanvas: HTMLCanvasElement;
	let lineChartCanvas: HTMLCanvasElement;
	let lineChart: Chart;

	async function fetchGraphiteData() {
		try {
			const response = await fetch('http://localhost:8080/api/graphite');
			const data = await response.json();
			return data;
		} catch (error) {
			console.error('Error fetching graphite data:', error);
			return null;
		}
	}

	function updateLineChart(data: any) {
		if (lineChart) {
			lineChart.data.labels = data.map((item: any) => new Date(item[0] * 1000).toLocaleString());
			lineChart.data.datasets[0].data = data.map((item: any) => item[1]);
			lineChart.update();
		}
	}

	onMount(async () => {
		// Pie Chart
		new Chart(pieChartCanvas, {
			type: 'pie',
			data: {
				labels: ['Red', 'Blue', 'Yellow'],
				datasets: [
					{
						data: [300, 50, 100],
						backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false
			}
		});

		// Line Chart
		lineChart = new Chart(lineChartCanvas, {
			type: 'line',
			data: {
				labels: [],
				datasets: [
					{
						label: 'Host Alive',
						data: [],
						borderColor: '#4BC0C0',
						tension: 0.1
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false
			}
		});

		// Fetch and update data
		const graphiteData = await fetchGraphiteData();
    console.log('graphite data: ', graphiteData)
		if (graphiteData && Array.isArray(graphiteData[0]?.datapoints)) {
			// updateLineChart(graphiteData[0].datapoints);
		}
	});
</script>

<h1>Cool Charts</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<h2>Data For: vigilant-vino-iamr-02</h2>

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
