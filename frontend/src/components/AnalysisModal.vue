<template>
  <Transition name="modal">
    <div v-if="show" class="overlay" @click.self="$emit('close')" role="dialog" aria-modal="true" aria-label="Анализ видео">
      <div class="modal">

        <!-- LEFT COLUMN -->
        <div class="col-left">
          <div class="preview-card">
            <div class="preview-thumb" :style="thumbBg">
              <img
                v-if="!imgError"
                :src="thumbUrl"
                :alt="post.title || 'video'"
                loading="eager"
                @error="imgError = true"
              />
              <div class="preview-overlay">
                <div class="top-badges">
                  <span class="reels-badge">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="4" stroke="currentColor" stroke-width="2"/><path d="M3 9h18" stroke="currentColor" stroke-width="2"/><path d="M8 3l3 6M14 3l3 6" stroke="currentColor" stroke-width="2"/></svg>
                    Reels
                  </span>
                  <span class="x10-badge">
                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none"><path d="M12 2C9 6 6.5 8.5 6.5 12A5.5 5.5 0 0 0 17.5 12C17.5 8.5 15 6 12 2z" fill="currentColor"/></svg>
                    X10
                  </span>
                </div>
                <button class="play-btn" type="button" aria-label="Play preview">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M8 5v14l11-7-11-7z" fill="#4E616B"/></svg>
                </button>
                <div class="overlay-stats">
                  <span class="stat"><svg width="11" height="11" viewBox="0 0 24 24" fill="none"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="#fff" stroke-width="2"/><circle cx="12" cy="12" r="3" stroke="#fff" stroke-width="2"/></svg>{{ fmtK(post.views_count) }}</span>
                  <span class="stat"><svg width="11" height="11" viewBox="0 0 24 24" fill="none"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" stroke="#fff" stroke-width="2"/></svg>{{ fmtK(post.likes_count) }}</span>
                  <span class="stat"><svg width="11" height="11" viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="#fff" stroke-width="2"/></svg>{{ fmtK(post.comments_count) }}</span>
                  <span class="stat"><svg width="11" height="11" viewBox="0 0 24 24" fill="none"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" stroke="#fff" stroke-width="2"/><polyline points="16 6 12 2 8 6" stroke="#fff" stroke-width="2"/><line x1="12" y1="2" x2="12" y2="15" stroke="#fff" stroke-width="2"/></svg>{{ fmtK(post.shares_count) }}</span>
                </div>
              </div>
            </div>
            <div class="preview-info">
              <div class="blogger-row">
                <div class="avatar" :style="avatarStyle">
                  <img v-if="!avatarError" :src="avatarUrl" alt="" loading="eager" @error="avatarError = true" />
                  <span v-else>{{ handle[1]?.toUpperCase() }}</span>
                </div>
                <div>
                  <div class="username">{{ handle }}</div>
                  <div class="post-date">{{ fmtDate(post.created_at) }}</div>
                </div>
              </div>
              <p class="desc">{{ post.title || post.text }}</p>
            </div>
          </div>

          <!-- Stats block -->
          <div class="stats-block">
            <div class="stat-row"><span class="stat-label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/></svg>Просмотры</span><span class="stat-val">{{ fmtM(post.views_count) }}</span></div>
            <div class="stat-row"><span class="stat-label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" stroke="currentColor" stroke-width="2"/></svg>Лайки</span><span class="stat-val">{{ fmtM(post.likes_count) }}</span></div>
            <div class="stat-row"><span class="stat-label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="2"/></svg>Комментарии</span><span class="stat-val">{{ fmtM(post.comments_count) }}</span></div>
            <div class="stat-row"><span class="stat-label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M22 2L11 13" stroke="currentColor" stroke-width="2"/><polygon points="22 2 15 22 11 13 2 9 22 2" fill="none" stroke="currentColor" stroke-width="2"/></svg>Репосты</span><span class="stat-val">{{ fmtM(post.shares_count) }}</span></div>
            <div class="stat-row"><span class="stat-label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 2v20M2 12h20" stroke="currentColor" stroke-width="2"/></svg>ER</span><span class="stat-val">{{ er }}%</span></div>
          </div>
        </div>

        <!-- RIGHT COLUMN -->
        <div class="col-right">
          <!-- Header -->
          <div class="right-header">
            <div>
              <p class="topic-label">Тема видео</p>
              <h2 class="topic-title">{{ post.title || post.text }}</h2>
              <div class="topic-meta">
                <span class="meta-pill">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12h2l2-6 4 12 2-6h4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  Tyga - Pop it off
                </span>
                <span class="meta-lang">
                  Язык:
                  <span class="lang-flag-icon" aria-hidden="true">
                    <svg width="18" height="14" viewBox="0 0 18 14" fill="none">
                      <rect width="18" height="14" rx="2" fill="#012169"/>
                      <path d="M0 1.5L6 6.2V0h6v6.2l6-4.7v2.4l-4.9 3.8H18v2.6h-4.9L18 12.1V14l-6-4.7V14H6V9.3L0 14v-1.9l4.9-3.8H0V5.7h4.9L0 1.9V1.5z" fill="#fff"/>
                      <path d="M0 2.3L4.3 5.7H3l-3-2.4V2.3zm18 0v1l-3 2.4h-1.3L18 2.3zM0 11.7l3-2.4h1.3L0 12.7v-1zM18 11.7v1l-4.3-3.4H15l3 2.4z" fill="#C8102E"/>
                      <path d="M7.2 0h3.6v5H18v4H10.8v5H7.2V9H0V5h7.2V0z" fill="#fff"/>
                      <path d="M7.8 0h2.4v5.6H18v2.8h-7.8V14H7.8V8.4H0V5.6h7.8V0z" fill="#C8102E"/>
                    </svg>
                  </span>
                  Английский
                </span>
              </div>
            </div>
            <button class="btn-close" @click="$emit('close')" aria-label="Закрыть">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6l12 12" stroke="#9898A6" stroke-width="2" stroke-linecap="round"/></svg>
            </button>
          </div>

          <!-- Tags -->
          <div class="tags-row">
            <span v-for="tag in tags" :key="tag.label" class="tag" :style="{ background: tag.bg, color: tag.color }">{{ tag.label }}</span>
          </div>

          <div class="section">
            <div class="section-head">
              <span class="section-title">Данные публикации</span>
            </div>
            <div class="meta-grid">
              <div class="meta-item"><span class="meta-key">id</span><span class="meta-val">{{ post.id ?? '—' }}</span></div>
              <div class="meta-item"><span class="meta-key">user_id</span><span class="meta-val">{{ post.user_id ?? '—' }}</span></div>
              <div class="meta-item"><span class="meta-key">created_at</span><span class="meta-val">{{ fmtDateTime(post.created_at) }}</span></div>
              <div class="meta-item"><span class="meta-key">updated_at</span><span class="meta-val">{{ fmtDateTime(post.updated_at) }}</span></div>
              <div class="meta-item full"><span class="meta-key">title</span><span class="meta-val">{{ post.title || '—' }}</span></div>
              <div class="meta-item full"><span class="meta-key">text</span><span class="meta-val">{{ post.text || '—' }}</span></div>
            </div>
          </div>

          <!-- Transcript -->
          <div class="section">
            <div class="section-head">
              <span class="section-title">Транскрипция</span>
              <button class="copy-btn" aria-label="Копировать">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9898A6" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
              </button>
            </div>
            <div class="content-block">{{ post.text || 'Транскрибация недоступна для данного видео.' }}</div>
          </div>

          <button class="btn-adapt">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" fill="white"/></svg>
            Адаптировать
          </button>

          <!-- Essence -->
          <div class="section">
            <div class="section-head">
              <span class="section-title">Суть</span>
            </div>
            <div class="content-block">{{ post.description || 'Краткое описание сути видео будет доступно после обработки.' }}</div>
          </div>

          <!-- Structure -->
          <div class="section">
            <div class="section-head"><span class="section-title">Структура</span></div>
            <div class="structure-steps">
              <div class="step" v-for="(step, i) in structureSteps" :key="i">
                <div class="step-track">
                  <div class="step-dot" :class="step.dotClass"></div>
                  <div class="step-line" v-if="i < structureSteps.length - 1"></div>
                </div>
                <div class="step-body">
                  <span class="step-time">{{ step.time }}</span>
                  <div class="step-content">
                    <span class="step-label">{{ step.label }}</span>
                    <span class="step-desc">{{ step.desc }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="section">
            <div class="section-head">
              <span class="section-title">Хук фраза</span>
              <button class="copy-btn" aria-label="Копировать">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9898A6" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
              </button>
            </div>
            <div class="content-block">Один из них — пустышка. Угадаешь какой?</div>
          </div>

          <div class="section">
            <div class="section-head">
              <span class="section-title">Визуальный хук</span>
              <button class="copy-btn" aria-label="Копировать">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9898A6" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
              </button>
            </div>
            <div class="content-block">Один из них — пустышка. Угадаешь какой?</div>
          </div>

          <div class="section">
            <div class="section-head">
              <span class="section-title">Текстовый хук</span>
              <button class="copy-btn" aria-label="Копировать">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9898A6" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
              </button>
            </div>
            <div class="content-block">Один из них — пустышка. Угадаешь какой?</div>
          </div>

          <div class="section">
            <div class="section-head"><span class="section-title">Рабочие приемы</span></div>
            <div class="content-block stack">
              <div v-for="(technique, idx) in techniques" :key="idx" class="stack-item">
                <div class="stack-title">{{ idx + 2 }}. {{ technique.title }}</div>
                <div class="stack-text">{{ technique.desc }}</div>
              </div>
            </div>
          </div>

          <div class="section">
            <div class="section-head"><span class="section-title">Воронка / Маркетинг</span></div>
            <div class="content-block stack">
              <div v-for="(funnel, idx) in funnelItems" :key="idx" class="stack-item">
                <div class="stack-title">{{ funnel.label }}</div>
                <div class="stack-text">{{ funnel.desc }}</div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  show: { type: Boolean, required: true },
  post: { type: Object, required: true }
})
defineEmits(['close'])

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
const imgError = ref(false)
const avatarError = ref(false)
const TAG_POOL = [
  { label: 'Туториал',           bg: '#D5D6F8', color: '#2B31B3' },
  { label: 'Энергичное видео',   bg: '#E1F7D8', color: '#1E6D00' },
  { label: 'Изи монтаж',         bg: '#FFF0CB', color: '#9E3F00' },
  { label: 'Трендовый звук',     bg: '#FFECF1', color: '#BF0031' },
  { label: 'Лид магнит',         bg: '#FFF0CB', color: '#9E3F00' },
  { label: 'Красота и здоровье', bg: '#D5D6F8', color: '#2B31B3' },
]

