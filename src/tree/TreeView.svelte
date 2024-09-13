<script>
	// Input property: tree data as an array of arrays
	export let data = [];

	// Recursive function to render tree nodes
	function renderTree(nodes) {
		return nodes
			.map((node) => {
				return `
				<li>
					${node[0]}
					${node[1]}
				</li>
				`;
			})
			.join('');
	}
</script>

<ul>
	{@html renderTree(data)}
</ul>

<style>
	ul {
		list-style-type: none;
		padding-left: 20px;
	}

	li {
		margin: 5px 0;
	}
</style>
