<template>
  <div class="video-card" @click="$emit('open-analysis', post)">
    <div class="card-thumb" :style="thumbBg">
      <img
        v-if="!imgError"
        :src="thumbUrl"
        :alt="post.title || 'video'"
        loading="eager"
        @error="imgError = true"
      />
      <div class="thumb-overlay">
        <div class="thumb-top">
          <div class="thumb-badges">
            <span class="badge">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="4" stroke="#fff" stroke-width="2"/><circle cx="8.5" cy="8.5" r="1.5" fill="#fff"/><path d="M12 3v18M3 12h18" stroke="#fff" stroke-width="2"/></svg>
              Reels
            </span>
            <span class="badge">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 2C9 6 6.5 8.5 6.5 12A5.5 5.5 0 0 0 17.5 12C17.5 8.5 15 6 12 2z" fill="#fff"/></svg>
              X10
            </span>
          </div>
          <div class="thumb-actions">
            <button
              class="action-btn like-btn"
              :class="{ liked: liked, 'is-animating': likeAnimating }"
              @click.stop="toggleLike"
              aria-label="like"
            >
              <svg class="heart-icon" width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" stroke-width="1.8"/></svg>
            </button>
            <button class="action-btn" @click.stop aria-label="open">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" stroke="#fff" stroke-width="2"/><polyline points="15 3 21 3 21 9" stroke="#fff" stroke-width="2"/><line x1="10" y1="14" x2="21" y2="3" stroke="#fff" stroke-width="2"/></svg>
            </button>
          </div>
        </div>

        <div class="overlay-stats">
          <span class="stat-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="#fff" stroke-width="2"/><circle cx="12" cy="12" r="3" stroke="#fff" stroke-width="2"/></svg>
            <span>{{ fmtK(post.views_count) }}</span>
          </span>
          <span class="stat-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" stroke="#fff" stroke-width="2"/></svg>
            <span>{{ fmtK(post.likes_count) }}</span>
          </span>
          <span class="stat-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="#fff" stroke-width="2"/></svg>
            <span>{{ fmtK(post.comments_count) }}</span>
          </span>
          <span class="stat-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M22 2L11 13" stroke="#fff" stroke-width="2"/><polygon points="22 2 15 22 11 13 2 9 22 2" fill="#fff"/></svg>
            <span>{{ fmtK(post.shares_count) }}</span>
          </span>
        </div>
      </div>
    </div>

    <div class="card-body">
      <div class="blogger-row top">
        <div class="avatar" :style="avatarStyle">
          <img :src="avatarUrl" alt="" loading="eager" @error="avatarError = true" v-if="!avatarError" />
          <span v-else>{{ handle[1]?.toUpperCase() }}</span>
        </div>
        <div class="blogger-meta">
          <span class="username">{{ handle }}</span>
          <span class="subs">{{ fmtK(post.views_count) }}</span>
        </div>
        <button class="settings-btn" @click.stop aria-label="settings">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z" stroke="#333CD3" stroke-width="2"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.65 1.65 0 0 0 15 19.4a1.65 1.65 0 0 0-1 .6 1.65 1.65 0 0 0-.33 1V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-.33-1 1.65 1.65 0 0 0-1-.6 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-.6-1 1.65 1.65 0 0 0-1-.33H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1-.33 1.65 1.65 0 0 0 .6-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6h.01a1.65 1.65 0 0 0 1-.6 1.65 1.65 0 0 0 .33-1V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 .33 1 1.65 1.65 0 0 0 1 .6h.01a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9c.16.33.24.69.24 1.06s-.08.73-.24 1.06z" stroke="#333CD3" stroke-width="1.4"/></svg>
        </button>
      </div>
      <p class="description">{{ post.title || post.text }}</p>
      <span class="more-link">Еще</span>
      <span class="date">{{ fmtDate(post.created_at) }}</span>
      <button class="btn-analysis" @click.stop="$emit('open-analysis', post)">Анализ</button>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'

const props = defineProps({
  post: { type: Object, required: true },
  liked: { type: Boolean, default: false },
})
const emit = defineEmits(['open-analysis', 'toggle-like'])
const likeAnimating = ref(false)
const imgError = ref(false)
const avatarError = ref(false)
let likeAnimationTimer = null

const HANDLES = ['@blogerich', '@digital_mk', '@trendsetter', '@viral_pro', '@content_lab']

