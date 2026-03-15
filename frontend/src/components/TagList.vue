<template>
  <div class="tag-list">
    <span
      v-for="tag in tags"
      :key="tag.label"
      class="tag"
      :style="{ background: tag.bg, color: tag.color }"
    >{{ tag.label }}</span>
  </div>
</template>

<script setup lang="ts">
interface Tag {
  label: string
  bg: string
  color: string
}

defineProps<{
  tags: Tag[]
}>()
</script>

<style scoped>
.tag-list { display: flex; gap: 6px; flex-wrap: wrap; }
.tag {
  font-size: 13px; font-weight: 500;
  padding: 4px 12px; border-radius: 1000px;
  font-family: 'Inter', sans-serif;
}
</style>
