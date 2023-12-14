<script >
    import { api } from "../api";
    import { onMount } from "svelte";
    import router from "page"

    export let params

    let id = params.id
    let type = params.funcao
    let userInfo = {}
    let password = ''


    function fecthData() {
        api.get(`/user/${id}`).then((res) => {
            userInfo = res.data
        }).catch((er) => alert(er.message))

        return () => {}
    }

    onMount(fecthData())

    function handleSubmit(e) {
        e.preventDefault()
        
        delete userInfo.id
        delete userInfo.funcao
        delete userInfo.hashSenha
        delete userInfo.authToken
        delete userInfo.login
        if (userInfo.uriImagem === null) {
            userInfo.uriImagem = ""
        }

        api.put(`/user/${id}`, userInfo).then((res) => {
            alert("Item editado com sucesso.")
            router.redirect(`/user/${id}/`)
        }).catch((er) => alert(er.message))
    }

    function handleSubmitFunction(e) {
        e.preventDefault()
        
        delete userInfo.id
        delete userInfo.login
        delete userInfo.authToken
        delete userInfo.nome
        delete userInfo.sobrenome
        delete userInfo.uriImagem
        delete userInfo.hashSenha
        
        api.put(`/user/${id}/function`, userInfo).then((res) => {
            alert("Item editado com sucesso.")
            router.redirect(`/user/${id}/`)
        }).catch((er) => alert(er.message))
    }

    function handleSubmitPassword(e) {
        e.preventDefault()
        
        let userPwdInfo = {
        'senha' : {
            'antiga' : '',
            'nova' : password
            },
        }
        
        api.put(`/user/${id}/password`, userPwdInfo).then((res) => {
            alert("Item editado com sucesso.")
            router.redirect(`/user/${id}/`)
        }).catch((er) => alert(er.message))
    }

    function deleteItem() {
        if (confirm("Confirme para deletar o Usuário.")) {
            api.delete(`/user/${id}`).then((res) => {
            alert("Item Deletado.")
            router.redirect(`/users/`)
        }).catch((er) => alert(er.message))
        }
    }

</script>

<main class="flex flex-col min-h-screen w-full items-center">
    <h1 class="text-4xl font-bold tracking-tight text-opacity-80 text-text mt-10">
        Editar <span class="text-accent">{userInfo.nome} {userInfo.sobrenome}</span>	
    </h1>
    <span class="text-accent">{userInfo.login}</span>
    <p class="max-w-prose mt-1 text-sm text-opacity-70 text-text leading-6 mt-3">
        Esta é a página de edição de um usuário. <br/>
        É necessário um administrador para realizar a edição.
    </p>
	<form on:submit={handleSubmit} class="bg-secondary rounded flex flex-col p-8 h-auto w-1/3 justify-center mt-10">
        <div class="flex flex-col">
            <label class="pt-4" for="titulo">Nome:</label>
            <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="titulo" bind:value={userInfo.nome}>
        </div>
        <div class="flex flex-col">
            <label class="pt-4" for="autor">Sobrenome:</label>
            <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="autor" bind:value={userInfo.sobrenome}>
        </div>
        <div class="flex flex-col">
            <label class="pt-4" for="uriImagem">Url da Imagem:</label>
            <input class="bg-transparent border-b border-primary px-4 py-2" type="url" id="uriImagem" bind:value={userInfo.uriImagem}>
        </div>
        <button class="hover:scale-[1.01] transition-all rounded px-4 py-2 bg-primary text-background mt-4 disabled:opacity-50">Editar</button>
	</form>

    <form on:submit={handleSubmitFunction} class="bg-secondary rounded flex flex-col p-8 h-auto w-1/3 justify-center mt-10">
        <div class="flex flex-col">
            <label class="pt-4" for="autor">Função:</label>
            <fieldset class="border border-gray-400 rounded flex justify-evenly" id="tipo">
                <span class="flex gap-2 p-2">
                    <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white rounded-full checked:bg-primary my-auto" type="radio" bind:group={userInfo.funcao} value="estudante" name="estudante" id="estudante" >
                    <label for="estudante">
                        Estudante
                    </label>
                </span>
                <span class="flex gap-2 p-2">
                    <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white rounded-full checked:bg-primary my-auto" type="radio" bind:group={userInfo.funcao} value="chefe" name="chefe" id="chefe" >
                    <label for="chefe">
                        Chefe
                    </label>
                </span>
                <span class="flex gap-2 p-2">
                    <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white  rounded-full checked:bg-primary my-auto" type="radio" bind:group={userInfo.funcao} value="administrador" name="administrador" id="administrador">
                    <label for="administrador">
                        Administrador
                    </label>
                </span>
            </fieldset>
        </div>
        <button class="hover:scale-[1.01] transition-all rounded px-4 py-2 bg-primary text-background mt-4 disabled:opacity-50">Editar</button>
	</form>
    <form on:submit={handleSubmitPassword} class="bg-secondary rounded flex flex-col p-8 h-auto w-1/3 justify-center mt-10">
        <div class="flex flex-col">
            <label class="pt-4" for="localizacao">Nova Senha:</label>
            <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="localizacao" bind:value={password}>
        </div>
        <button class="hover:scale-[1.01] transition-all rounded px-4 py-2 bg-primary text-background mt-4 disabled:opacity-50">Editar</button>
	</form>
    <button on:click={deleteItem} class="hover:scale-[1.01] transition-all rounded px-4 py-2 bg-accent text-background mt-4 disabled:opacity-50 bg-red-800 hover:text-red-500" >Deletar {userInfo.nome} {userInfo.sobrenome}</button>
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