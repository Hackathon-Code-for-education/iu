<script lang="ts" setup>
import { refThrottled } from '@vueuse/core'
import { useOrganizationsReadAll } from '~/api'
import { getFileUrl } from '~/api/file'

const { data: orgs } = useOrganizationsReadAll()
const filter = ref('')
const filterThrottled = refThrottled(filter, 350)

const orgsFiltered = computed(() => {
  if (!orgs.value?.data)
    return null

  if (!filterThrottled.value.trim())
    return orgs.value.data

  return orgs.value.data.filter(org => (
    org.name.toLowerCase().includes(filterThrottled.value.toLowerCase())
    || org.username.toLowerCase().includes(filterThrottled.value.toLowerCase())
  ))
})
</script>

<template>
  <UContainer>
    <Card class="mb-4 px-4">
      <UInput
        v-model="filter"
        placeholder="Поиск по названию..."
        class="w-full py-2"
        variant="none"
      />
    </Card>
    <div v-if="orgsFiltered" class="grid grid-cols-3 gap-4">
      <NuxtLink v-for="org in orgsFiltered" :key="org.id" :to="`/${org.username}`">
        <Card class="px-4 h-[80px] flex gap-4 items-center hover:dark:border-green-700 hover:border-green-600">
          <UAvatar size="xl" :src="org.logo ? getFileUrl(org.logo) : undefined" />
          <h3 class="text-xl line-clamp-2">
            {{ org.name }}
          </h3>
        </Card>
      </NuxtLink>
    </div>
    <div v-else class="grid grid-cols-3 gap-4">
      <Card v-for="(_, i) in new Array(8).fill(null)" :key="i" class="px-4 h-[80px] flex gap-4 items-center">
        <USkeleton class="h-14 w-14 rounded-full" />
        <USkeleton class="rounded h-8 grow" />
      </Card>
    </div>
  </UContainer>
</template>
