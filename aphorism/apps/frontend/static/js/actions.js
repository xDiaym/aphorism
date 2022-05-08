import { api } from "./api.js";

const setToken = token => localStorage.setItem('token', token);
const getToken = () => localStorage.getItem('token');

export const redirectToMyFeed = () => {
  const token = getToken();
  const init = { headers: { "Authorization": `Bearer ${token}` } };
  fetch("/feed/me", init).then(res => {
    if (res.redirected) window.location = res.url;
  });
}

export async function register(email, password, slug, name) {
  const response = await api.auth.register({email, password, slug, name});
  setToken(response.token);
}

export async function login(email, password) {
  const response = await api.auth.login({ email, password });
  setToken(response.token);
}
