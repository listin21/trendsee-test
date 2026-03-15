<template>
  <div class="video-card" @click="$emit('click', post)">
    <!-- Thumbnail container -->
    <div class="thumb" :style="{ backgroundImage: `url(${thumbUrl})` }">
      <!-- Header: badges left, action buttons right -->
      <div class="thumb-header">
        <div class="badge-list">
          <div class="badge-pill">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="white"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg>
            <span>Reels</span>
          </div>
          <div v-if="isHot" class="badge-pill badge-hot">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="white"><path d="M13.5 0.67s.74 2.65.74 4.8c0 2.06-1.35 3.73-3.41 3.73-2.07 0-3.63-1.67-3.63-3.73l.03-.36C5.21 7.51 4 10.62 4 14c0 4.42 3.58 8 8 8s8-3.58 8-8C20 8.61 17.41 3.8 13.5 0.67z"/></svg>
            <span>X10</span>
          </div>
        </div>
        <div class="actions">
          <button
            class="action-btn heart-btn"
            :class="[{ liked: liked }, animClass]"
            @click.stop="toggleLike"
            aria-label="Сохранить"
          >
            <svg class="heart-icon" width="20" height="20" viewBox="0 0 24 24"
              :fill="liked ? '#FF4E7B' : 'none'"
              :stroke="liked ? '#FF4E7B' : 'white'"
              stroke-width="1.5">
              <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
            </svg>
          </button>
          <button class="action-btn" @click.stop aria-label="Открыть">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          </button>
        </div>
      </div>

      <!-- Stats bar at bottom of thumbnail -->
      <div class="stats-bar">
        <div class="stat-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3" fill="white"/></svg>
          <span>{{ views }}</span>
        </div>
        <div class="stat-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>
          <span>{{ likes }}</span>
        </div>
        <div class="stat-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
          <span>{{ comments }}</span>
        </div>
        <div class="stat-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2" fill="white" stroke="none"/></svg>
          <span>{{ shares }}</span>
        </div>
      </div>
    </div>

    <!-- Info section below thumbnail -->
    <div class="info">
      <!-- Blogger Card -->
      <div class="blogger-card">
        <div class="blogger">
          <img :src="avatarUrl" class="avatar" alt="" loading="lazy" />
          <div class="blogger-meta">
            <span class="blogger-name">@{{ authorHandle }}</span>
            <span class="blogger-subs">{{ subsCount }}</span>
          </div>
        </div>
        <button class="icon-action" @click.stop aria-label="Настройки">
          <!-- eye + plus icon like Figma -->
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="#4E616B" stroke-width="1.5"/>
            <circle cx="12" cy="12" r="3" stroke="#4E616B" stroke-width="1.5"/>
            <line x1="19" y1="5" x2="19" y2="11" stroke="#4E616B" stroke-width="1.5" stroke-linecap="round"/>
            <line x1="16" y1="8" x2="22" y2="8" stroke="#4E616B" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
      </div>

      <!-- Description -->
      <h4 class="post-title">{{ post.title || 'Без названия' }}</h4>
      <p class="description">{{ previewText }}</p>

      <!-- Date -->
      <span class="date">{{ formattedDate }}</span>

      <!-- Analyse button -->
      <button class="btn-analyse" @click.stop="$emit('click', post)">Анализ</button>
    </div>
  </div>
</template>

<script>
function seededRand(seed, min, max) {
  const s = ((seed * 9301 + 49297) % 233280) / 233280
  return min + Math.floor(s * (max - min))
}
function fmtK(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return Math.round(n / 1000) + 'k'
  return String(n)
}