const id       = computed(() => props.post.id || 1)
const thumbUrl = computed(() => `https://picsum.photos/seed/${id.value * 7}/260/200`)
const avatarUrl = computed(() => `https://picsum.photos/seed/${id.value * 13}/32/32`)
const handle   = computed(() => HANDLES[id.value % HANDLES.length])
const thumbBg = computed(() => ({ background: GRADIENTS[id.value % GRADIENTS.length] }))
const avatarStyle = computed(() => ({ background: GRADIENTS[(id.value * 3 + 2) % GRADIENTS.length] }))
const er       = computed(() => {
  const v = props.post.views_count || 1
  const eng = (props.post.likes_count || 0) + (props.post.comments_count || 0)
  return ((eng / v) * 100).toFixed(1)
})
const tags = computed(() => {
  const idx = id.value % TAG_POOL.length
  return [TAG_POOL[idx], TAG_POOL[(idx+1)%TAG_POOL.length], TAG_POOL[(idx+2)%TAG_POOL.length], TAG_POOL[(idx+3)%TAG_POOL.length]]
})

const structureSteps = [
  { time: '0–5 сек',    label: 'Шок-сравнение', desc: 'Визуальный хук + текст на экране', dotClass: 'dot-dashed' },
  { time: '5–15 сек',   label: 'Сюжет',         desc: 'Показывает проблему → решение',    dotClass: 'dot-solid' },
  { time: '15–120 сек', label: 'Финал / CTA',    desc: 'Призыв к действию',               dotClass: 'dot-filled' },
]

