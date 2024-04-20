<script setup lang="ts">
const colorMode = useColorMode()
function handleClick() {
  colorMode.preference = colorMode.value === 'light' ? 'dark' : 'light'
}
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold text-center">Hi there!</h1>
  </div>
</template>