export default {
  name: 'PostCard',
  props: { post: { type: Object, required: true } },
  emits: ['click'],
  data() {
    return {
      liked: false,
      heartAnimating: false,
      animClass: '',
    }
  },
  methods: {
    async toggleLike() {
      if (this.heartAnimating) return
      this.heartAnimating = true

      // Determine animation direction before toggling
      const isUnliking = this.liked
      const duration = isUnliking ? 350 : 500

      // Force remove class first so re-adding it triggers animation again
      this.animClass = ''
      await this.$nextTick()
      this.animClass = isUnliking ? 'animating-unlike' : 'animating-like'

      setTimeout(() => {
        this.liked = !this.liked
        this.animClass = ''
        this.heartAnimating = false
      }, duration)
    },
  },
  computed: {
    thumbUrl() {
      return `https://picsum.photos/seed/${(this.post.id || 1) * 7}/400/400`
    },
    avatarUrl() {
      return `https://picsum.photos/seed/${(this.post.id || 1) * 13}/80/80`
    },
    isHot() {
      return Date.now() - new Date(this.post.created_at).getTime() < 1000 * 60 * 10
    },
    authorHandle() {
      const handles = ['blogerich', 'digital_mk', 'trendsetter', 'viral_pro', 'content_lab']
      return handles[(this.post.id || 0) % handles.length]
    },
    subsCount() {
      return fmtK(seededRand((this.post.id || 1) * 17, 10000, 900000))
    },
    previewText() {
      const max = 60
      return this.post.text.length > max ? this.post.text.slice(0, max) : this.post.text
    },
    formattedDate() {
      return new Date(this.post.created_at).toLocaleDateString('ru-RU', {
        day: '2-digit', month: '2-digit', year: 'numeric'
      }).replace(/\//g, '.')
    },
    views()    { return fmtK(seededRand((this.post.id || 1) * 3,  800,   150000)) },
    likes()    { return fmtK(seededRand((this.post.id || 1) * 7,  500,   90000)) },
    comments() { return fmtK(seededRand((this.post.id || 1) * 11, 100,   20000)) },
    shares()   { return String(seededRand((this.post.id || 1) * 5, 50, 1000)) },
    er()       { return (seededRand((this.post.id || 1) * 19, 10, 150) / 10).toFixed(1) + '%' },
  }
}
</script>

<style scoped>
.video-card {
  width: 262px;
  min-width: 220px;
  max-width: 262px;
  height: 576px;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 4px 4px 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  transition: box-shadow 0.2s;
  flex-shrink: 0;
  font-family: 'Inter', sans-serif;
}
.video-card:hover {
  box-shadow: 0 6px 20px rgba(43,49,179,0.15);
}

/* Thumbnail */
.thumb {
  width: 254px;
  height: 400px;
  border-radius: 16px;
  background-size: cover;
  background-position: center;
  background-color: #1a1a2e;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 12px;
  flex-shrink: 0;
}

.thumb-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.badge-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(8px);
  border-radius: 8px;
  padding: 4px;
  color: white;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.4px;
}

.badge-hot {
  background: rgba(239,68,68,0.7);
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Action buttons in thumb header */
.action-btn {
  width: 36px;
  height: 36px;
  background: rgba(0,0,0,0.4);
  border: none;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 8px;
}

/* Stats bar */
.stats-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 230px;
  height: 55px;
  background: rgba(0,0,0,0.3);
  backdrop-filter: blur(4px);
  border-radius: 12px;
  padding: 8px 4px;
  margin: 0 auto;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.4px;
  line-height: 14px;
}

/* Info section — 254×160px, padding: 0 4px, gap: 4px */
.info {
  width: 254px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0 4px;
  gap: 4px;
  flex-shrink: 0;
}

/* Blogger Card — padding: 4px 0, gap: 8px */
.blogger-card {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
  width: 246px;
  min-height: 49px;
}

.blogger {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 128px;
  object-fit: cover;
  flex-shrink: 0;
}

.blogger-meta {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 4px;
}

.blogger-name {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.1px;
  color: #2B31B3;
}

.blogger-subs {
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
  color: #4E616B;
}

/* Description */
.description {
  width: 246px;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 12px;
  line-height: 14px;
  letter-spacing: 0.4px;
  color: #4E616B;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  margin: 0;
}

.post-title {
  width: 246px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.1px;
  color: #171C1F;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.icon-action {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* Date — 246×15px */
.date {
  width: 246px;
  height: 15px;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 12px;
  line-height: 14px;
  letter-spacing: 0.4px;
  color: #A0ADB4;
  display: flex;
  align-items: flex-end;
}

/* Analyse button — 246×40px */
.btn-analyse {
  width: 246px;
  height: 40px;
  background: #2B31B3;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 12px;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 600;
  line-height: 16px;
  letter-spacing: 0.4px;
  cursor: pointer;
  transition: background 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-analyse:hover { background: #2028A0; }

/* Heart button animation */
@keyframes heart-like {
  0%   { transform: rotate(0deg)   scale(1); }
  25%  { transform: rotate(20deg)  scale(0.85); }
  50%  { transform: rotate(-15deg) scale(0.7); }
  75%  { transform: rotate(8deg)   scale(0.9); }
  100% { transform: rotate(0deg)   scale(1); }
}

@keyframes heart-unlike {
  0%   { transform: scale(1); }
  30%  { transform: scale(0.65); }
  60%  { transform: scale(0.8); }
  100% { transform: scale(1); }
}

.heart-btn {
  width: 36px;
  height: 36px;
  padding: 8px;
  border-radius: 12px;
  gap: 8px;
  opacity: 1;
  transition: background 0.2s;
}

.heart-btn.animating-like {
  animation: heart-like 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

.heart-btn.animating-unlike {
  animation: heart-unlike 0.35s ease-in-out both;
}

.heart-btn.liked {
  background: rgba(255, 78, 123, 0.25);
}
</style>
