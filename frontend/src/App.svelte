<script lang="ts">
  import HomePage from './pages/InventoryPage.svelte'
  import LoginPage from "./pages/LoginPage.svelte";
  import AdminPage from './pages/AdminPage.svelte';
  import NavbarLayout from "./layouts/NavbarLayout.svelte";
  import type { ComponentType } from "svelte";
  import { user } from "./stores/user"
  import router, {  createRoute } from "./router/index"

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

  createRoute("/admin", () => page = AdminPage, {
    middlewares: [
      () => requireAuthLoggedIn("administrador")
    ]
  });

  createRoute("/inventario", () => page = HomePage, {
    middlewares: [
      () => requireAuthLoggedIn("estudante")
    ]
  });

  router.start()
</script>

{#if page === LoginPage}
  <LoginPage />
{/if}
{#if page !== LoginPage}
  <NavbarLayout {page} {params} />
{/if}
