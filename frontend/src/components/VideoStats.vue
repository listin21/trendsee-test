<template>
  <div class="stats-list">
    <div class="stat-row" v-for="s in stats" :key="s.label">
      <span class="stat-icon" v-html="s.icon"></span>
      <span class="stat-label">{{ s.label }}</span>
      <span class="stat-val">{{ s.value }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stats: { type: Array, required: true }
  // each: { icon: String (svg html), label: String, value: String }
})
</script>

<style scoped>
.stats-list { display: flex; flex-direction: column; gap: 4px; }
.stat-row {
  display: flex; align-items: center; gap: 8px;
  background: #F4F5F6; border-radius: 12px;
  padding: 8px 12px; box-sizing: border-box;
}
.stat-icon { display: flex; align-items: center; flex-shrink: 0; }
.stat-label { flex: 1; font-size: 12px; color: #343A40; letter-spacing: 0.4px; font-family: 'Inter', sans-serif; }
.stat-val { font-size: 14px; font-weight: 500; color: #393C4C; font-family: 'Inter', sans-serif; }
</style>
