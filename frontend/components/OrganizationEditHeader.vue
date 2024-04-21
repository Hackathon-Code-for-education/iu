<script setup lang="ts">
import { useOrganizationsGetByUsername } from '~/api'

const props = defineProps<{
  orgUsername: string
  orgId: string
}>()

const { data: org } = useOrganizationsGetByUsername(props.orgUsername, { query: { retry: 0 } })
</script>

<template>
  <UContainer v-if="org">
    <Card class="bg-neutral-900 p-4 gap-2 flex flex-col mb-4">
      <div class="flex justify-between items-start">
        <h1 class="text-2xl font-medium">
          {{ org.data.name }}
        </h1>
        <UButton
          :to="`/${orgUsername}`"
          variant="ghost"
          label="Просмотреть страницу"
          size="sm"
          color="gray"
        />
      </div>
      <div class="flex items-start">
        <UHorizontalNavigation
          :links="[
            { icon: 'i-octicon-info', label: 'Данные', to: `/${orgUsername}/edit` },
            { icon: 'i-octicon-location', label: 'Локации', to: `/${orgUsername}/edit/scenes` },
          ]"
        />
      </div>
    </Card>
  </UContainer>
</template>
