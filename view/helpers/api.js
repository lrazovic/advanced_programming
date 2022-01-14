import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:3000/api/'

export async function post(_this, url, payload, successCallback, errorCallback) {
  const headers = ''

  try {
    const response = await axios({
      method: 'POST',
      url: url,
      data: payload,
      headers: headers
    })
    successCallback(response)
  } catch (error) {
    if (!error.status) { console.log('network error')} 
    console.log(error.response)
    if (errorCallback) { errorCallback(error)} 
  }
}

export async function get(_this, url, payload, successCallback, errorCallback) {
  const headers = ''

  try {
    const response = await axios({
      method: 'GET',
      url: url,
      params: payload.params,
      headers: headers
    })
    successCallback(response)
  } catch (error) {
    if (errorCallback) { errorCallback(error)} 
  }
}

export async function del(_this, url, payload, successCallback, errorCallback) {
  const headers = ''

  try {
    const response = await axios({
      method: 'DELETE',
      url: url,
      headers: headers,
      payload: payload
    })
    successCallback(response)
  } catch (error) {
    if (errorCallback) { errorCallback(error)} 
  }
}
