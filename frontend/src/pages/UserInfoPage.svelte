<script >
    import { onMount } from "svelte";
    import { api } from "../api";
    import { ShieldHalf, KeyRound, Backpack } from "lucide-svelte"
    import defaultUser from "../assets/default_user.png"
    import { user } from "../stores/user";

    export let params
    let id = params.id

    let userInfo = {}

    function fecthData() {
        api.get(`/user/${id}`).then((res) => {
            userInfo = res.data
        }).catch((er) => alert(er.message))

        return () => {}
    }

    onMount(fecthData())

</script>

<main class="flex min-h-full w-full h-full justify-center">
    <section class="flex flex-col h-auto w-1/2 items-left pl-24 ">
        <div class="item_type" >
            {#if userInfo.funcao == "estudante"}
                <Backpack size=48 class="absolute top-16 left-12 text-primary"/>
                <h1 class='pl-10 relative -left-10 top-3 text-primary'>
                    {userInfo.nome} {userInfo.sobrenome}
                </h1>
            {/if}
            {#if userInfo.funcao == "chefe"}
                <KeyRound size=48 class="absolute top-16 left-12 text-primary"/>
                <h1 class='pl-10 relative -left-10 top-3 text-primary'>
                    {userInfo.nome} {userInfo.sobrenome}
                </h1>
            {/if}
            {#if userInfo.funcao == "administrador"}
                <ShieldHalf size=48 class="absolute top-16 left-14 text-text"/>
                <h1 class='pl-10 relative -left-10 top-3 text-primary'>
                    {userInfo.nome} {userInfo.sobrenome}
                </h1>
            {/if}
        </div>
        <div class=" flex bg-secondary w-full p-6 mt-10 text-text rounded-sm leading-7">{userInfo.login}</div>
    </section>
    
    <section class="flex flex-col h-full p-6 max-h-screen w-1/2">
        <div class="flex gap-2 h-min w-fit self-end">
            <h1 class=" text-lg font-bold rounded-md bg-accent py-2 px-3 h-min w-fit text-background self-end mb-2">{userInfo.funcao}</h1>
            {#if $user.funcao === "administrador"}
                <a href={`/user/edit/${id}`} class=" text-lg font-bold rounded-md bg-secondary py-2 px-3 h-min w-fit text-background self-end mb-2 hover:bg-primary transition"> Editar </a>
            {/if}
        </div>
        {#if userInfo.funcao === "administrador"}
            <div class="flex flex-col content-center items-center p-5 items-right bg-red-800 rounded-lg h-full max-h-full">
                <img src={userInfo.uriImagem? userInfo.uriImagem  : defaultUser} alt="Falha ao carregar Imagem" class="imagem object-contain h-full max-h-screen w-full"/>
            </div>
        {/if}
        {#if userInfo.funcao === "chefe" || userInfo.funcao === "estudante"}
            <div class="flex flex-col content-center items-center p-5 items-right bg-{(userInfo.funcao === "estudante")? "primary" : "text"} rounded-lg h-full max-h-full">
                <img src={userInfo.uriImagem? userInfo.uriImagem  : defaultUser} alt="Falha ao carregar Imagem" class="imagem object-contain h-full max-h-screen w-full"/>
            </div>
        {/if}
    </section>
</main>

<style>
    .item_type {
        font-size: 3rem;
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