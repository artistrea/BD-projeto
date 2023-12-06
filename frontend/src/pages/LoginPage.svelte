<script >
	import { login } from "../stores/user"
	import router from "page"

	let handle;
	let password;

	function handleSubmit(e) {
		e.preventDefault();
		
		login(handle, password)
			.then(() => {
				router.redirect("/");
				alert("Logado com sucesso!")
			})
			.catch(err => {
				if (err.response.status === 401) alert("Handle e/ou senha erradas")
				else alert("Ocorreu um erro inesperado no servidor!")
			})
	}
</script>

<main class="flex min-h-screen w-full items-center justify-center">
	<form on:submit={handleSubmit} class="bg-secondary rounded flex flex-col p-8 h-96 justify-center">
		<div class="flex flex-col">
			<label class="pt-4" for="login">Login:</label>
			<input class="bg-transparent border-b border-primary px-4 py-2" type="text" id="login" bind:value={handle}>
		</div>
		<div class="flex flex-col">
			<label class="pt-4" for="password">Senha:</label>
			<input class="bg-transparent border-b border-primary px-4 py-2" type="password" id="password" bind:value={password}>
		</div>
		<button class="hover:scale-[1.01] transition-all rounded px-4 py-2 mt-auto bg-primary text-background">Entrar</button>
	</form>
</main>

<style>
</style>