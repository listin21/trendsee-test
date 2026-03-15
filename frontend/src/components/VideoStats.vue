<template>
  <div class="stats-list">
    <div class="stat-row" v-for="s in sanitizedStats" :key="s.label">
      <span class="stat-icon" v-html="s.icon"></span>
      <span class="stat-label">{{ s.label }}</span>
      <span class="stat-val">{{ s.value }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { PropType } from 'vue'

interface StatItem {
  icon: string
  label: string
  value: string
}

const props = defineProps({
  stats: {
    type: Array as PropType<StatItem[]>,
    required: true,
    validator: (value: unknown[]) =>
      Array.isArray(value) &&
      value.every(
        (item) =>
          typeof item === 'object' &&
          item !== null &&
          typeof (item as StatItem).icon === 'string' &&
          typeof (item as StatItem).label === 'string' &&
          typeof (item as StatItem).value === 'string'
      ),
  },
})

function sanitizeSvg(input: string): string {
  // Allow only inline SVG content and remove scriptable attributes/tags.
  const parser = new DOMParser()
  const doc = parser.parseFromString(input, 'image/svg+xml')
  const svg = doc.querySelector('svg')
  if (!svg) return ''

  const blockedTags = new Set(['script', 'foreignObject'])
  const walker = doc.createTreeWalker(svg, NodeFilter.SHOW_ELEMENT)
  const toRemove: Element[] = []

  while (walker.nextNode()) {
    const el = walker.currentNode as Element
    if (blockedTags.has(el.tagName)) {
      toRemove.push(el)
      continue
    }
    for (const attr of [...el.attributes]) {
      const n = attr.name.toLowerCase()
      const v = attr.value.toLowerCase()
      if (n.startsWith('on') || v.includes('javascript:')) {
        el.removeAttribute(attr.name)
      }
    }
  }
  for (const el of toRemove) el.remove()

  return svg.outerHTML
}

const sanitizedStats = computed(() =>
  props.stats.map((s) => ({ ...s, icon: sanitizeSvg(s.icon) }))
)
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
