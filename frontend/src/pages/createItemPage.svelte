<script >
    import { api } from "../api";
    import router from "page"

    let item = {
        'id' : undefined,
        'type' : undefined,
        'descricao' : undefined,
        'categoria' : undefined,
        'dataDeAquisicao' : undefined,
        'estadoDeConservacao' : undefined,
        'localizacao' : undefined,
        'uriImagem' : ''
    }

    let livro = {
        "ISBN" : undefined,
        "title" : undefined,
        "author" : undefined
    }

    $: livro.ISBN = item.id

    let materialDidatico = {
        "id" : undefined,
        "numeroDeSerie": undefined
    }

    $: materialDidatico.id = item.id


    function handleSubmit(e) {
        e.preventDefault()
        let body = item.type === "livro"? {item, livro} : {item, materialDidatico}

        api.post("/items/create", body).then((res) => {
            alert("Item cadastrado com sucesso.")
            router.redirect("/inventario")
        }).catch((er) => alert(er.message))
    }
</script>

<main class="flex flex-col min-h-screen w-full items-center">
    <h1 class="text-4xl font-bold tracking-tight text-opacity-80 text-text mt-10">
        Cadastrar Novo <span class="text-accent">{item.type? (item.type == "livro"? 'Livro' : "Material Didático") : "Item"}</span>	
    </h1>
    <p class="max-w-prose mt-1 text-sm text-opacity-70 text-text leading-6 mt-3">
        Esta é a página para cadastramento de um novo livro ou material didático. <br/>
        É necessário um admin ou chefe de laboratório para realizar o cadastro.
    </p>
	<form on:submit={handleSubmit} class="bg-secondary rounded flex flex-col p-8 h-auto justify-center mt-10">
        <label for="tipo" class="self-start">
            Deseja cadastrar um Livro ou Material Didático?
            <fieldset class="border border-gray-400 rounded flex flex-col" id="tipo">
                <span class="flex gap-2 p-2">
                <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white rounded-full checked:bg-primary my-auto" type="radio" bind:group={item.type} value="materialDidatico" name="materialDidatico" id="materialDidatico" >
                <label for="materialDidatico">
                    Materiais Didático
                </label>
                </span>
                <span class="flex gap-2 p-2">
                <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white  rounded-full checked:bg-primary my-auto" type="radio" bind:group={item.type} value="livro" name="livro" id="livro">
                <label for="livro">
                    Livro
                </label>
                </span>
            </fieldset>
        </label>
        {#if item.type === 'livro'}
            <div class="flex flex-col">
                <label class="pt-4" for="titulo">Título:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="titulo" bind:value={livro.title}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="autor">Autor:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="autor" bind:value={livro.author}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="ISBN">ISBN:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="number" id="ISBN" bind:value={item.id}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="categoria">Categoria:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="categoria" bind:value={item.categoria}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="descricao">Descrição:</label>
                <textarea class="bg-transparent border border-primary px-4 py-2" rows=3 bind:value={item.descricao} id="descricao"/>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="localizacao">Localização:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="localizacao" bind:value={item.localizacao}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="estadoDeConservacao">Estado de Conservação:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="estadoDeConservacao" bind:value={item.estadoDeConservacao}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="dataDeAquisicao">Data de Aquisição:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="date" id="dataDeAquisicao" on:change={(e) => item.dataDeAquisicao = new Date(e.currentTarget.value).toDateString()}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="uriImagem">Url da Imagem:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="url" id="uriImagem" bind:value={item.uriImagem}>
            </div>
            <button disabled={Object.values(item).includes(undefined) || Object.values(livro).includes(undefined)} class="hover:scale-[1.01] transition-all rounded px-4 py-2 bg-primary text-background mt-4 disabled:opacity-50">Cadastrar</button>
        {/if}
        {#if item.type === "materialDidatico"}
            <div class="flex flex-col">
                <label class="pt-4" for="id">Identificador:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="number" id="id" bind:value={item.id}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="numeroDeSerie">Número de Série:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="number" id="numeroDeSerie" bind:value={materialDidatico.numeroDeSerie}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="categoria">Categoria:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="categoria" bind:value={item.categoria}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="descricao">Descrição:</label>
                <textarea class="bg-transparent border border-primary px-4 py-2" rows=3 bind:value={item.descricao} id="descricao"/>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="localizacao">Localização:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="localizacao" bind:value={item.localizacao}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="estadoDeConservacao">Estado de Conservação:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="estadoDeConservacao" bind:value={item.estadoDeConservacao}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="dataDeAquisicao">Data de Aquisição:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="date" id="dataDeAquisicao" on:change={(e) => item.dataDeAquisicao = new Date(e.currentTarget.value).toDateString()}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="uriImagem">Url da Imagem:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="url" id="uriImagem" bind:value={item.uriImagem}>
            </div>
            <button disabled={Object.values(item).includes(undefined) || Object.values(materialDidatico).includes(undefined)} class="hover:scale-[1.01] transition-all rounded px-4 py-2 bg-primary text-background mt-4 disabled:opacity-50">Cadastrar</button>
        {/if}
	</form>
</main>

<style>
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
    }
    input[type=number] {
    -moz-appearance: textfield;
    }

</style>