const techniques = [
  { title: 'Суть видео', desc: 'Почему работает: объясняет выгоду простым языком и сразу попадает в боль аудитории.' },
  { title: 'Монтаж', desc: 'Почему работает: частые смены планов удерживают внимание и не дают зрителю заскучать.' },
  { title: 'Реплики', desc: 'Почему работает: разговорный стиль и короткие фразы усиливают доверие и читаемость.' },
]

const funnelItems = [
  { label: 'CTA голос/визуал', desc: 'Почему сработало: зритель узнает свой кейс и получает четкий следующий шаг.' },
  { label: 'Триггер', desc: 'Почему сработало: контраст до/после дает быстрый эмоциональный отклик.' },
  { label: 'Куда ведет', desc: 'Почему сработало: связка с профилем и комментариями повышает глубину просмотра.' },
  { label: 'Лид-магнит', desc: 'Почему сработало: обещание простой пользы снижает порог действия.' },
]

watch(id, () => {
  imgError.value = false
  avatarError.value = false
})

function fmtK(n) {
  if (!n) return '0'
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return Math.round(n / 1000) + 'k'
  return String(n)
}
function fmtM(n) {
  if (!n) return '0'
  if (n >= 1000000) return `${(n / 1000000).toFixed(1).replace('.', ',')} млн`
  if (n >= 1000) return `${Math.round(n / 1000)} тыс`
  return String(n)
}
function fmtDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}
function fmtDateTime(d) {
  if (!d) return '—'
  return new Date(d).toLocaleString('ru-RU')
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 1000;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 0;
}
.modal {
  background: #FFFFFF;
  border-radius: 24px 0 0 24px;
  width: 1020px;
  height: 100dvh;
  max-height: 100dvh;
  max-width: 100%;
  display: flex;
  overflow: hidden;
  box-shadow: 0 24px 80px rgba(14, 29, 57, 0.28);
  font-family: 'Inter', sans-serif;
}