const GRADIENTS = [
  'linear-gradient(160deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(160deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(160deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(160deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(160deg, #fa709a 0%, #fee140 100%)',
  'linear-gradient(160deg, #a18cd1 0%, #fbc2eb 100%)',
  'linear-gradient(160deg, #fccb90 0%, #d57eeb 100%)',
  'linear-gradient(160deg, #e0c3fc 0%, #8ec5fc 100%)',
]

const id        = computed(() => props.post.id || 1)
const thumbUrl  = computed(() => `https://picsum.photos/seed/${id.value * 7}/254/400`)
const avatarUrl = computed(() => `https://picsum.photos/seed/${id.value * 13}/40/40`)
const thumbBg   = computed(() => ({
  background: GRADIENTS[id.value % GRADIENTS.length],
}))
const avatarStyle = computed(() => ({
  background: GRADIENTS[(id.value * 3 + 2) % GRADIENTS.length],
}))
const handle   = computed(() => HANDLES[id.value % HANDLES.length])

function toggleLike() {
  emit('toggle-like', props.post.id)
  likeAnimating.value = false
  requestAnimationFrame(() => {
    likeAnimating.value = true
    clearTimeout(likeAnimationTimer)
    likeAnimationTimer = setTimeout(() => {
      likeAnimating.value = false
    }, 450)
  })
}

function fmtK(n) {
  if (!n) return '0'
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return Math.round(n / 1000) + 'k'
  return String(n)
}

function fmtDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}

onBeforeUnmount(() => {
  clearTimeout(likeAnimationTimer)
})
</script>

<style scoped>
.video-card {
  width: 100%;
  min-width: 0;
  padding: 4px 4px 8px;
  background: #FFFFFF;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  transition: box-shadow 0.2s ease;
  box-sizing: border-box;
}
.video-card:hover {
  box-shadow: 0 8px 24px rgba(14, 29, 57, 0.14);
}

.card-thumb {
  position: relative;
  width: 100%;
  aspect-ratio: 9 / 14;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: 12px;
}
.card-thumb img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.thumb-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.08) 0%, rgba(0,0,0,0.45) 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 12px;
}

.thumb-top {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.thumb-badges {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  width: fit-content;
  height: 28px;
  padding: 4px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  border-radius: 6px;
  font-size: 12px;
  line-height: 14px;
  font-weight: 500;
  color: #fff;
}

.thumb-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.15s ease;
}
.action-btn:active { transform: scale(0.92); }

.heart-icon {
  transform-origin: center;
}

.heart-icon path {
  stroke: #fff;
  fill: transparent;
  transition: fill 0.2s ease, stroke 0.2s ease;
}

.like-btn.liked .heart-icon path {
  stroke: #FF5D7B;
  fill: #FF5D7B;
}

.like-btn.is-animating .heart-icon {
  animation: heart-bounce-spin 0.45s ease;
}

@keyframes heart-bounce-spin {
  0% { transform: scale(1) rotate(0deg); }
  20% { transform: scale(0.86) rotate(-12deg); }
  44% { transform: scale(0.62) rotate(220deg); }
  70% { transform: scale(1.14) rotate(360deg); }
  100% { transform: scale(1) rotate(360deg); }
}

.overlay-stats {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 6px;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  border-radius: 10px;
  box-sizing: border-box;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  width: 55.5px;
  font-size: 12px;
  line-height: 14px;
  color: #fff;
  font-weight: 500;
}

.card-body {
  width: 100%;
  padding: 4px 4px 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
  box-sizing: border-box;
}
.blogger-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.blogger-row.top {
  width: 100%;
  min-height: 40px;
  padding: 4px 0;
  justify-content: space-between;
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex-shrink: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  font-weight: 700;
  color: #fff;
}
.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.blogger-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 4px;
  flex: 1;
}

.username {
  font-size: 14px;
  line-height: 21px;
  font-weight: 600;
  color: #2B31B3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.subs {
  font-size: 12px;
  line-height: 16px;
  color: #4E616B;
  font-weight: 500;
}

.settings-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
}

.description {
  font-size: 11px;
  line-height: 14px;
  letter-spacing: 0.3px;
  color: #4E616B;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin: 0;
  width: 100%;
}

.more-link {
  font-size: 12px;
  line-height: 16px;
  color: #171C1F;
  font-weight: 600;
}
.date {
  font-size: 12px;
  line-height: 14px;
  color: #A0ADB4;
}
.btn-analysis {
  width: 100%;
  height: 40px;
  padding: 12px;
  background: #2B31B3;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 12px;
  line-height: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s;
}
.btn-analysis:hover { opacity: 0.85; }
</style>
