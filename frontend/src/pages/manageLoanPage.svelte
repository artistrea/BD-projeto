<script>
    import { onMount } from "svelte";
    import { api } from "../api";


    let loans = []
    function fetchData() {
        api.get(`/loan`).then((res) => {
            loans = res.data
            console.log(loans)
        }).catch((er) => alert(er.message))
    }

    onMount(fetchData)

    let today = new Date()

    $: late = loans.filter((loan) => loan.status === "emAndamento" && new Date(loan.dataDeDevolucaoPrevista) < today)
    $: asked = loans.filter((loan) => loan.status === "pedido")
    $: onGoing = loans.filter((loan) => loan.status === "emAndamento" && new Date(loan.dataDeDevolucaoPrevista) >= today)
    $: returned = loans.filter((loan) => loan.status === "concluido")

    let filters = {
        status : []
    }

    function acceptLoan(loan) {
        let onGoing_loan = loans.find((l) => l.status === "emAndamento" && l.userId === loan.userId && l.itemId === loan.itemId && l.itemType === loan.itemType)
        loan.status = "emAndamento"
        api.put(`loan/${loan.userId}/${loan.itemId}/${loan.itemType}`, loan).then((res) => {
            if (onGoing_loan) {
                onGoing_loan.status = "concluido"
                onGoing_loan.dataDeDevolucaoPrevista = today.toISOString()
                api.put(`loan/${loan.userId}/${loan.itemId}/${loan.itemType}`, onGoing_loan).then((res) => {
                    alert("Pedido de Empréstimo Aceito.")
                    window.location.reload()
                }).catch((er) => alert(er.message + ' 1'))
            }
        }).catch((er) => alert(er.message))

    }

    function rejectLoan(loan) {
        let body = {
            dataDeEmprestimo : loan.dataDeEmprestimo,
            itemType : loan.itemType
        }
        api.delete(`loan/${loan.userId}/${loan.itemId}`, {data: body }).then((res) => {
            alert("Pedido de Empréstimo Recusado.")
            window.location.reload()
        }).catch((er) => alert(er.message))
    }

    function registerReturn(loan) {
        loan.status = "concluido"
        loan.dataDeDevolucaoPrevista = today.toISOString()
        api.put(`loan/${loan.userId}/${loan.itemId}/${loan.itemType}`, loan).then((res) => {
            alert("Devolução Registrada.")
            window.location.reload()
        }).catch((er) => alert(er.message))
    }

