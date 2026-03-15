<template>
  <aside class="sidebar" :class="{ 'is-collapsed': collapsed, 'is-mobile-hidden': forceCollapsed }">
    <div class="sidebar-main">
      <div class="brand-row">
        <div class="brand-logo" :title="isCollapsed ? 'trendsee' : undefined">
          <svg width="26" height="20" viewBox="0 0 26 20" fill="none" aria-hidden="true">
            <path d="M1 10C3.5 5.2 7.8 2.5 13 2.5c5.2 0 9.5 2.7 12 7.5-2.5 4.8-6.8 7.5-12 7.5C7.8 17.5 3.5 14.8 1 10z" fill="#171C1F"/>
            <circle cx="13" cy="10" r="4.5" fill="#F4F5F6"/>
            <circle cx="13" cy="10" r="2.4" fill="#171C1F"/>
          </svg>
        </div>
        <template v-if="!collapsed">
          <span class="brand-name">trendsee</span>
          <span class="beta-badge">Beta</span>
        </template>
        <button class="collapse-toggle" type="button" @click="toggleSidebar" :aria-label="isCollapsed ? 'Развернуть сайдбар' : 'Свернуть сайдбар'">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <path
              :d="collapsed ? 'M9 6l6 6-6 6' : 'M15 6l-6 6 6 6'"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
      </div>

      <section class="menu-group" v-for="group in groups" :key="group.title">
        <h4 v-if="!collapsed" class="group-title">{{ group.title }}</h4>
        <nav class="group-list">
          <RouterLink
            v-for="item in group.items"
            :key="item.to"
            :to="item.to"
            class="nav-item"
            :class="{ active: isActive(item.to) }"
          >
            <span
              class="nav-icon"
              aria-hidden="true"
              :style="{ color: isActive(item.to) ? '#2B31B3' : item.color || '#667A85' }"
            >
              <svg v-if="item.icon === 'home'" width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M4 11.4L12 5l8 6.4M6.6 9.4V19h10.8V9.4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <svg v-else-if="item.icon === 'video'" width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="4" y="6" width="16" height="12" rx="2" stroke="currentColor" stroke-width="2"/><path d="M10 10l4 2-4 2v-4z" fill="currentColor"/></svg>
              <svg v-else-if="item.icon === 'spy'" width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 4l2 3h3l-2 2 1 4-4-2-4 2 1-4-2-2h3l2-3zM7 18h10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <svg v-else-if="item.icon === 'radar'" width="22" height="22" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="7" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/><path d="M12 12l6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              <svg v-else-if="item.icon === 'cross'" width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M7 7h4v4H7zM13 13h4v4h-4zM9 9l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <svg v-else-if="item.icon === 'bot'" width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="5" y="7" width="14" height="11" rx="3" stroke="currentColor" stroke-width="2"/><path d="M12 4v3M9 12h.01M15 12h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              <svg v-else-if="item.icon === 'spark'" width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M6 16l3-3M9 7l2 2M14 4l2 4M15 14l5-1M5 9l4-1M12 20l1-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M11 11l2 2-2 2-2-2z" stroke="currentColor" stroke-width="2"/></svg>
              <svg v-else-if="item.icon === 'carousel'" width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="4" y="7" width="16" height="11" rx="2" stroke="currentColor" stroke-width="2"/><path d="M4 11h16" stroke="currentColor" stroke-width="2"/></svg>
              <svg v-else-if="item.icon === 'link'" width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M10.5 13.5l3-3M8 16a4 4 0 010-5.7l2.3-2.3a4 4 0 115.7 5.7L15 15M16 8a4 4 0 015.7 0 4 4 0 010 5.7l-2.3 2.3a4 4 0 11-5.7-5.7L15 9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="6" y="4" width="12" height="16" rx="2" stroke="currentColor" stroke-width="2"/><path d="M9 8h6M9 12h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            </span>
            <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
            <span v-if="!collapsed && item.badge" class="item-badge">{{ item.badge }}</span>
          </RouterLink>
        </nav>
      </section>
    </div>

    <div class="sidebar-footer">
      <div v-if="!collapsed" class="tokens-card">
        <div class="tokens-row">
          <span class="tokens-label">Токены</span>
          <span class="tokens-value">1 245 / 4 497</span>
        </div>
        <div class="tokens-track">
          <div class="tokens-fill"></div>
        </div>
        <button class="plan-row" type="button" @click="isPlanExpanded = !isPlanExpanded">
          <span class="plan-name">Creative +</span>
          <span class="plan-arrow" :class="{ open: isPlanExpanded }">›</span>
        </button>
        <div v-if="isPlanExpanded" class="upgrade-box">
          <div class="upgrade-sub">Пробная версия</div>
          <button class="upgrade-btn" type="button">Улучшить подписку</button>
        </div>
      </div>
      <div class="profile-row" :class="{ compact: collapsed }">
        <div class="profile-avatar"></div>
        <div v-if="!collapsed" class="profile-body">
          <div class="profile-name">Александра</div>
          <div class="profile-phone">+7 (999) 999-99-99</div>
        </div>
      </div>
      <button v-if="!collapsed" class="lang-chip" type="button"><span class="flag-ru"></span>RU</button>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'Sidebar',
  props: {
    forceCollapsed: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['toggle'],
  data() {
    return {
      isCollapsed: false,
      isPlanExpanded: false,
      groups: [
        {
          title: 'Поиск контента',
          items: [
            { label: 'Главная', to: '/', icon: 'home', color: '#AE7D16' },
            { label: 'Видео', to: '/analysis', icon: 'video', color: '#2B31B3' },
            { label: 'Шпионаж', to: '/spy', icon: 'spy', color: '#6A45D4' },
            { label: 'Контент радар', to: '/radar', icon: 'radar', color: '#C0284D', badge: '712' },
          ],
        },
        {
          title: 'Работа с соцсетями',
          items: [
            { label: 'Кросс-постинг', to: '/cross-posting', icon: 'cross', color: '#C63F9A' },
            { label: 'Чат боты', to: '/bots', icon: 'bot', color: '#7B7C87' },
          ],
        },
        {
          title: 'Инструменты',
          items: [
            { label: 'ИИ-сценарий', to: '/script', icon: 'spark', color: '#0074AE' },
            { label: 'Карусели', to: '/carousels', icon: 'carousel', color: '#B56F2D' },
            { label: 'Анализ видео', to: '/analysis', icon: 'link', color: '#5C37D2' },
            { label: 'Анализ профиля', to: '/profile-analysis', icon: 'link', color: '#8E00CC' },
            { label: 'Черновик', to: '/draft', icon: 'draft', color: '#586572', badge: 'Скоро' },
          ],
        },
      ],
    }
  },
  computed: {
    collapsed() {
      return this.forceCollapsed || this.isCollapsed
    },
  },
  watch: {
    forceCollapsed(val) {
      if (val) this.isCollapsed = false
      this.setSidebarWidth()
    },
  },
  mounted() {
    this.setSidebarWidth()
  },
  beforeUnmount() {
    document.documentElement.style.setProperty('--sidebar-w', '274px')
  },
  methods: {
    isActive(path) {
      if (path === '/analysis') {
        return this.$route.path.startsWith('/analysis')
      }
      return this.$route.path === path
    },
    toggleSidebar() {
      this.$emit('toggle')
      if (!this.forceCollapsed && window.innerWidth >= 768) {
        this.isCollapsed = !this.isCollapsed
        this.setSidebarWidth()
      }
    },
    setSidebarWidth() {
      const w = this.collapsed ? '76px' : '274px'
      document.documentElement.style.setProperty('--sidebar-w', w)
    },
  },
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-w);
  min-height: 800px;
  height: 100dvh;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  border-radius: 0 16px 16px 0;
  padding: 12px 16px 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 20;
  transition: width 0.2s ease, padding 0.2s ease, transform 0.2s ease;
}

