<script lang="ts">
  import router from "page"
  import HomePage from './pages/HomePage.svelte'
  import LoginPage from "./pages/LoginPage.svelte";
  import NavbarLayout from "./layouts/NavbarLayout.svelte";
  import type { ComponentType } from "svelte";

  let page: ComponentType;
  let params: any;
  let user = null;

  // only unauth route:
  router('/login', () => page = LoginPage);

  function requireAuthLoggedIn(authLevel: "administrador" | "chefe" | "estudante") {
    if (!user) router.redirect("/login");

    if (user.funcao === "administrador") return;
    if (authLevel !== "administrador" && user.funcao === "chefe") return;
    if (authLevel === "estudante" && user.funcao === "estudante") return;
    
    router.redirect("/login");
  }

  function declareRoute(path: string, component: ComponentType, authLevel: "administrador" | "chefe" | "estudante" = "estudante") {
    router(path, () => {
      requireAuthLoggedIn(authLevel);
      page = component;
    })
  }

  declareRoute("/", HomePage);

  router.start();
</script>

{#if page === LoginPage}
  <LoginPage />
{/if}
{#if page !== LoginPage}
  <NavbarLayout {page} {params} />
{/if}
