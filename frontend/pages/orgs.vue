<script lang="ts" setup>
import { useOrganizationsReadAll } from '~/api'

const { data: orgs, isLoading } = useOrganizationsReadAll()
</script>

<template>
  <UContainer>
    <div v-if="orgs" class="grid grid-cols-3 gap-4">
      <NuxtLink v-for="org in orgs.data" :key="org.id" :to="`/${org.username}`">
        <Card class="px-4 h-[80px] flex items-center">
          <h3 class="text-xl">
            {{ org.name }}
          </h3>
        </Card>
      </NuxtLink>
    </div>
    <div v-else-if="isLoading" class="grid grid-cols-3 gap-4">
      <USkeleton class="rounded-xl h-[80px] w-full" />
      <USkeleton class="rounded-xl h-[80px] w-full" />
      <USkeleton class="rounded-xl h-[80px] w-full" />
      <USkeleton class="rounded-xl h-[80px] w-full" />
      <USkeleton class="rounded-xl h-[80px] w-full" />
    </div>
  </UContainer>
</template>
