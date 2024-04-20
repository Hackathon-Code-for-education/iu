<script lang="ts" setup>
import { useOrganizationsReadAll } from '~/api'

const { data: orgs, isLoading } = useOrganizationsReadAll()
</script>

<template>
  <UContainer>
    <div v-if="orgs" class="grid grid-cols-3 gap-4">
      <NuxtLink v-for="org in orgs.data" :key="org.id" :to="`/${org.username}`">
        <Card class="p-6">
          <h3 class="text-xl">
            {{ org.name }}
          </h3>
        </Card>
      </NuxtLink>
    </div>
    <div v-else-if="isLoading" class="grid grid-cols-3 gap-4">
      <USkeleton class="rounded-xl" />
    </div>
  </UContainer>
</template>
