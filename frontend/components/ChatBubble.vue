<script lang="ts" setup>
import type { Message } from './Chat.vue'

defineProps<{
  message: Message
}>()
</script>

<template>
  <div class="bubble relative dark:bg-green-900 bg-green-200 px-2 pt-1 pb-[24px] rounded-md" :class="[message.incoming ? 'self-start' : 'self-end']">
    <div>
      {{ message.content }}
    </div>
    <span class="text-xs opacity-50 absolute right-2 bottom-2" :title="message.date.toLocaleString()">
      {{ `${message.date.getHours().toString().padStart(2, '0')}:${message.date.getMinutes().toString().padStart(2, '0')}` }}
    </span>
  </div>
</template>

<style scoped>
.bubble {
  min-width: 50px;
  max-width: min(60%, 500px);
}
</style>