/* LEFT */
.col-left {
  width: 258px;
  min-width: 258px;
  flex: 0 0 258px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-right: 1px solid #E6E8EA;
  padding: 24px 0 0;
  overflow-y: auto;
  min-height: 0;
  scrollbar-width: none;
}
.col-left::-webkit-scrollbar { display: none; }

.preview-card {
  background: #FFFFFF;
  border-radius: 0;
  overflow: visible;
  padding: 0 0 0 16px;
}
.preview-thumb {
  position: relative;
  width: 220px;
  height: 340px;
  border-radius: 16px;
  overflow: hidden;
}
.preview-thumb img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.preview-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.12) 0%, rgba(0,0,0,0.6) 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 12px;
}
.reels-badge {
  background: rgba(0,0,0,0.4);
  border-radius: 8px;
  padding: 3px 8px;
  font-size: 11px;
  font-weight: 600;
  color: #fff;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  width: fit-content;
  align-self: flex-start;
  line-height: 1.1;
}
.top-badges {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.x10-badge {
  align-self: flex-start;
  background: rgba(0,0,0,0.4);
  border-radius: 8px;
  padding: 3px 8px;
  font-size: 11px;
  font-weight: 600;
  color: #fff;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  width: fit-content;
  line-height: 1.1;
}
.play-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
}
.overlay-stats {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.stat {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  color: #fff;
  font-weight: 500;
}
.preview-info {
  padding: 8px 0 0;
}
.blogger-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
}
.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.username {
  font-size: 14px;
  line-height: 21px;
  font-weight: 600;
  color: #2B31B3;
}
.post-date {
  font-size: 12px;
  line-height: 14px;
  color: #A0ADB4;
}
.desc {
  font-size: 12px;
  color: #4E616B;
  line-height: 1.35;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.stats-block {
  padding: 0 16px 0 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #F4F5F6;
  border-radius: 12px;
  padding: 8px 12px;
}
.stat-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  line-height: 14px;
  color: #343A40;
}
.stat-val {
  font-size: 14px;
  line-height: 21px;
  font-weight: 500;
  color: #393C4C;
}

