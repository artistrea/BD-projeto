<script>
    import { user } from "../stores/user";
    export let page;
    export let params;

    import { logout } from "../stores/user";
  	import router from "page";

    function logoutAccount() {
		  logout().then(() => {
        router.redirect("/login");
        alert("Logout com sucesso!")
      })
      .catch(err => {
        if (err.response.status === 401) alert("Nenhum usuário está logado!")
        else alert("Ocorreu um erro inesperado no servidor!")
      })
	}
</script>


<nav>
  <ul class="flex gap-2 justify-between px-4 bg-secondary">
    <li>
      <a class="block py-2 px-4 hover:bg-background transition-colors" href="/">Menu</a>
    </li>
    <li class="flex">
      <a class="block py-2 px-4 hover:bg-background transition-colors" href="/meusEmprestimos">Meus Empréstimos</a>
      <a class="block py-2 px-4 hover:bg-background transition-colors" href="/inventario">Inventário</a>
      {#if $user?.funcao === "administrador" || $user?.funcao === "chefe"}
        <a class="block py-2 px-4 hover:bg-background transition-colors" href="/novoItem">Novo Item</a>
        <a class="block py-2 px-4 hover:bg-background transition-colors" href="/gerenciarEmprestimos">Gerenciar Emprestimos</a>
        <a class="block py-2 px-4 hover:bg-background transition-colors" href="/users">Gerenciar Usuários</a>
      {/if}
      {#if $user?.funcao === "administrador"}
        <a class="block py-2 px-4 hover:bg-background transition-colors" href="/novoUsuario">Novo Usuário</a>
      {/if}
    </li>
    <li>
      <button on:click={logoutAccount} class="block py-2 px-4 hover:bg-background transition-colors">Sair</button>
    </li>
  </ul>
</nav>  

<svelte:component this={page} {params} />