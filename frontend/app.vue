<script setup lang="ts">
import axios from 'axios'

const config = useRuntimeConfig()
axios.defaults.baseURL = config.public.apiUrl
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>

  <UNotifications />
</template>