@media (max-width: 767px) {
  .sidebar {
    width: 260px !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.12);
    transform: translateX(0);
  }
  .sidebar.is-mobile-hidden {
    transform: translateX(-100%);
  }
}

.sidebar.is-collapsed {
  padding: 12px 10px 16px;
}

.sidebar-main {
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  scrollbar-width: none;
  padding-right: 2px;
}

.sidebar-main::-webkit-scrollbar {
  display: none;
}

.brand-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0 8px;
  min-height: 32px;
  overflow: hidden;
}

.brand-logo {
  width: 26px;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-name {
  font-size: 15px;
  line-height: 20px;
  font-weight: 700;
  color: #1B1A25;
  letter-spacing: -0.03em;
  white-space: nowrap;
  font-family: 'Inter', sans-serif;
}

.beta-badge {
  background: #E6E8EA;
  color: #61717C;
  border-radius: 1000px;
  font-size: 11px;
  font-weight: 700;
  line-height: 13px;
  padding: 3px 8px;
  white-space: nowrap;
}

.collapse-toggle {
  margin-left: auto;
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  border: none;
  border-radius: 6px;
  background: #E1E4E7;
  color: #667A85;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s ease;
}
.collapse-toggle:hover {
  background: #D0D4D8;
}

.menu-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.group-title {
  font-size: 14px;
  line-height: 21px;
  color: #83939C;
  font-weight: 600;
  padding: 4px 0;
}

.group-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.nav-item {
  width: 100%;
  min-height: 40px;
  border-radius: 12px;
  padding: 8px;
  color: var(--sidebar-text);
  font-size: 16px;
  line-height: 24px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: background 0.15s ease, color 0.15s ease;
}

.nav-item:hover {
  background: var(--sidebar-hover-bg);
}

.nav-icon {
  width: 24px;
  height: 24px;
  color: #667A85;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.nav-label {
  flex: 1;
}

.nav-item.active {
  background: var(--sidebar-active-bg);
  color: var(--sidebar-text-active);
}

.nav-item.active .nav-icon {
  color: #2B31B3;
}

.item-badge {
  border-radius: 1000px;
  padding: 4px 8px;
  font-size: 12px;
  line-height: 14px;
  font-weight: 700;
  background: #D5D6F8;
  color: #2B31B3;
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 8px;
}

.tokens-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px;
}

