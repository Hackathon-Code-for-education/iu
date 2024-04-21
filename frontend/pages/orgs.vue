<script lang="ts" setup>
import { useOrganizationsReadAll } from '~/api'
import { getFileUrl } from '~/api/file'

const { data: orgs } = useOrganizationsReadAll()
</script>

<template>
  <UContainer>
    <div v-if="orgs" class="grid grid-cols-3 gap-4">
      <NuxtLink v-for="org in orgs.data" :key="org.id" :to="`/${org.username}`">
        <Card class="px-4 h-[80px] flex gap-4 items-center hover:dark:border-green-700 hover:border-green-600">
          <UAvatar size="xl" :src="org.logo ? getFileUrl(org.logo) : undefined" />
          <h3 class="text-xl line-clamp-2">
            {{ org.name }}
          </h3>
        </Card>
      </NuxtLink>
    </div>
    <div v-else class="grid grid-cols-3 gap-4">
      <Card v-for="i in new Array(5).fill(null)" :key="i" class="px-4 h-[80px] flex gap-4 items-center">
        <USkeleton class="h-14 w-14 rounded-full" />
        <USkeleton class="rounded h-8 grow" />
      </Card>
    </div>
  </UContainer>
</template>
