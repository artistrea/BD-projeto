<script>
	import { onMount } from "svelte";
	import { api } from "../api";
    import { ShieldHalf, KeyRound, Backpack } from "lucide-svelte"

    let users = [];
	let selectedTypes = [];
	function fetchData() {
		api.get("/users").then((res) => {
			users = res.data;
		}).catch((er) => alert(er.message))

		return () => {};
    };
    
	onMount(fetchData());
</script>
<div class="pl-20 flex justify-between relative">
	<div class="py-8 mx-auto">
		<h1 class="text-4xl font-bold tracking-tight text-opacity-80 text-text">
			Inventário	
		</h1>
		<p class="max-w-prose mt-1 text-sm text-opacity-70 text-text leading-6">
			Estes são os usuários cadastrados no projeto. Você pode adicionar um novo usuário ou editar os dados de um usuário já existente.
			É necessário um admin para realizar esta operação.
		</p>

		<main class="mt-2">
			<ul class="flex flex-col gap-4 p-8">
				{#each users.filter((user) => selectedTypes.length === 0 || selectedTypes.some(t => t === user.funcao)) as user (user.id)}
					{#if user.funcao === "estudante"}
						<li class="bg-primary text-background text-opacity-90 rounded relative">
              <a href={`/user/${user.id}`}>
                <Backpack class="absolute top-4 -left-8 text-primary" />
                <div class="flex justify-between">
                  <h2 class="pt-4 pb-2 pl-4">
                    <span class="text-xl">{user.nome} {user.sobrenome}</span>
                    <br>
                    <span class="opacity-70 text-sm">
                      {user.login}
                    </span>
                  </h2>
                  <span class="text-sm font-bold rounded-bl bg-accent py-2 px-3 h-min ">{user.funcao}</span>
                </div>
              </a>
            </li>
					{/if}
                    {#if user.funcao === "chefe"}
						<li class="bg-text text-background text-opacity-90 rounded relative">
              <a href={`/user/${user.id}`}>
                <KeyRound class="absolute top-4 -left-8 text-primary" />
                <div class="flex justify-between">
                  <h2 class="pt-4 pb-2 pl-4">
                    <span class="text-xl">{user.nome} {user.sobrenome}</span>
                    <br>
                    <span class="opacity-70 text-sm">
                      {user.login}
                    </span>
                  </h2>
                  <span class="text-sm font-bold rounded-bl bg-accent py-2 px-3 h-min ">{user.funcao}</span>
                </div>
              </a>
						</li>
					{/if}
                    {#if user.funcao === "administrador"}
						<li class="bg-red-800 text-background text-opacity-90 rounded relative">
              <a href={`/user/${user.id}`}>
                <ShieldHalf class="absolute top-4 -left-8 text-primary" />
                <div class="flex justify-between">
                  <h2 class="pt-4 pb-2 pl-4">
                    <span class="text-xl">{user.nome} {user.sobrenome}</span>
                    <br>
                    <span class="opacity-70 text-sm">
                      {user.login}
                    </span>
                  </h2>
                  <span class="text-sm font-bold rounded-bl bg-accent py-2 px-3 h-min ">{user.funcao}</span>
                </div>
              </a>
						</li>
					{/if}
				{/each}
			</ul>
		</main>
	</div>

	<aside class="bg-secondary shadow-inner py-4 h-screen sticky top-0">
		<h2 class="px-4 text-2xl font-bold tracking-tight">
			Filtros
		</h2>
		<p class="px-4 max-w-prose mt-1 text-sm text-opacity-70 text-text leading-6">
			Escolha a função que você deseja ver dentre os usuários.
		</p>
		<div class="py-2">
			<fieldset class="border border-gray-400 rounded flex flex-col">
        <span class="flex gap-2 p-2">
          <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white rounded checked:bg-primary my-auto" type="checkbox" name="estudante" id="estudante" checked={selectedTypes.some(t => t === "estudante")} on:change={(e) => !e.currentTarget.checked ? selectedTypes = selectedTypes.filter(t => t!== "estudante") : selectedTypes = [...selectedTypes, "estudante"]}>
          <label for="estudante">
            Estudante
          </label>
        </span>
        <span class="flex gap-2 p-2">
            <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white rounded checked:bg-primary my-auto" type="checkbox" name="chefe" id="chefe" checked={selectedTypes.some(t => t === "chefe")} on:change={(e) => !e.currentTarget.checked ? selectedTypes = selectedTypes.filter(t => t!== "chefe") : selectedTypes = [...selectedTypes, "chefe"]}>
            <label for="chefe">
              Chefe
            </label>
        </span>
        <span class="flex gap-2 p-2">
          <input class="bg-origin-content appearance-none border border-gray-400 w-4 h-4 bg-white rounded checked:bg-primary my-auto" type="checkbox" name="administrador" id="administrador" checked={selectedTypes.some(t => t === "administrador")} on:change={(e) => !e.currentTarget.checked ? selectedTypes = selectedTypes.filter(t => t!== "administrador") : selectedTypes = [...selectedTypes, "administrador"]}>
          <label for="administrador">
            Administrador
          </label>
        </span>
			</fieldset>
		</div>
	</aside>
</div>

<style>
  input:checked {
    background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M12.207 4.793a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-2-2a1 1 0 011.414-1.414L6.5 9.086l4.293-4.293a1 1 0 011.414 0z'/%3e%3c/svg%3e")
  }
</style>