import axios from 'axios'
import { mockPosts } from './mockData'

const API_BASE_URL = 'http://localhost:8000'
const USE_MOCK_DATA = false // Используем реальный backend по умолчанию

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const getPosts = async (page = 1, limit = 10) => {
  if (USE_MOCK_DATA) {
    await new Promise(resolve => setTimeout(resolve, 500))
    const offset = (page - 1) * limit
    return mockPosts.slice(offset, offset + limit)
  }

  const offset = (page - 1) * limit
  const response = await api.get('/posts', {
    params: { limit, offset }
  })
  return response.data
}

export const getPost = async (postId) => {
  const response = await api.get(`/posts/${postId}`)
  return response.data
}

export const createPost = async (postData, token) => {
  const response = await api.post('/posts', postData, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  return response.data
}

export const createUser = async (name) => {
  const response = await api.post('/users', { name })
  return response.data
}

export default api
