<script >
    import { onMount } from "svelte";
    import { api } from "../api";
    import { BookOpenText, PencilRuler } from "lucide-svelte"
    import defaultBook from "../assets/default_book.png"
    import defaultMaterial from "../assets/default_material.png"
    import { user } from "../stores/user";

    export let params
    let id = params.id
    let type = params.type

    let item = {}
    let available = false

    let askedForLoan = false

    function fecthData() {
        api.get(`/items/${type}/${id}`).then((res) => {
            item = res.data
        }).catch((er) => alert(er.message))

        api.get(`/items/isAvailable/${type}/${id}`).then((res) => {
            available = res.data.available
        }).catch((er) => alert(er.message))

        return () => {}
    }

    onMount(fecthData())

    function createLoan(status) {
        let today = new Date(Date.now())
        let new_loan = {
            dataDeEmprestimo : today.toDateString(),
            dataDeDevolucaoPrevista : new Date(today.setMonth(today.getMonth() + 1)).toDateString(),
            status : status,
            userId : $user.id,
            itemId : item.id,
            itemType : item.type
        }


        api.post("/loan", new_loan).then((res) => {
            alert("Empréstimo Solicitado.")
            askedForLoan = true
        }).catch((er) => alert(er.message))
    }

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
                <PencilRuler size=48 class="absolute top-16 left-14 text-text"/>
                <h1 class='pl-10'>
                    Material Didático
                </h1>
                {/if}
        </div>
        <div class="flex flex-col w-full justify-center">
            {#if item.type == "livro"}
                <h1 class="text-5xl" >{item.title} </h1>
                <p class="text-opacity-50 text-4xl pt-5" >{item.author}</p>
            {/if}
        </div>
        <div class=" flex bg-secondary w-full p-6 mt-10 text-text rounded-sm leading-7">
           {item.descricao} 
        </div>
        <div class="mt-5">
            {#if item.type == "livro"}
            <b>ISBN:</b>
            {item.ISBN}
            {/if}
            {#if item.type == "materialDidatico"}
            <b>Número de Série: </b>
            {item.numeroDeSerie}
            {/if}
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

        {#if item.type == "livro" || $user.funcao === "chefe" || $user.funcao === "administrador"}
        <div class="flex justify-evenly content-center items-center mt-5 w-full h-full ">
            <button disabled={!available || askedForLoan} on:click={() => {createLoan("pedido")}} class="h-min bg-accent rounded-md text-background p-5 text-lg hover:bg-primary transition">
                Solicitar Empréstimo
            </button>
            {#if $user.funcao === "chefe" || $user.funcao === "administrador"}
                <button disabled={!available || askedForLoan} on:click={() => createLoan("emAndamento")} class="h-min bg-accent rounded-md text-background p-5 text-lg hover:bg-primary transition">
                    Cadastrar Empréstimo
                </button>
            {/if}
        </div>
        {/if}
    </section>
    <section class="flex flex-col h-full p-6 max-h-screen w-1/2">
        <div class="flex gap-2 h-min w-fit self-end">
            <h1 class=" text-lg font-bold rounded-md bg-accent py-2 px-3 h-min w-fit text-background self-end mb-2">{item.categoria}</h1>
            {#if $user.funcao === "chefe" || $user.funcao === "administrador"}
            <a href={`/item/edit/${id}/${type}`} class=" text-lg font-bold rounded-md bg-secondary py-2 px-3 h-min w-fit text-background self-end mb-2 hover:bg-primary transition"> Editar </a>
            {/if}
        </div>
        <div class="flex flex-col content-center items-center p-5 items-right bg-{(item.type === "livro")? "primary" : "text"} rounded-lg h-full max-h-full">
            {#if item.type === "livro"}
            <img src={item.uriImagem? item.uriImagem  : defaultBook} alt="Falha ao carregar Imagem" class="imagem object-contain h-full max-h-screen w-full"/>
            {/if}
            {#if item.type === "materialDidatico"}
            <img src={item.uriImagem? item.uriImagem  : defaultMaterial} alt="Falha ao carregar Imagem" class="imagem object-contain h-full max-h-screen w-full"/>
            {/if}
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

    :disabled {
        opacity: 0.5;
    }
    .imagem {
        max-height: 80vh;
    }
</style>