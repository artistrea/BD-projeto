<script lang="ts">
  import HomePage from './pages/InventoryPage.svelte'
  import LoginPage from "./pages/LoginPage.svelte";
  import NavbarLayout from "./layouts/NavbarLayout.svelte";
  import ItemPage from './pages/ItemPage.svelte';
  import CreateItemPage from './pages/createItemPage.svelte';
  import type { ComponentType } from "svelte";
  import { user } from "./stores/user"
  import router, {  createRoute } from "./router/index"
    import EditItemPage from './pages/editItemPage.svelte';

  let page: ComponentType;
  let params: any;

  // only unauth route:
  createRoute('/login', () => {
    if ($user) router.redirect("/")
    else page = LoginPage
  });


  function requireAuthLoggedIn(authLevel: "administrador" | "chefe" | "estudante") {
    if (!$user) {
      router.redirect("/login");
      return false;
    };

    if ($user.funcao === "administrador") return true;
    if (authLevel !== "administrador" && $user.funcao === "chefe") return true;
    if (authLevel === "estudante" && $user.funcao === "estudante") return true;
    
    router.redirect("/login");
    return false;
  }

  createRoute("/inventario", () => page = HomePage, {
    middlewares: [
      () => requireAuthLoggedIn("estudante")
    ]
  });

  createRoute("/item/:id/:type", (ctx) => {page = ItemPage; params=ctx.params}, {
    middlewares: [
      () => requireAuthLoggedIn("estudante")
    ],
  })

  createRoute("/novoItem", () => page = CreateItemPage, {
    middlewares: [
      () => requireAuthLoggedIn("chefe")
    ]
  })

  createRoute("/item/edit/:id/:type", (ctx) => {page = EditItemPage; params=ctx.params}, {
    middlewares: [
      () => requireAuthLoggedIn("chefe")
    ]
  })

  router.start()
</script>

{#if page === LoginPage}
  <LoginPage />
{/if}
{#if page !== LoginPage}
  <NavbarLayout {page} {params} />
{/if}
