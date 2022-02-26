import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:3000/'

export async function post(_this, url, payload, successCallback, errorCallback) {
  let headers = _this.$auth.getToken() ? { 'Authorization': `Bearer ${_this.$auth.getToken()}` } : '';

  try {
    const response = await axios({
      method: 'POST',
      url: url,
      data: payload,
      headers: headers
    })
    successCallback(response)
  } catch (error) {
    if (!error.status) { console.log('network error') }
    if (errorCallback) { errorCallback(error) }
  }
}

export async function put(_this, url, payload, successCallback, errorCallback) {
  let headers = _this.$auth.getToken() ? { 'Authorization': `Bearer ${_this.$auth.getToken()}` } : '';

  try {
    const response = await axios({
      method: 'PUT',
      url: url,
      data: payload,
      headers: headers
    })
    successCallback(response)
  } catch (error) {
    if (!error.status) { console.log('network error') }
    if (errorCallback) { errorCallback(error) }
  }
}

export async function get(_this, url, payload, successCallback, errorCallback) {
  let headers = _this.$auth.getToken() ? { 'Authorization': `Bearer ${_this.$auth.getToken()}` } : '';

  try {
    const response = await axios({
      method: 'GET',
      url: url,
      params: payload.params,
      headers: headers
    })
    successCallback(response)
  } catch (error) {
    if (errorCallback) { errorCallback(error) }
  }
}

export async function del(_this, url, payload, successCallback, errorCallback) {
  let headers = _this.$auth.getToken() ? { 'Authorization': `Bearer ${_this.$auth.getToken()}` } : '';

  try {
    const response = await axios({
      method: 'DELETE',
      url: url,
      headers: headers,
      payload: payload
    })
    successCallback(response)
  } catch (error) {
    if (errorCallback) { errorCallback(error) }
  }
}
