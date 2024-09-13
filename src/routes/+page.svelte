<script lang="ts">
	import { onMount } from 'svelte';
	import Chart from 'chart.js/auto';
	import TreeView from '../tree/TreeView.svelte';

	let pieChartCanvas: HTMLCanvasElement;
	let lineChartCanvas: HTMLCanvasElement;
	let pieChart: Chart<'pie', number[], string>;
	let lineChart: Chart<'line', never[], never>;

	// let treeData: never[] = [];
	let loading = true;
	let error = null;
	let treeData = [];

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
	function updatePieChart(data: any) {
		if (pieChart) {
			pieChart.update();
		}
	}

	onMount(async () => {
		const pieChartContainer = document.getElementById('pie-chart-container')!;
		const lineChartContainer = document.getElementById('line-chart-container')!;

		let startX: number,
			startY: number,
			startXLine: number,
			startYLine: number,
			startWidthLine: number,
			startHeightLine: number,
			startWidth: number,
			startHeight: number,
			draggingLine = false,
			dragging = false;

		pieChartContainer.addEventListener('mousedown', (e) => {
			dragging = true;
			startX = e.clientX;
			startY = e.clientY;
			startWidth = pieChartContainer.offsetWidth;
			startHeight = pieChartContainer.offsetHeight;
			pieChartContainer.style.cursor = 'grabbing';
		});

		lineChartContainer.addEventListener('mousedown', (e) => {
			draggingLine = true;
			startXLine = e.clientX;
			startYLine = e.clientY;
			startWidthLine = lineChartContainer.offsetWidth;
			startHeightLine = lineChartContainer.offsetHeight;
			lineChartContainer.style.cursor = 'grabbing';
		});
		document.addEventListener('mousemove', (e) => {
			if (dragging) {
				const dx = e.clientX - startX;
				const dy = e.clientY - startY;

				pieChartContainer.style.width = `${startWidth + dx}px`;
				pieChartContainer.style.height = `${startHeight + dy}px`;
			}
			if (draggingLine) {
				const dx = e.clientX - startXLine;
				const dy = e.clientY - startYLine;
				lineChartContainer.style.width = `${startWidthLine + dx}px`;
				lineChartContainer.style.height = `${startHeightLine + dy}px`;
			}
		});

		document.addEventListener('mouseup', () => {
			if (dragging) {
				dragging = false;
				pieChartContainer.style.cursor = 'grab';

				// Save size to localStorage
				localStorage.setItem('containerWidth', String(pieChartContainer.offsetWidth));
				localStorage.setItem('containerHeight', String(pieChartContainer.offsetHeight));
			}

			if (draggingLine) {
				draggingLine = false;
				lineChartContainer.style.cursor = 'grab';
				localStorage.setItem('lineContainerWidth', String(lineChartContainer.offsetWidth));
				localStorage.setItem('lineContainerHeight', String(lineChartContainer.offsetHeight));
			}
		});
		// Load size from localStorage if available
		const savedWidth = localStorage.getItem('containerWidth');
		const savedHeight = localStorage.getItem('containerHeight');
		const lineWidth = localStorage.getItem('lineContainerWidth');
		const lineHeight = localStorage.getItem('lineContainerHeight');

		pieChartContainer.style.width = `${savedWidth}px`;
		pieChartContainer.style.height = `${savedHeight}px`;
		lineChartContainer.style.width = `${lineWidth}px`;
		lineChartContainer.style.height = `${lineHeight}px`;

		// Pie Chart
		pieChart = new Chart(pieChartCanvas, {
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
		loading = false;
		console.log('graphite data: ', graphiteData);
		if (graphiteData && Array.isArray(graphiteData[0]?.datapoints)) {
			updateLineChart(graphiteData[0].datapoints);
			treeData = graphiteData[0].datapoints.map((point) => {
				return [point[0], [point[1]]];
			});
		}
	});
</script>

<h1>Cool Charts</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<h2>Data For: vigilant-vino-iamr-02</h2>

<div class="chart-grid">
	<div class="chart-container" id="pie-chart-container">
		<h2>Pie Chart</h2>
		<canvas bind:this={pieChartCanvas}></canvas>
	</div>
	<div class="chart-container" id="line-chart-container">
		<h2>Line Chart</h2>
		<canvas bind:this={lineChartCanvas}></canvas>
	</div>
</div>

<div class="chart-container" id="treeview-chart-container">
	<h2>Tree View</h2>
	<TreeView data={treeData} />
</div>

<style>
	.chart-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 1rem;
		margin-top: 2rem;
	}

	.chart-container {
		width: 200px;
		height: 200px;
	}

	canvas {
		width: 100% !important;
		height: 100% !important;
	}
</style>
