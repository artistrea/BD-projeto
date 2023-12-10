<script>
    export let page;
    export let params;
</script>


<nav>
  <ul class="flex gap-2 justify-between px-4 bg-secondary">
    <li>
      <a class="block py-2 px-4 hover:bg-background transition-colors" href="/">Menu</a>
    </li>
    <li>
      <a class="block py-2 px-4 hover:bg-background transition-colors" href="/inventario">Inventário</a>
    </li>
    <li>
      <button class="block py-2 px-4 hover:bg-background transition-colors">Sair</button>
    </li>
  </ul>
</nav>  

<svelte:component this={page} {params} />