<script>
    export let page;
    export let params;
</script>


<nav>
  <ul class="flex gap-2 justify-center bg-secondary">
    <li>
      <a class="block py-2 px-4 hover:bg-background transition-colors" href="/">Vá pra home</a>
    </li>
    <li>
      <a class="block py-2 px-4 hover:bg-background transition-colors" href="/login">Faça login</a>
    </li>
  </ul>
</nav>  

<svelte:component this="{page}" params="{params}" />