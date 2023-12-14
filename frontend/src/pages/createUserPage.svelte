<script >
    import { api } from "../api";
    import router from "page"
    
    let user = {
        'login' : '',
        'uriImagem' : undefined,
        'nome' : '',
        'sobrenome' : '',
        'funcao' : '',
        'senha' : ''
    }

    function handleSubmit(e) {
        e.preventDefault()
       
        if (user.login === '' || user.nome === ''  || user.sobrenome === ''  || user.funcao === ''  || user.senha === '') {
            alert("ERRO, campo incompleto.")
            return
        }

        if (user.login.indexOf('@') === -1) {
            alert("ERRO, o login não é um email válido.")
            return
        }

        api.post("/user", user).then((res) => {
            alert("Item cadastrado com sucesso.")
            router.redirect("/users")
        }).catch((er) => alert(er.message))
    }
</script>

<main class="flex flex-col min-h-screen w-full items-center">
    <h1 class="text-4xl font-bold tracking-tight text-opacity-80 text-text mt-10">
        Cadastrar Novo Usuário	
    </h1>
    <p class="max-w-prose text-sm text-opacity-70 text-text leading-6 mt-3">
        Esta é a página para cadastramento de um novo usuário. <br/>
        É necessário um admin para realizar o cadastro.
    </p>
    <form on:submit={handleSubmit} class="bg-secondary rounded flex flex-col p-8 h-auto justify-center mt-10 w-1/3">
        <div class="flex flex-col">
            <label class="pt-4" for="titulo">Nome:</label>
            <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="nome" bind:value={user.nome}>
        </div>

        <div class="flex flex-col">
            <label class="pt-4" for="titulo">Sobrenome:</label>
            <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="sobrenome" bind:value={user.sobrenome}>
        </div>

        <div class="flex flex-col">
            <label class="pt-4" for="titulo">Login:</label>
            <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="login" bind:value={user.login}>
        </div>

        <div class="flex flex-col">
            <label class="pt-4" for="titulo">Senha:</label>
            <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="senha" bind:value={user.senha}>
        </div>

        <div class="flex flex-col">
            <label class="pt-4" for="autor">Função:</label>
            <fieldset class="border border-gray-400 rounded flex justify-evenly" id="tipo">
                <span class="flex gap-2 p-2">
                    <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white rounded-full checked:bg-primary my-auto" type="radio" bind:group={user.funcao} value="estudante" name="estudante" id="estudante" >
                    <label for="estudante">
                        Estudante
                    </label>
                </span>
                <span class="flex gap-2 p-2">
                    <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white rounded-full checked:bg-primary my-auto" type="radio" bind:group={user.funcao} value="chefe" name="chefe" id="chefe" >
                    <label for="chefe">
                        Chefe
                    </label>
                </span>
                <span class="flex gap-2 p-2">
                    <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white  rounded-full checked:bg-primary my-auto" type="radio" bind:group={user.funcao} value="administrador" name="administrador" id="administrador">
                    <label for="administrador">
                        Administrador
                    </label>
                </span>
            </fieldset>
        </div>

        <div class="flex flex-col">
            <label class="pt-4" for="titulo">Url da Imagem:</label>
            <input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="senha" bind:value={user.uriImagem}>
        </div>

        <button class="hover:scale-[1.01] transition-all rounded px-4 py-2 bg-primary text-background mt-4 disabled:opacity-50">Cadastrar</button>
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