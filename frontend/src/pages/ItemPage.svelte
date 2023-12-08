<script >
    import { onMount } from "svelte";
    import { api } from "../api";
    import { BookOpenText, PencilRuler } from "lucide-svelte"
    import defaultBook from "../assets/default_book.png"

    export let params
    let id = params.id
    let type = params.type

    let item = {}

    function fecthData() {
        api.get(`/items/${type}/${id}`).then((res) => {
            item = res.data
            console.log(item)
        }).catch((er) => alert(er.message))

        return () => {}
    }

    onMount(fecthData())

</script>

<main class="flex min-h-full w-full h-full justify-center">
    <section class="flex flex-col h-auto w-1/2 items-left pl-24 ">
        <div class="item_type" >
            {#if item.type == "livro"}
                <BookOpenText size=48 class="absolute top-16 left-12 text-primary"/>
                <h1 class='pl-10 relative -left-10 text-primary'>
                    Livro
                </h1>
                {/if}
                {#if item.type == "materialDidatico"}
                <PencilRuler size=48 class="absolute top-16 left-14 text-primary"/>
                <h1 class='pl-10'>
                    Material Didático
                </h1>
                {/if}
        </div>
        <div class="flex flex-col w-full justify-center">
            <h1 class="text-5xl" >{item.title} </h1>
            <p class="text-opacity-50 text-4xl pt-5" >{item.author}</p>
        </div>
        <div class=" flex bg-secondary w-full p-6 mt-10 text-text rounded-sm leading-7">
           {item.descricao} 
        </div>
        <div class="mt-5">
            <b>ISBN:</b>
            {item.ISBN}
        </div>
        <div class="mt-5">
            <b>Data de Aquisição:</b>
            { (new Date(item.dataDeAquisicao)).toLocaleDateString('pt-BR', { timeZone: 'UTC' }) }
        </div>
        <div class="mt-5">
            <b>Estado de Conservação: </b>
            {item.estadoDeConservacao}
        </div>
        <div class="mt-5 flex flex-col bg-primary w-full p-6 text-background rounded-sm leading-7" >
            <b class=" text-lg">Encontra-se em: </b>
            <p class="relative -right-10">
                {item.localizacao}
            </p>
        </div>
    </section>
    <section class="flex flex-col h-full p-6 max-h-screen w-1/2">
        <h1 class=" text-lg font-bold rounded-md bg-accent py-2 px-3 h-min w-min text-background self-end mb-2">{item.categoria}</h1>
        <div class="flex flex-col content-center items-center p-5 items-right bg-primary rounded-lg h-full max-h-full">
            <img src={item.uriImagem? item.uriImagem  : defaultBook} alt="Falha ao carregar Imagem" class="imagem object-contain h-full max-h-screen w-full"/>
        </div>
    </section>
</main>

<style>
    .item_type {
        font-size: 4rem;
        width: 45vw;
        display: flex;
        justify-content: left;
        
    }
    .imagem {
        max-height: 80vh;
    }
</style>