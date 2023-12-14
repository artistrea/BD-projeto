<script >
    import { api } from "../api";
    import { onMount } from "svelte";
    import router from "page"

    export let params

    let id = params.id
    let type = params.type
    let item = {}
    let dataDeAquisicao

    function fecthData() {
        api.get(`/items/${type}/${id}`).then((res) => {
            item = res.data
            dataDeAquisicao = new Date(item.dataDeAquisicao).toISOString().split('T')[0]
        }).catch((er) => alert(er.message))
        return () => {}
    }

    onMount(fecthData())

    $: item.dataDeAquisicao = new Date(dataDeAquisicao).toUTCString()

    function handleSubmit(e) {
        e.preventDefault()

        delete item.id
        delete item.type
        delete item.ISBN

        api.patch(`/items/update/${type}/${id}`, item).then((res) => {
            alert("Item editado com sucesso.")
            router.redirect(`/item/${id}/${type}`)
        }).catch((er) => alert(er.message))
    }

    function deleteItem() {
        if (confirm("Confirme para deletar o Item.")) {
            api.delete(`/items/delete/${type}/${id}`).then((res) => {
            alert("Item Deletado.")
            router.redirect(`/inventario`)
        }).catch((er) => alert(er.message))
        }
    }

</script>

<main class="flex flex-col min-h-screen w-full items-center">
    <h1 class="text-4xl font-bold tracking-tight text-opacity-80 text-text mt-10">
        Editar <span class="text-accent">{item.type? (item.type == "livro"? 'Livro' : "Material Didático") : "Item"}</span>	
    </h1>
    <p class="max-w-prose mt-1 text-sm text-opacity-70 text-text leading-6 mt-3">
        Esta é a página de edição de um {item.type == "livro"? 'livro' : "material didático"}. <br/>
        É necessário um administrador ou chefe de laboratório para realizar a edição.
    </p>
	<form on:submit={handleSubmit} class="bg-secondary rounded flex flex-col p-8 h-auto w-1/3 justify-center mt-10">
        {#if item.type === 'livro'}
            <div class="flex flex-col">
                <label class="pt-4" for="titulo">Título:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="titulo" bind:value={item.title}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="autor">Autor:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="autor" bind:value={item.author}>
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
                <input class="bg-transparent border-b border-primary px-4 py-2" type="date" id="dataDeAquisicao" bind:value={dataDeAquisicao}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="uriImagem">Url da Imagem:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="url" id="uriImagem" bind:value={item.uriImagem}>
            </div>
            <button class="hover:scale-[1.01] transition-all rounded px-4 py-2 bg-primary text-background mt-4 disabled:opacity-50">Editar</button>
        {/if}
        {#if item.type === "materialDidatico"}
            <div class="flex flex-col">
                <label class="pt-4" for="numeroDeSerie">Número de Série:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="number" id="numeroDeSerie" bind:value={item.numeroDeSerie}>
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
                <input class="bg-transparent border-b border-primary px-4 py-2" type="date" id="dataDeAquisicao" bind:value={dataDeAquisicao}>
            </div>
            <div class="flex flex-col">
                <label class="pt-4" for="uriImagem">Url da Imagem:</label>
                <input class="bg-transparent border-b border-primary px-4 py-2" type="url" id="uriImagem" bind:value={item.uriImagem}>
            </div>
            <button class="hover:scale-[1.01] transition-all rounded px-4 py-2 bg-primary text-background mt-4 disabled:opacity-50">Editar</button>
        {/if}
	</form>
    <button on:click={deleteItem} class="hover:scale-[1.01] transition-all rounded px-4 py-2 bg-accent text-background mt-4 disabled:opacity-50 hover:text-red-500" >Deletar {item.type == "livro"? 'Livro' : "Material Didático"}</button>
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