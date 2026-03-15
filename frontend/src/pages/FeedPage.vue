<template>
  <div class="feed-page">
    <!-- Topbar -->
    <header class="topbar">
      <button class="menu-btn" aria-label="Открыть меню" @click="$emit('open-sidebar')">
        <svg width="18" height="14" viewBox="0 0 18 14" fill="none">
          <rect y="0" width="18" height="2" rx="1" fill="#667A85"/>
          <rect y="6" width="18" height="2" rx="1" fill="#667A85"/>
          <rect y="12" width="18" height="2" rx="1" fill="#667A85"/>
        </svg>
      </button>
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="tab"
          :class="{ active: isTabActive(tab.key) }"
          @click="onTabClick(tab.key)"
        >{{ tab.label }}</button>
      </div>
      <div class="topbar-right">
        <div class="search-box">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" placeholder="Поиск..." v-model="searchQuery" aria-label="Поиск" />
        </div>
        <button class="btn-primary">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Добавить
        </button>
      </div>
    </header>

    <!-- Initial loader -->
    <div v-if="loading && posts.length === 0" class="initial-loader">
      <div class="spinner"></div>
    </div>

    <!-- Grid -->
    <div v-else class="grid">
      <VideoCard
        v-for="post in filteredPosts"
        :key="post.id"
        :post="post"
        :liked="likedIds.has(post.id)"
        @open-analysis="openModal"
        @toggle-like="toggleLike(post.id)"
      />
    </div>

    <!-- Empty favorites state -->
    <div v-if="activeTab === 'favorites' && filteredPosts.length === 0 && !loading" class="empty-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" stroke="#C5CDD2" stroke-width="1.5"/></svg>
      <p>Нет избранных видео</p>
      <span>Нажмите на сердечко в карточке, чтобы добавить</span>
    </div>

    <!-- Pagination loader -->
    <div v-if="loading && posts.length > 0" class="bottom-loader">
      <div class="spinner"></div>
    </div>

    <div v-if="!hasMore && posts.length > 0 && activeTab !== 'favorites'" class="end-msg">Все публикации загружены</div>

    <!-- Scroll sentinel -->
    <div ref="sentinel" style="height:1px"></div>

    <!-- Modal -->
    <AnalysisModal :show="showModal" :post="selectedPost || {}" @close="closeModal" />
  </div>
</template>

<script>
import VideoCard from '../components/VideoCard.vue'
import AnalysisModal from '../components/AnalysisModal.vue'
import { getPost, getPosts } from '../services/api.js'

export default {
  name: 'FeedPage',
  components: { VideoCard, AnalysisModal },
  data() {
    return {
      posts: [],
      loading: false,
      hasMore: true,
      page: 1,
      limit: 20,
      showModal: false,
      selectedPost: null,
      searchQuery: '',
      activeTab: 'feed',
      likedIds: new Set(),
      tabs: [
        { key: 'feed',      label: 'Лента' },
        { key: 'analysis',  label: 'Анализ' },
        { key: 'favorites', label: 'Избранное' },
      ],
      observer: null
    }
  },
  watch: {
    '$route.fullPath': {
      immediate: true,
      handler() {
        this.syncTabWithRoute()
        this.syncModalWithRoute()
      },
    },
  },
  computed: {
    filteredPosts() {
      let list = this.posts
      if (this.activeTab === 'favorites') {
        list = list.filter(p => this.likedIds.has(p.id))
      }
      if (this.searchQuery.trim()) {
        const q = this.searchQuery.toLowerCase()
        list = list.filter(p =>
          (p.title || '').toLowerCase().includes(q) ||
          (p.text || '').toLowerCase().includes(q)
        )
      }
      return list
    }
  },
  mounted() {
    this.loadPosts()
    this.observer = new IntersectionObserver(
      entries => { if (entries[0].isIntersecting) this.loadPosts() },
      { rootMargin: '500px' }
    )
    this.$nextTick(() => {
      if (this.$refs.sentinel) this.observer.observe(this.$refs.sentinel)
    })
  },
  beforeUnmount() {
    if (this.observer) this.observer.disconnect()
    document.body.style.overflow = ''
  },
  methods: {
    syncTabWithRoute() {
      if (this.$route.path.startsWith('/analysis')) {
        this.activeTab = 'analysis'
        return
      }
      if (this.$route.path === '/') {
        this.activeTab = 'feed'
      }
    },
    isTabActive(tabKey) {
      if (tabKey === 'favorites') return this.activeTab === 'favorites'
      return this.activeTab === tabKey
    },
    onTabClick(tabKey) {
      this.activeTab = tabKey
      if (tabKey === 'feed') {
        this.$router.push('/')
        return
      }
      if (tabKey === 'analysis') {
        if (this.selectedPost?.id) {
          this.$router.push(`/analysis/${this.selectedPost.id}`)
        } else {
          this.$router.push('/analysis')
        }
      }
    },
    async syncModalWithRoute() {
      const routePostId = this.$route.params.postId
      if (!routePostId) {
        this.showModal = false
        return
      }

      const targetId = Number(routePostId)
      if (!Number.isFinite(targetId)) {
        this.showModal = false
        return
      }

      if (this.selectedPost?.id === targetId && this.showModal) return

      const existingPost = this.posts.find(post => Number(post.id) === targetId)
      if (existingPost) {
        this.selectedPost = existingPost
        this.showModal = true
        return
      }

      try {
        const fetchedPost = await getPost(targetId)
        this.selectedPost = fetchedPost
        this.showModal = true
      } catch (e) {
        console.error(e)
        this.showModal = false
      }
    },
    async loadPosts() {
      if (this.loading || !this.hasMore) return
      this.loading = true
      try {
        const newPosts = await getPosts(this.page, this.limit)
        if (!newPosts.length) {
          this.hasMore = false
        } else {
          this.posts.push(...newPosts)
          this.page++
          if (newPosts.length < this.limit) this.hasMore = false
          if (this.$route.params.postId) this.syncModalWithRoute()
        }
      } catch (e) {
        console.error(e)
      } finally {
        this.loading = false
      }
    },
    toggleLike(postId) {
      const next = new Set(this.likedIds)
      if (next.has(postId)) {
        next.delete(postId)
      } else {
        next.add(postId)
      }
      this.likedIds = next
    },
    openModal(post) {
      this.selectedPost = post
      this.showModal = true
      document.body.style.overflow = 'hidden'
      if (Number(this.$route.params.postId) !== Number(post.id)) {
        this.$router.push(`/analysis/${post.id}`)
      }
    },
    closeModal() {
      this.showModal = false
      document.body.style.overflow = ''
      if (this.$route.path.startsWith('/analysis')) {
        this.$router.push('/')
      }
    }
  }
}
</script>

