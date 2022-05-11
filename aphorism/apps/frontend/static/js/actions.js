import { api } from "./api.js";

const setToken = token => localStorage.setItem('token', token);
const getToken = () => localStorage.getItem('token');

export const isMe = (slug) => slug === getMySlug();

export const redirectToMyFeed = () => {
  const token = getToken();
  const init = { headers: { "Authorization": `Bearer ${token}` } };
  fetch("/feed/me", init).then(res => {
    if (res.redirected) window.location = res.url;
    else throw new Error('Failed to get feed')
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


export async function isSubscribed(slug) {
  const response = await api.subscription.isSubscribed(slug, getToken()); 
  return response.subscribed;
}

export async function subscribe(slug) {
  return await api.subscription.subscribe(slug, getToken());
}

export async function unsubscribe(slug) {
  return await api.subscription.unsubscribe(slug, getToken());
}
