import Cookies from "js-cookie";
import { writable } from "svelte/store";
import { api } from "../api";

type UserFuntion = "administrador" | "chefe" | "estudante";

type User =
  | undefined
  | {
      id: number;
      uriImagem: string;
      funcao: UserFuntion;
      nome: string;
      sobrenome: string;
      login: string;
    };

export const user = writable<User>(undefined);
export let tryingToLoadUser: Promise<any>;

export async function login(email: string, password: string) {
  return api
    .post("/auth/login", {
      login: email || "",
      password: password || "",
    })
    .then((res) => {
      user.set(res.data.user);

      setDefaultAuthHeaders(res.data.user.login, res.data.authentication_token);

      Cookies.set("authentication_token", res.data.authentication_token);
      Cookies.set("login", res.data.user.login);
    });
}

export async function refetchCurrentUser() {
  console.log(1);
  return api.post("/user/atual").then((res) => {
    user.set(res.data);
  });
}

function setDefaultAuthHeaders(login: string, authentication_token: string) {
  api.defaults.headers.common["X-Auth-Login"] = login;
  api.defaults.headers.common["X-Auth-Token"] = authentication_token;
}

const storedAuthToken = Cookies.get("authentication_token");
const storedLogin = Cookies.get("login");

if (storedLogin && storedAuthToken) {
  setDefaultAuthHeaders(storedLogin, storedAuthToken);
  tryingToLoadUser = refetchCurrentUser()
    .then(() => {})
    .catch(() => {});
}
