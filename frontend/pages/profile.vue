<script lang="ts" setup>
const { me, loggedIn } = useMe()

watch(loggedIn, (newLoggedIn) => {
  if (newLoggedIn === false)
    navigateTo('/login')
}, { immediate: true })
</script>

<template>
  <UContainer>
    <div v-if="!me">
      <USkeleton class="w-[300px] h-[200px] rounded-xl" />
    </div>

    <div v-else>
      <Card class="w-[300px] h-[200px] p-6">
        <h3>{{ me.name }}</h3>
      </Card>
    </div>
  </UContainer>
</template>
