<script setup lang="ts">
import { useOrganizationsGetByUsername, useScenesGetScenesForOrganization } from '~/api'

const props = defineProps<{
  orgUsername: string
  orgId: string
}>()

const { data: org } = useOrganizationsGetByUsername(props.orgUsername, { query: { retry: 0 } })
const { data: scenes } = useScenesGetScenesForOrganization(props.orgId, { query: { retry: 0 } })
</script>

<template>
  <UContainer v-if="org && scenes">
    <div class="grid grid-cols-3 gap-4 mt-4">
      <Card class="p-4 h-80" />
      <Card class="p-4 h-80 col-span-2" />
    </div>
  </UContainer>
</template>