.tokens-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.tokens-label {
  font-size: 14px;
  line-height: 21px;
  color: #171C1F;
  font-style: italic;
  font-weight: 700;
}

.tokens-value {
  font-size: 14px;
  line-height: 21px;
  color: #171C1F;
  font-weight: 400;
}

.tokens-track {
  width: 100%;
  height: 8px;
  border-radius: 999px;
  background: #E6E8EA;
  overflow: hidden;
}

.tokens-fill {
  width: 28%;
  height: 100%;
  background: #2B31B3;
}

.plan-row {
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  border: none;
  background: transparent;
  padding: 0;
  cursor: pointer;
}

.plan-name {
  font-size: 14px;
  line-height: 21px;
  color: #83939C;
  font-weight: 500;
}

.plan-arrow {
  color: #667A85;
  font-size: 20px;
  line-height: 20px;
  transition: transform 0.18s ease;
}

.plan-arrow.open {
  transform: rotate(90deg);
}

.upgrade-box {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.upgrade-sub {
  font-size: 14px;
  line-height: 20px;
  color: #4E616B;
  font-weight: 500;
}

.upgrade-btn {
  width: 100%;
  height: 40px;
  border: none;
  border-radius: 10px;
  background: #E9EBEE;
  color: #2B31B3;
  font-size: 18px;
  line-height: 1;
  font-weight: 600;
  cursor: pointer;
}

.profile-row {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  border-radius: 12px;
  padding: 8px 4px;
}

.profile-row.compact {
  justify-content: center;
  padding: 8px 0;
}

.profile-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(145deg, #d6dce2 0%, #b6c1cc 100%);
  flex-shrink: 0;
}

.profile-body {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.profile-name {
  font-size: 14px;
  line-height: 21px;
  color: #4E616B;
  font-weight: 500;
}

.profile-phone {
  font-size: 12px;
  line-height: 14px;
  color: #A0ADB4;
}

.lang-chip {
  align-self: flex-start;
  border: none;
  background: transparent;
  color: #83939C;
  border-radius: 12px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.flag-ru {
  width: 24px;
  height: 16px;
  border-radius: 2px;
  border: 1px solid rgba(0,0,0,0.1);
  background: linear-gradient(
    to bottom,
    #FFFFFF 0%,
    #FFFFFF 33.33%,
    #0034A9 33.33%,
    #0034A9 66.66%,
    #D7280F 66.66%,
    #D7280F 100%
  );
}

.sidebar.is-collapsed .group-list {
  gap: 6px;
}

.sidebar.is-collapsed .nav-item {
  justify-content: center;
  padding: 8px 0;
}

.sidebar.is-collapsed .sidebar-footer {
  align-items: center;
}
</style>
