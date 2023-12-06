import axios from "axios";
import { writable } from "svelte/store";
import { api } from "../api";

const session = writable(null);

export function login(email: string, password: string) {
  return api
    .post("/auth/login", {
      login: email || "",
      password: password || "",
    })
    .then((res) => session.set(res.data));
}
