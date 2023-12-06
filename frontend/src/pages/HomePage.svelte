<script>
	// import { onMount } from "svelte";

	// const apiKEY = "YOUR-API-KEY";
	// const dataUrl = `https://newsapi.org/v2/everything?q=javascript&sortBy=publishedAt&apiKey=${apiKEY}`;
    // let items = [];
	// const fetchData = async () => {
    // 	const response = await fetch(dataUrl);
    // 	const data = await response.json();
	// 	console.log(data);
    // 	items = data["articles"];
    // };
    
	// onMount(fetchData());
	console.log("home")
</script>
<div class="container">
<h1>
	EPA
</h1>

</div>

<style>
h1 {
	color: purple;
	font-family: 'kalam';
}
.container {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(305px, 1fr));
	grid-gap: 15px;
}
.container > .card img {
	max-width: 100%;
}
</style>