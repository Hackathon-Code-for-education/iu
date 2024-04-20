<script lang="ts" setup>
import ChatBubble from './ChatBubble.vue'

export type Message = {
  id: string;
  content: string;
  date: Date;
  incoming: boolean;
}

const props = defineProps<{
  title: string;
  messages: Message[];
  input: string
  inputDisabled: boolean
}>()

defineEmits<{
  'update:input': [value: string]
  'send': []
}>()

const messagesGrouped = computed(() => {
  const msgs = unref(props.messages)
  msgs.sort((a, b) => a.date.getTime() - b.date.getTime())
  const groups = msgs.reduce((acc, msg) => {
    const key = msg.date.toLocaleDateString()
    if (!acc[key]) {
      acc[key] = []
    }
    acc[key].push(msg)
    return acc
  }, {} as Record<string, Message[]>)
  return Object.values(groups).sort((a, b) => b[0].date.getTime() - a[0].date.getTime())
})
</script>

<template>
  <div class="h-full w-full min-h-[500px] flex flex-col items-stretch">
    <!-- <header class="basis-auto shrink-0 grow-0">
      <h2>{{ title }}</h2>
    </header> -->
    <div class="flex-auto relative">
      <div class="overflow-y-auto flex flex-col-reverse w-full absolute max-h-full px-4 bg-fixed bg-repeat bg-[url('/img/chat-pattern-white.svg')] dark:bg-[url('/img/chat-pattern-black.svg')]">
        <div v-for="messageGroup in messagesGrouped" :key="messageGroup[0].date.getTime()" class="relative pt-2 max-h-full">
          <h3
            class="sticky inline-block top-0 left-1/2 -translate-x-1/2 text-[16px] leading-[16px] px-[8px] py-[2px] rounded-full bg-gray-500 bg-opacity-25 backdrop-blur-sm">
            {{ messageDate(messageGroup[0].date) }}
          </h3>
          <div class="flex flex-col gap-2 py-2">
            <ChatBubble v-for="message in messageGroup" :key="message.id" :message="message" />
          </div>
        </div>
      </div>
    </div>
    <div class="flex basis-auto shrink-0 grow-0 gap-4 py-2 px-4 items-start border-t border-gray-700">
      <UTextarea
        class="w-full"
        :maxrows="5"
        :rows="1"
        autoresize
        :model-value="input"
        @change="(val) => $emit('update:input', val)"
        :disabled="inputDisabled"
      />
      <UButton
        @click="$emit('send')"
        :disabled="inputDisabled"
        icon="i-heroicons-paper-airplane"
      />
    </div>
  </div>
</template>