<style scoped>
.feed-page {
  width: 100%;
  min-height: 100dvh;
  padding: 16px;
  background: #F4F5F6;
  box-sizing: border-box;
}

.topbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  min-height: 44px;
  flex-wrap: nowrap;
  background: #fff;
  border-radius: 14px;
  padding: 6px 8px;
  border: 1px solid #E6E8EA;
}

.tabs {
  display: flex;
  gap: 2px;
  background: #F0F2F5;
  border-radius: 10px;
  padding: 3px;
  height: 34px;
  align-items: center;
  flex-shrink: 0;
}

.tab {
  height: 28px;
  padding: 0 14px;
  border-radius: 8px;
  border: none;
  background: transparent;
  font-size: 13px;
  font-weight: 600;
  color: #667A85;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s ease, color 0.15s ease;
}
.tab:hover {
  background: #E5E8EE;
  color: #3C4D59;
}
.tab.active {
  background: #4966F0;
  color: #fff;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  flex-shrink: 0;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 34px;
  background: #F4F5F6;
  border: 1px solid #E0E3E8;
  border-radius: 8px;
  padding: 0 12px;
  color: #7A8891;
  min-width: 160px;
  max-width: 220px;
  flex: 1 1 160px;
}
.search-box svg { flex-shrink: 0; }
.search-box input {
  border: none;
  outline: none;
  font-size: 13px;
  color: #4E616B;
  background: transparent;
  width: 100%;
  min-width: 0;
}
.search-box input::placeholder { color: #A0ADB4; }

.btn-primary {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 34px;
  padding: 0 14px;
  white-space: nowrap;
  background: #4966F0;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  flex-shrink: 0;
  transition: opacity 0.15s ease, transform 0.12s ease;
}
.btn-primary:hover { opacity: 0.88; }
.btn-primary:active { transform: scale(0.97); }
.btn-primary svg { width: 14px; height: 14px; }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 12px;
  align-items: start;
}

.initial-loader {
  display: flex;
  justify-content: center;
  padding: 80px 0;
}

.bottom-loader {
  display: flex;
  justify-content: center;
  padding: 28px 0;
}

.spinner {
  width: 28px;
  height: 28px;
  border: 3px solid rgba(255,255,255,0.1);
  border-top-color: #4F6EF7;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.end-msg {
  text-align: center;
  padding: 24px;
  font-size: 13px;
  color: #5C5C6E;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 80px 20px;
  text-align: center;
}
.empty-state p {
  font-size: 16px;
  font-weight: 600;
  color: #4E616B;
  margin: 0;
}
.empty-state span {
  font-size: 13px;
  color: #A0ADB4;
}

.menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
}

@media (max-width: 767px) {
  .menu-btn { display: flex; }
  .feed-page {
    width: 100%;
    border-radius: 12px;
    padding: 10px;
  }
  .topbar {
    flex-wrap: wrap;
    gap: 8px;
    padding: 6px;
    border-radius: 10px;
  }
  .tabs { width: 100%; }
  .tab { flex: 1; padding: 0 8px; font-size: 12px; }
  .topbar-right { width: 100%; }
  .search-box { flex: 1; min-width: 0; max-width: none; }
  .grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; }
}

@media (min-width: 768px) and (max-width: 900px) {
  .grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
  }
  .topbar { flex-wrap: wrap; }
  .topbar-right { flex: 1; }
  .search-box { flex: 1; min-width: 0; max-width: none; }
}
</style>
