import axios from 'axios'

const instance = axios.create({
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken'
})

export default instance