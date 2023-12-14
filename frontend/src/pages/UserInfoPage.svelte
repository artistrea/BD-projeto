<script >
    import { api } from "../api";
    import { onMount } from "svelte";
    import router from "page"

    export let params;

    let id = params.id
    let type = params.type

</script>