<script>
    import { onMount } from "svelte";
    import { api } from "../api";
    import { user } from "../stores/user";


    let loans = []
    function fetchData() {
        api.get(`/loan/${$user.id}`).then((res) => {
            loans = res.data
        }).catch((er) => alert(er.message))
    }

    onMount(fetchData)

    let today = new Date()
    const ALLOW_TIME_TO_ASK_RENOVATION = 7*24*60*60*1000  // 1 uma semana em ms

    $: late = loans.filter((loan) => loan.status === "emAndamento" && new Date(loan.dataDeDevolucaoPrevista) < today)
    $: onGoing = loans.filter((loan) => loan.status === "emAndamento" && new Date(loan.dataDeDevolucaoPrevista) >= today)
    $: asked = loans.filter((loan) => loan.status === "pedido")
    $: returned = loans.filter((loan) => loan.status === "concluido")

    function askRenovation(loan) {
        loan.dataDeEmprestimo = today.toUTCString()
        loan.dataDeDevolucaoPrevista = new Date(today.setMonth(today.getMonth() + 1)).toDateString()
        loan.status = 'pedido'

        api.post("/loan", loan).then((res) => {
            alert("Renovação Solicitada.")
            window.location.reload()
        }).catch((er) => alert(er.message))
    }

</script>

<div class="py-8 mx-auto w-1/3">
    <h1 class="flex justify-center text-4xl font-bold tracking-tight text-opacity-80 text-text">
        Meus Empréstimos	
    </h1>
    <p class="max-w-prose mt-1 text-sm text-opacity-70 text-text leading-6">
        Estes são todos os seus empréstimos. <br/>
        Se houver algum atrasado pedimos, por obséquio, que retorne o item o mais rápido o possível, se não o fizer penalizações serão aplicáveis.
    </p>

    <main class="mt-2">
        {#if late.length}
        <h2 class="flex justify-center font-semibold text-3xl tracking-tight text-opacity-80 text-red-400 pt-6 w-full">
            Atrasados	
        </h2>
        <ul class="flex flex-col gap-4 py-2 w-full">
            {#each late as loan}
            <li class="flex w-full items-center relative">
                <div class="bg-text text-red-400 text-opacity-90 rounded relative pb-4 w-full">
                    <div class="flex justify-between">
                    <h2 class="pt-4 pl-4">
                        <b>{loan.itemType === "livro"? "ISBN" : "Identificador"}:   </b>
                        {loan.itemId}
                    </h2>
                    <span class="text-sm text-background font-bold rounded-bl bg-accent py-2 px-3 h-min ml-4">{loan.itemType === "livro"? "Livro" : "Material Didático"}</span>
                    </div>
                    <div class=" pl-4">
                        Data de Devolução Prevista: 
                        <b>{new Date(loan.dataDeDevolucaoPrevista).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b>
                    </div>
                    <div class=" pl-4">
                    Data do Empréstimo: 
                    <b>{new Date(loan.dataDeEmprestimo).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b>
                    </div>
                </div>
                {#if (!loans.some((l) => l.status === "pedido" && l.itemId === loan.itemId))}
                    <button on:click|once={() => {askRenovation(loan);} }  class=" absolute bg-accent p-5 rounded-md font-semibold text-background hover:bg-primary transition -right-48 w-fit">Pedir Renovação</button>
                {/if}
            </li>
            {/each}
        </ul>
        {/if}

        {#if onGoing.length}
        <h2 class="flex justify-center font-semibold text-3xl tracking-tight text-opacity-80 text-primary pt-6">
            Em Andamento	
        </h2>
        <ul class="flex flex-col gap-4 py-2">
            {#each onGoing as loan}
            <li class="flex w-full items-center relative">
                <div class="bg-primary text-background text-opacity-90 rounded relative pb-4 w-full">
                    <div class="flex justify-between">
                    <h2 class="pt-4 pl-4">
                        <b>{loan.itemType === "livro"? "ISBN" : "Identificador"}:   </b>
                        {loan.itemId}
                    </h2>
                    <span class="text-sm text-background font-bold rounded-bl bg-accent py-2 px-3 h-min ml-4">{loan.itemType === "livro"? "Livro" : "Material Didático"}</span>
                    </div>
                    <div class=" pl-4">
                    Data de Devolução Prevista:
                        <b>{new Date(loan.dataDeDevolucaoPrevista).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b> 
                    </div>
                    <div class=" pl-4">
                    Data do Empréstimo: 
                    <b>{new Date(loan.dataDeEmprestimo).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b>
                    </div>
                </div>
                {#if (new Date(loan.dataDeDevolucaoPrevista).getTime() - today.getTime() < ALLOW_TIME_TO_ASK_RENOVATION && !loans.some((l) => l.status === "pedido" && l.itemId === loan.itemId))}
                    <button on:click|once={() => {askRenovation(loan);} }  class=" absolute bg-accent p-5 rounded-md font-semibold text-background hover:bg-primary transition -right-48 w-fit">Pedir Renovação</button>
                {/if}
            </li>
            {/each}
        </ul>
        {/if}

        {#if asked.length}
        <h2 class="flex justify-center font-semibold text-3xl tracking-tight text-accent pt-6">
            Pedidos
        </h2>
        <ul class="flex flex-col gap-4 py-2">
            {#each asked as loan}
            <li class="bg-secondary text-text text-opacity-90 rounded relative pb-4">
                    <div class="flex justify-between">
                    <h2 class="pt-4 pl-4">
                        <b>{loan.itemType === "livro"? "ISBN" : "Identificador"}:   </b>
                        {loan.itemId}
                    </h2>
                    <span class="text-sm text-background font-bold rounded-bl bg-accent py-2 px-3 h-min ml-4">{loan.itemType === "livro"? "Livro" : "Material Didático"}</span>
                    </div>
                    <div class=" pl-4">
                    Data do Pedido: 
                    <b>{new Date(loan.dataDeEmprestimo).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b>
                    </div>
            </li>
            {/each}
        </ul>
        {/if}

        {#if returned.length}
        <h2 class="flex justify-center font-semibold text-3xl tracking-tight text-opacity-80 text-text pt-6">
            Concluidos
        </h2>
        <ul class="flex flex-col gap-4 py-2">
            {#each returned as loan}
            <li class="bg-accent text-background text-opacity-90 rounded relative pb-4">
                    <div class="flex justify-between">
                    <h2 class="pt-4 pl-4">
                        <b>{loan.itemType === "livro"? "ISBN" : "Identificador"}:   </b>
                        {loan.itemId}
                    </h2>
                    <span class="text-sm text-text font-bold rounded-bl bg-secondary py-2 px-3 h-min ml-4">{loan.itemType === "livro"? "Livro" : "Material Didático"}</span>
                    </div>
                    <div class=" pl-4">
                    Data de Devolução:
                        <b>{new Date(loan.dataDeDevolucaoPrevista).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b> 
                    </div>
                    <div class=" pl-4">
                    Data do Pedido: 
                    <b>{new Date(loan.dataDeEmprestimo).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b>
                    </div>
            </li>
            {/each}
        </ul>
        {/if}
    </main>
</div>

<style>

</style>