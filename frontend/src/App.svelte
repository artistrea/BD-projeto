<script lang="ts">
  import HomePage from './pages/InventoryPage.svelte'
  import LoginPage from "./pages/LoginPage.svelte";
  import UsersPage from './pages/UsersPage.svelte';
  import UserInfoPage from './pages/UserInfoPage.svelte';
  import EditUserPege from './pages/editUserPege.svelte';
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

  createRoute("/users", () => page = UsersPage, {
    middlewares: [
      () => requireAuthLoggedIn("chefe")
    ]
  });

  createRoute("/user/:id", (ctx) => {page = UserInfoPage; params=ctx.params}, {
    middlewares: [
      () => requireAuthLoggedIn("chefe")
    ],
  })

  createRoute("/user/edit/:id", (ctx) => {page = EditUserPege; params=ctx.params}, {
    middlewares: [
      () => requireAuthLoggedIn("administrador")
    ],
  })

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
