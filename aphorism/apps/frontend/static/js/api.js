"use strict";

const methods = {
  get: async function (endpoint, token = null) {
    const options = {
      method: 'GET',
      headers: {
        ...(token && `Authorization ${token}`)
      }
    }
    const response = await fetch(endpoint, options);
    const json = await response.json();
    if (!response.ok) throw new Error(json);
    return json;
  },
  post: async function (endpoint, body, token = null) {
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token && {'Authorization': `Bearer ${token}`})
      },
      body: JSON.stringify(body)
    }
    const response = await fetch(endpoint, options);
    const json = await response.json();
    if (!response.ok) throw new Error(json.message);
    return json;
  },
  put: async function (endpoint, token = null) {
    const options = {
      method: 'PUT',
      headers: {
        ...(token && {'Authorization': `Bearer ${token}`})
      }
    }
    const response = await fetch(endpoint, options);
    const json = await response.json();
    if (!response.ok) throw new Error(json);
    return json;
  },
  delete: async function (endpoint, token = null) {
    const options = {
      method: 'DELETE',
      headers: {
        ...(token && {'Authorization': `Bearer ${token}`})
      }
    }
    const response = await fetch(endpoint, options);
    const json = await response.json();
    if (!response.ok) throw new Error(json);
    return json;
  }
}


class AuthAPI {
  constructor(url) {
    this.baseUrl = url + '/auth';
  }

  async register(data) {
    return await methods.post(this.baseUrl + '/register', data);
  }
  
  async login(data) {
    return await methods.post(this.baseUrl + '/login', data)
  }
  
  async logout(token) {
    await methods.delete(this.baseUrl + '/logout');
  }
}

class SubscriptionApi {
  constructor(baseUrl) {
    this.url = baseUrl + '/subscription'
  }
  
  async isSubscribed(slug, token) {
    return await methods.get(this.url + `/${slug}`, token);
  }
  
  async subscribe(slug, token) {
    return await methods.post(this.url + `/${slug}`, token);
  }
  
  async unsubscribe(slug, token) {
    return await methods.delete(this.url + `/${slug}`, token);
  }
  
}

class UserApi {
  constructor(baseUrl) {
    this.url = baseUrl + '/user';
  }
}

class API {
  static URL = '/api/v1'
  
  constructor() {
    this.auth = new AuthAPI(API.URL);
    this.subscription = new SubscriptionApi(API.URL);
    this.user = new UserApi(API.URL);
  }
}

export const api = new API();