/* RIGHT */
.col-right {
  flex: 1;
  width: auto;
  padding: 24px 28px 24px 28px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-height: 0;
  scrollbar-width: none;
}
.col-right::-webkit-scrollbar { display: none; }

.right-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}
.topic-label {
  font-size: 14px;
  line-height: 21px;
  font-weight: 500;
  color: #4E616B;
  margin: 0 0 8px;
}
.topic-title {
  font-size: 24px;
  font-weight: 600;
  color: #000000;
  line-height: 1.18;
  margin: 0;
  max-width: 574px;
}
.topic-meta {
  margin-top: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.meta-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #F4F5F6;
  color: #5B6A73;
  border-radius: 10px;
  padding: 4px 8px;
  font-size: 14px;
}
.meta-lang {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #758892;
  font-size: 14px;
}
.lang-flag-icon {
  width: 18px;
  height: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 2px;
  overflow: hidden;
  flex-shrink: 0;
}
.btn-close {
  width: 40px;
  height: 40px;
  background: #F4F5F6;
  border: none;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
}

.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.tag {
  padding: 4px 12px;
  border-radius: 1000px;
  font-size: 14px;
  line-height: 21px;
  font-weight: 500;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.meta-grid {
  background: #F4F5F6;
  border-radius: 12px;
  padding: 12px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}
.meta-item {
  border-radius: 8px;
  border: 1px solid #E2E6EA;
  background: #FFFFFF;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.meta-item.full {
  grid-column: 1 / -1;
}
.meta-key {
  font-size: 11px;
  line-height: 14px;
  color: #83939C;
  font-weight: 600;
  text-transform: uppercase;
}
.meta-val {
  font-size: 13px;
  line-height: 18px;
  color: #2C3A43;
  word-break: break-word;
}
.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 0;
}
.section-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  color: #000000;
}
.copy-btn {
  background: #F4F5F6;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
}
.content-block {
  background: #F4F5F6;
  border-radius: 6px;
  padding: 16px;
  font-size: 14px;
  line-height: 21px;
  color: #4E616B;
}

.btn-adapt {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #2B31B3;
  color: #fff;
  font-size: 18px;
  line-height: 24px;
  font-weight: 600;
  padding: 8px 24px;
  height: 56px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  align-self: flex-start;
}

/* Structure timeline */
.structure-steps { display: flex; flex-direction: column; }
.step { display: flex; gap: 8px; }
.step-track { display: flex; flex-direction: column; align-items: center; width: 24px; flex-shrink: 0; }
.step-dot { width: 16px; height: 16px; border-radius: 50%; flex-shrink: 0; margin-top: 10px; }
.dot-dashed { background: transparent; border: 2px dashed #2B31B3; }
.dot-solid  { background: transparent; border: 2px solid #2B31B3; }
.dot-filled { background: #2B31B3; }
.step-line { width: 1px; flex: 1; background: #AEB1F2; min-height: 60px; }
.step-body { display: flex; gap: 8px; padding-bottom: 12px; flex: 1; }
.step-time {
  font-size: 12px;
  line-height: 14px;
  color: #4E616B;
  width: 96px;
  flex-shrink: 0;
  padding-top: 10px;
  text-align: right;
}
.step-content { display: flex; flex-direction: column; gap: 4px; padding-top: 8px; }
.step-label { font-size: 14px; line-height: 21px; font-weight: 600; color: #000; }
.step-desc  { font-size: 14px; line-height: 21px; color: #4E616B; max-width: 400px; }

.stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stack-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stack-title {
  font-size: 16px;
  line-height: 24px;
  font-weight: 600;
  color: #000;
}

.stack-text {
  font-size: 14px;
  line-height: 21px;
  color: #4E616B;
}

/* Transition */
.modal-enter-active { transition: opacity 0.2s ease; }
.modal-leave-active { transition: opacity 0.18s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .modal { transition: transform 0.2s ease-out; }
.modal-leave-active .modal { transition: transform 0.18s ease-in; }
.modal-enter-from .modal { transform: scale(0.96); }
.modal-leave-to .modal { transform: scale(0.97); }
</style>
