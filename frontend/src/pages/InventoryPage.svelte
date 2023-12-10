<script>
	import { onMount } from "svelte";
	import { api } from "../api";
  import { BookOpenText, PencilRuler } from "lucide-svelte"

	// // const apiKEY = "YOUR-API-KEY";
	// // const dataUrl = `https://newsapi.org/v2/everything?q=javascript&sortBy=publishedAt&apiKey=${apiKEY}`;
  let items = [];
	let selectedTypes = [];
	function fetchData() {
		api.get("/items").then((res) => {
			items = res.data;
		}).catch((er) => alert(er.message))

		return () => {};
    };
    
	onMount(fetchData());
</script>
<div class="pl-20 flex justify-between relative">
	<div class="py-8 mx-auto">
		<h1 class="text-4xl font-bold tracking-tight text-opacity-80 text-text">
			Inventário	
		</h1>
		<p class="max-w-prose mt-1 text-sm text-opacity-70 text-text leading-6">
			Estes são os itens que você pode pedir para pegar emprestado.
			É necessário um admin ou chefe de laboratório para consumar o empréstimo.
		</p>

		<main class="mt-2">
			<ul class="flex flex-col gap-4 p-8">
				{#each items.filter((item) => selectedTypes.length === 0 || selectedTypes.some(t => t === item.type)) as item (item.id ?? item.ISBN)}
					{#if item.type === "livro"}
						<li class="bg-primary text-background text-opacity-90 rounded relative">
              <a href={`/item/${item.id}/${item.type}`}>
                <BookOpenText class="absolute top-4 -left-8 text-primary" />
                <div class="flex justify-between">
                  <h2 class="pt-4 pb-2 pl-4">
                    <span class="text-xl">{item.title}</span>
                    <br>
                    <span class="opacity-70 text-sm">
                      {item.author}
                    </span>
                  </h2>
                  <span class="text-sm font-bold rounded-bl bg-accent py-2 px-3 h-min ">{item.categoria}</span>
                </div>
                <p class="w-[40ch] leading-7 mb-4 ml-6 overflow-ellipsis overflow-hidden line-clamp-3">
                  {item.descricao}
                </p>
            </a>
						</li>
					{/if}
					{#if item.type === "materialDidatico"}
						<li class="bg-text text-background text-opacity-90 rounded relative">
              <a href={`/item/${item.id}/${item.type}`}>
                <PencilRuler class="absolute top-4 -left-8 text-text" />
                <div class="flex justify-between">
                  <h2 class="pt-4 pl-4">
                    {item.descricao}
                  </h2>
                  <span class="text-sm font-bold rounded-bl bg-accent py-2 px-3 h-min ">{item.categoria}</span>
                </div>
                <span class="opacity-70 text-sm pb-2 pl-4">
                    Estado de Conservação:
                    {item.estadoDeConservacao}
                </span>
            </a>
						</li>
					{/if}
				{/each}
			</ul>
		</main>
	</div>

	<aside class="bg-secondary shadow-inner py-4 h-screen sticky top-0">
		<h2 class="px-4 text-2xl font-bold tracking-tight">
			Filtros
		</h2>
		<p class="px-4 max-w-prose mt-1 text-sm text-opacity-70 text-text leading-6">
			Escolha o que quer visualizar do inventário.
		</p>
		<div class="py-2">
			<fieldset class="border border-gray-400 rounded flex flex-col">
        <span class="flex gap-2 p-2">
          <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white rounded checked:bg-primary my-auto" type="checkbox" name="materialDidatico" id="materialDidatico" checked={selectedTypes.some(t => t === "materialDidatico")} on:change={(e) => !e.currentTarget.checked ? selectedTypes = selectedTypes.filter(t => t!== "materialDidatico") : selectedTypes = [...selectedTypes, "materialDidatico"]}>
          <label for="materialDidatico">
            Materiais Didáticos
          </label>
        </span>
        <span class="flex gap-2 p-2">
          <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white rounded checked:bg-primary my-auto" type="checkbox" name="livro" id="livro" checked={selectedTypes.some(t => t === "livro")} on:change={(e) => !e.currentTarget.checked ? selectedTypes = selectedTypes.filter(t => t!== "livro") : selectedTypes = [...selectedTypes, "livro"]}>
          <label for="livro">
            Livros
          </label>
        </span>
			</fieldset>
		</div>
	</aside>
</div>

<style>
  input:checked {
    background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M12.207 4.793a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-2-2a1 1 0 011.414-1.414L6.5 9.086l4.293-4.293a1 1 0 011.414 0z'/%3e%3c/svg%3e")
  }
</style>
<!-- [
  {
    "ISBN": 8577803828,
    "author": "CARLOS ALBERTO HEUSER",
    "categoria": "Bancos de Dados",
    "dataDeAquisicao": "Sun, 12 Nov 2023 00:00:00 GMT",
    "descricao": "Livro sobre modelagem de Bancos de Dados. 6\u00aa edi\u00e7\u00e3o",
    "estadoDeConservacao": "bom",
    "id": 8577803828,
    "localizacao": "prateleira 1",
    "title": "Projeto de Banco de Dados",
    "type": "livro",
    "uriImagem": "https://media.istockphoto.com/id/466564401/pt/vetorial/modelo-de-livro-vertical-em-branco.jpg?s=1024x1024&w=is&k=20&c=ZKSJ4qganGkiieYJMx6ODiCmZUuXLmdOmWBn_qg6Byc="
  },
  {
    "ISBN": 8579360855,
    "author": "ELMASRI, R. E. e NAVATHE, S.",
    "categoria": "Bancos de Dados",
    "dataDeAquisicao": "Mon, 01 Jan 2001 00:00:00 GMT",
    "descricao": "Livro sobre sistemas de bancdos de dados",
    "estadoDeConservacao": "ruim",
    "id": 8579360855,
    "localizacao": "prateleira 4",
    "title": "Sistemas de Banco de Dados",
    "type": "livro",
    "uriImagem": "https://media.istockphoto.com/id/495477978/pt/foto/livro-aberto.jpg?s=2048x2048&w=is&k=20&c=dnNS2jDfWlODq7CtV_IyAdZCaeLKEb0P1mpMFzfkwPM="
  },
  {
    "ISBN": 1234567890,
    "author": "QUALQUER, PESSOA",
    "categoria": "Outros",
    "dataDeAquisicao": "Sat, 02 Feb 2002 00:00:00 GMT",
    "descricao": "Um Outro Livro Qualquer",
    "estadoDeConservacao": "\u00f3timo",
    "id": 1234567890,
    "localizacao": "prateleira 1",
    "title": "Livro Qualquer",
    "type": "livro",
    "uriImagem": ""
  },
  {
    "categoria": "escrita",
    "dataDeAquisicao": "Sun, 25 Aug 2019 00:00:00 GMT",
    "descricao": "Lapiseira Pentel P207",
    "estadoDeConservacao": "bom",
    "id": 101507,
    "localizacao": "sala3",
    "numeroDeSerie": 696332587,
    "type": "materialDidatico",
    "uriImagem": ""
  },
  {
    "categoria": "escrita",
    "dataDeAquisicao": "Fri, 07 Jul 2017 00:00:00 GMT",
    "descricao": "Borracha FaberCastell",
    "estadoDeConservacao": "ruim",
    "id": 156242,
    "localizacao": "sala2",
    "numeroDeSerie": 121698535,
    "type": "materialDidatico",
    "uriImagem": ""
  },
  {
    "categoria": "escrit\u00f3rio",
    "dataDeAquisicao": "Sat, 03 Apr 2021 00:00:00 GMT",
    "descricao": "Pasta Fich\u00e1rio 100U",
    "estadoDeConservacao": "\u00f3timo",
    "id": 566542,
    "localizacao": "sala4",
    "numeroDeSerie": 648465469,
    "type": "materialDidatico",
    "uriImagem": ""
  }
] -->
