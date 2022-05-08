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

class API {
  static URL = '/api/v1'
  
  constructor() {
    this.auth = new AuthAPI(API.URL);
  }
}

export const api = new API();
