<script>
    export let page;
    export let params;
</script>


<nav>
    <ul>
      <li>
        <a href="/">Vá pra home</a>
      </li>
    </ul>
  </nav>  

<svelte:component this="{page}" params="{params}" />