</script>
<div class="pl-20 flex justify-between relative">
    <div class="py-8 mx-auto w-full justify-center items-center">
        <h1 class="flex justify-center text-4xl font-bold tracking-tight text-opacity-80 text-text">
            Gerenciamento de Empréstimos	
        </h1>

        <main class="flex justify-evenly w-full mt-2">
            {#if !filters.status.length || filters.status.includes("atrasado")}
            <div>
                <h2 class="flex justify-center font-semibold text-3xl tracking-tight text-opacity-80 text-red-400 pt-6 w-full">
                    Atrasados	
                </h2>
                <ul class="flex flex-col gap-4 py-2 w-full">
                    {#each late as loan}
                    <li class="bg-text text-text text-opacity-90 rounded relative">
                        <div class="bg-text text-red-400 text-opacity-90 rounded relative pb-4 w-full">
                            <div class="flex justify-between">
                            <h2 class="pt-4 pl-4">
                                <b>Nome:   </b>
                                {loan.nome} {loan.sobrenome}
                                <br/>
                                    <b>Email:</b>
                                    {loan.login}
                            </h2>
                            <span class="text-sm text-background font-bold rounded-bl bg-accent py-2 px-3 h-min ml-4">{loan.itemType === "livro"? "Livro" : "Material Didático"}</span>
                        </div>
                        <h2 class="pt-4 pl-4">
                            <b>{loan.itemType === "livro"? "ISBN" : "Identificador"}:   </b>
                            {loan.itemId}
                        </h2>
                            <div class=" pl-4">
                                Data de Devolução Prevista: 
                                <b>{new Date(loan.dataDeDevolucaoPrevista).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b>
                            </div>
                            <div class=" pl-4">
                            Data do Empréstimo: 
                            <b>{new Date(loan.dataDeEmprestimo).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b>
                            </div>
                        </div>
                        <fieldset class=" bg-accent rounded-b flex justify-between text-background font-semibold py-1">
                            <button on:click={() => registerReturn(loan)} class="flex justify-center w-full">Registrar Devolução</button>
                        </fieldset>
                    </li>
                    {/each}
                </ul>
            </div>
            {/if}

            {#if !filters.status.length || filters.status.includes("pedido")}
            <div>
                <h2 class="flex justify-center font-semibold text-3xl tracking-tight text-accent pt-6">
                    Pedidos
                </h2>
                <ul class="flex flex-col gap-4 py-2">
                    {#each asked as loan}
                    <li class="bg-secondary text-text text-opacity-90 rounded relative">
                            <div class="flex justify-between">
                                <h2 class="pt-4 pl-4">
                                    <b>Nome:   </b>
                                    {loan.nome} {loan.sobrenome}
                                    <br/>
                                    <b>Email:</b>
                                    {loan.login}
                                </h2>
                                <span class="text-sm text-background font-bold rounded-bl bg-accent py-2 px-3 h-min ml-4">{loan.itemType === "livro"? "Livro" : "Material Didático"}</span>
                            </div>
                            <h2 class="pt-4 pl-4">
                                <b>{loan.itemType === "livro"? "ISBN" : "Identificador"}:   </b>
                                {loan.itemId}
                            </h2>
                            <div class=" pl-4">
                            Data do Pedido: 
                            <b>{new Date(loan.dataDeEmprestimo).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b>
                            </div>
                            <fieldset class=" bg-accent rounded-b flex justify-between text-background font-semibold py-1">
                                <button on:click={() => acceptLoan(loan)} class="flex justify-center w-full">Aceitar</button>
                                |
                                <button on:click={() => rejectLoan(loan)} class="flex justify-center w-full">Recusar</button>
                            </fieldset>
                    </li>
                    {/each}
                </ul>
            </div>
            {/if}

            {#if !filters.status.length || filters.status.includes("emAndamento")}
            <div>
                <h2 class="flex justify-center font-semibold text-3xl tracking-tight text-opacity-80 text-primary pt-6">
                    Em Andamento	
                </h2>
                <ul class="flex flex-col gap-4 py-2">
                    {#each onGoing as loan}
                    <li class="fbg-primary text-text text-opacity-90 rounded relative">
                        <div class="bg-primary text-background text-opacity-90 rounded relative pb-4 w-full">
                            <div class="flex justify-between">
                            <h2 class="pt-4 pl-4">
                                <b>Nome:   </b>
                                {loan.nome} {loan.sobrenome}
                                <br/>
                                    <b>Email:</b>
                                    {loan.login}
                            </h2>
                            <span class="text-sm text-background font-bold rounded-bl bg-accent py-2 px-3 h-min ml-4">{loan.itemType === "livro"? "Livro" : "Material Didático"}</span>
                            </div>
                            <h2 class="pt-4 pl-4">
                                <b>{loan.itemType === "livro"? "ISBN" : "Identificador"}:   </b>
                                {loan.itemId}
                            </h2>
                            <div class=" pl-4">
                            Data de Devolução Prevista:
                                <b>{new Date(loan.dataDeDevolucaoPrevista).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b> 
                            </div>
                            <div class=" pl-4">
                            Data do Empréstimo: 
                            <b>{new Date(loan.dataDeEmprestimo).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}</b>
                            </div>
                        </div>
                        <fieldset class=" bg-accent rounded-b flex justify-between text-background font-semibold py-1">
                            <button on:click={() => registerReturn(loan)} class="flex justify-center w-full">Registrar Devolução</button>
                        </fieldset>
                    </li>
                    {/each}
                </ul>
            </div>
            {/if}

            {#if !filters.status.length || filters.status.includes("concluido")}
            <div>
                <h2 class="flex justify-center font-semibold text-3xl tracking-tight text-opacity-80 text-text pt-6">
                    Concluidos
                </h2>
                <ul class="flex flex-col gap-4 py-2">
                    {#each returned as loan}
                    <li class="bg-accent text-background text-opacity-90 rounded relative pb-4">
                            <div class="flex justify-between">
                                <h2 class="pt-4 pl-4">
                                    <b>Nome:   </b>
                                    {loan.nome} {loan.sobrenome}
                                    <br/>
                                    <b>Email:</b>
                                    {loan.login}
                                </h2>
                                <span class="text-sm text-text font-bold rounded-bl bg-secondary py-2 px-3 h-min ml-4">{loan.itemType === "livro"? "Livro" : "Material Didático"}</span>
                            </div>
                            <h2 class="pt-4 pl-4">
                                <b>{loan.itemType === "livro"? "ISBN" : "Identificador"}:   </b>
                                {loan.itemId}
                            </h2>
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
            </div>
            {/if}
        </main>

    </div>
    <aside class="bg-secondary shadow-inner py-4 h-screen sticky top-0">
        <h2 class="px-4 text-2xl font-bold tracking-tight">
            Filtros
        </h2>
        <p class="px-4 max-w-prose mt-1 text-sm text-opacity-70 text-text leading-6">
            Escolha quais status você quer gerenciar.
        </p>
        <div class="py-2">
            <fieldset class="border border-gray-400 rounded justify-evenly m-2" id="tipo">
                <span class="flex gap-2 p-2">
                <input class="bg-origin-content appearance-none rounded border border-gray-400 w-4 h-4 bg-white checked:bg-primary my-auto" checked={filters.status.some((s) => s === 'atrasado')} type="checkbox" on:change={(e) => !e.currentTarget.checked ? filters.status = filters.status.filter(s => s !== "atrasado") : filters.status = [...filters.status, "atrasado"]} name="atrasado" id="atrasado" >
                <label for="atrasado">
                    Atrasado
                </label>
                </span>
                <span class="flex gap-2 p-2">
                    <input class="bg-origin-content appearance-none rounded border border-gray-400 w-4 h-4 bg-white  checked:bg-primary my-auto" checked={filters.status.some((s) => s === 'pedido')}  type="checkbox"on:change={(e) => !e.currentTarget.checked ? filters.status = filters.status.filter(t => t!== "pedido") : filters.status = [...filters.status, "pedido"]} name="pedido" id="pedido">
                    <label for="pedido">
                        Pedido
                    </label>
                </span>
                <span class="flex gap-2 p-2">
                <input class="bg-origin-content appearance-none rounded border border-gray-400 w-4 h-4 bg-white  checked:bg-primary my-auto" checked={filters.status.some((s) => s === 'emAndamento')}  type="checkbox"on:change={(e) => !e.currentTarget.checked ? filters.status = filters.status.filter(t => t!== "emAndamento") : filters.status = [...filters.status, "emAndamento"]} name="emAndamento" id="emAndamento">
                <label for="emAndamento">
                    Em Andamento
                </label>
                </span>
                
                <span class="flex gap-2 p-2">
                    <input class="bg-origin-content appearance-none rounded border border-gray-400 w-4 h-4 bg-white  checked:bg-primary my-auto" checked={filters.status.some((s) => s === 'concluido')}  type="checkbox"on:change={(e) => !e.currentTarget.checked ? filters.status = filters.status.filter(t => t!== "concluido") : filters.status = [...filters.status, "concluido"]} name="concluido" id="concluido">
                    <label for="concluido">
                        Concluido
                    </label>
                </span>
            </fieldset>
        </div>
    </aside>
</div>
<style>

</style>