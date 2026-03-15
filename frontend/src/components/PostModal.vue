<template>
  <Transition name="modal">
    <div v-if="show" class="overlay" @click.self="$emit('close')" role="dialog" aria-modal="true" aria-label="Публикация">
      <div class="modal">
        <div class="modal-header" :style="{ background: thumbGradient }">
          <button class="close-btn" @click="$emit('close')" aria-label="Закрыть">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
          <div class="play-btn" aria-hidden="true">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
          </div>
        </div>

        <div class="modal-body">
          <div class="modal-tags">
            <span class="tag" v-for="tag in tags" :key="tag">{{ tag }}</span>
          </div>

          <h2 class="modal-title">{{ post.title }}</h2>

          <div class="modal-meta">
            <div class="meta-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
              <span>User #{{ post.user_id }}</span>
            </div>
            <div class="meta-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              <span>{{ formattedCreatedAt }}</span>
            </div>
            <div class="meta-item" v-if="post.updated_at">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              <span>Изменено: {{ formattedUpdatedAt }}</span>
            </div>
          </div>

          <div class="modal-stats">
            <div class="stat-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              <span class="stat-val">{{ post.views || '4 821' }}</span>
              <span class="stat-label">просмотров</span>
            </div>
            <div class="stat-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>
              <span class="stat-val">{{ post.likes || '142' }}</span>
              <span class="stat-label">лайков</span>
            </div>
            <div class="stat-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
              <span class="stat-val">{{ post.comments || '23' }}</span>
              <span class="stat-label">комментариев</span>
            </div>
            <div class="stat-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
              <span class="stat-val">{{ post.reposts || '8' }}</span>
              <span class="stat-label">репостов</span>
            </div>
          </div>

          <div class="divider"></div>

          <p class="modal-text">{{ post.text }}</p>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
const GRADIENTS = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
  'linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)',
  'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
  'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)',
]
const ALL_TAGS = ['Видео', 'Контент', 'Тренды', 'Маркетинг', 'SMM', 'Аналитика', 'Reels', 'Shorts']

export default {
  name: 'PostModal',
  props: {
    show: { type: Boolean, required: true },
    post: { type: Object, required: true }
  },
  emits: ['close'],
  computed: {
    thumbGradient() {
      return GRADIENTS[(this.post.id || 0) % GRADIENTS.length]
    },
    tags() {
      const idx = (this.post.id || 0) % ALL_TAGS.length
      return [ALL_TAGS[idx], ALL_TAGS[(idx + 2) % ALL_TAGS.length]]
    },
    formattedCreatedAt() {
      if (!this.post.created_at) return ''
      return new Date(this.post.created_at).toLocaleString('ru-RU', {
        day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit'
      })
    },
    formattedUpdatedAt() {
      if (!this.post.updated_at) return ''
      return new Date(this.post.updated_at).toLocaleString('ru-RU', {
        day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
/* ── Overlay ── */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

/* ── Modal panel ── */
.modal {
  background: var(--surface);
  border-radius: 16px;
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.22);
}

.modal-header {
  height: 200px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px 16px 0 0;
  flex-shrink: 0;
}

.close-btn {
  position: absolute;
  top: 14px;
  right: 14px;
  width: 34px;
  height: 34px;
  background: rgba(0, 0, 0, 0.35);
  border: none;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s ease;
}
.close-btn:hover { background: rgba(0, 0, 0, 0.55); }
.close-btn:focus-visible { outline: 2px solid white; outline-offset: 2px; }

.play-btn {
  width: 60px;
  height: 60px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body { padding: 24px; }

.modal-tags {
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.tag {
  font-size: 11px;
  font-weight: 600;
  color: var(--primary);
  background: var(--primary-light);
  padding: 3px 10px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 14px;
  line-height: 1.35;
}

.modal-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 20px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12.5px;
  color: var(--text-2);
}

.modal-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.stat-box {
  background: var(--surface-2);
  border-radius: var(--radius-sm);
  padding: 12px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: var(--text-2);
}

.stat-val {
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
}

.stat-label {
  font-size: 10.5px;
  color: var(--text-3);
  text-align: center;
}

.divider {
  height: 1px;
  background: var(--border);
  margin-bottom: 20px;
}

.modal-text {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-2);
  white-space: pre-wrap;
}

/* ── Transition: overlay + modal animate together ── */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Modal panel slides up on enter, down on leave */
.modal-enter-active .modal {
  transition: transform 0.25s cubic-bezier(0.34, 1.4, 0.64, 1), opacity 0.2s ease;
}
.modal-leave-active .modal {
  transition: transform 0.18s ease-in, opacity 0.18s ease;
}
.modal-enter-from .modal {
  transform: translateY(24px) scale(0.97);
  opacity: 0;
}
.modal-leave-to .modal {
  transform: translateY(12px) scale(0.98);
  opacity: 0;
}

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  .modal-enter-active,
  .modal-leave-active,
  .modal-enter-active .modal,
  .modal-leave-active .modal {
    transition: opacity 0.15s ease;
  }
  .modal-enter-from .modal,
  .modal-leave-to .modal {
    transform: none;
  }
}
</style>
