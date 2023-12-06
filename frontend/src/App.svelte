<script>
  import router from "page"
  import HomePage from './pages/HomePage.svelte'
  import LoginPage from "./pages/LoginPage.svelte";
  import NavbarLayout from "./layouts/NavbarLayout.svelte";

  let page;
  let params;
  let user = null;

  function authUser() {
    if (!user) router.redirect("/login")
  }

  router('/', () => page = HomePage);
  router('/login', () => page = LoginPage);



  router.start();
</script>

{#if page === LoginPage}
  <LoginPage />
{/if}
{#if page !== LoginPage}
  <NavbarLayout {page} {params} />
{/if}
