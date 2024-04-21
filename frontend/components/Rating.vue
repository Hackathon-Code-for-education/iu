<script lang="ts" setup>
const props = defineProps<{
  modelValue: number
  disabled?: boolean
  size?: 'sm' | 'md'
  readonly?: boolean
}>()
const emit = defineEmits<{
  'update:modelValue': [v: number]
}>()

function handleStarClick(v: number) {
  if (!props.disabled)
    emit('update:modelValue', v)
}
</script>

<template>
  <div
    class="flex gap-2"
    :class="[
      (!readonly && disabled && 'cursor-not-allowed opacity-85'),
    ]"
  >
    <UIcon
      v-for="(_, i) in new Array(5).fill(null)"
      :key="i"
      :name="modelValue >= (i + 1) ? 'i-octicon-star-fill-24' : 'i-octicon-star-24'"
      class="text-yellow-400 text-[32px]"
      :class="[
        (!readonly && !disabled && 'cursor-pointer'),
        size === 'sm' ? 'text-[24px]' : 'text-[32px]',
        modelValue >= (i + 1) ? 'rated' : '',
      ]"
      @click="handleStarClick(i + 1)"
    />
  </div>
</template>

<style>
@keyframes rated-anim {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

.rated {
  animation: rated-anim 0.5s;
}
</style>
