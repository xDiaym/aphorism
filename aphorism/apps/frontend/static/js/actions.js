import { api } from "./api.js";

const setToken = token => localStorage.setItem('token', token);
const getToken = () => localStorage.getItem('token');

export async function register(email, password, slug, name) {
  const response = await api.auth.register({email, password, slug, name});
  setToken(response.token);
}
