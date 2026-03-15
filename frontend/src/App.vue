<template>
  <div id="app" :class="{ 'sidebar-open': sidebarOpen }">
    <div v-if="isMobile && sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false" aria-hidden="true"></div>
    <Sidebar :force-collapsed="isMobile && !sidebarOpen" @toggle="onSidebarToggle" />
    <main class="main-content" :style="mainStyle">
      <router-view v-slot="{ Component }">
        <component :is="Component" @open-sidebar="sidebarOpen = true" />
      </router-view>
    </main>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'

export default {
  name: 'App',
  components: { Sidebar },
  data() {
    return {
      isMobile: false,
      sidebarOpen: false,
    }
  },
  computed: {
    mainStyle() {
      if (this.isMobile) return { marginLeft: '0' }
      return {}
    },
  },
  mounted() {
    this.checkMobile()
    window.addEventListener('resize', this.checkMobile)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkMobile)
  },
  methods: {
    checkMobile() {
      this.isMobile = window.innerWidth < 768
      if (!this.isMobile) this.sidebarOpen = false
    },
    onSidebarToggle() {
      if (!this.isMobile) return
      this.sidebarOpen = !this.sidebarOpen
    },
  },
}
</script>

<style>
#app {
  display: flex;
  width: 100%;
  min-height: 100dvh;
  background: var(--bg);
  position: relative;
}

.main-content {
  margin-left: var(--sidebar-w);
  flex: 1;
  min-height: 100dvh;
  background: var(--bg);
  overflow-x: hidden;
  overflow-y: auto;
  transition: margin-left 0.2s ease;
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 19;
}

@media (max-width: 767px) {
  .main-content {
    margin-left: 0 !important;
    padding-bottom: 16px;
  }
}
</style>
