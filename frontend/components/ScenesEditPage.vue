<script setup lang="ts">
import { useOrganizationsGetByUsername, useScenesGetScenesForOrganization } from '~/api'

const props = defineProps<{
  orgUsername: string
  orgId: string
}>()

const { data: org } = useOrganizationsGetByUsername(props.orgUsername, { query: { retry: 0 } })
const { data: scenes } = useScenesGetScenesForOrganization(props.orgId, { query: { retry: 0 } })

const sceneId = ref(org.value?.data.main_scene)
</script>

<template>
  <UContainer v-if="org && scenes">
    <Card class="bg-neutral-900">
      <div class="px-4 flex py-4 justify-between items-start">
        <div class="flex justify-between gap-5 items-end">
          <div>
            <h1 class="text-2xl font-medium">
              {{ org.data.name }}
            </h1>
          </div>
        </div>
      </div>
    </Card>
    <div class="grid grid-cols-3 gap-4 mt-4">
      <Card class="p-4">
        <div class="flex flex-col gap-2">
          <h3 class="font-bold">
            Локации
          </h3>
          <UButton
            v-for="scene in scenes?.data"
            :key="scene.id"
            :label="scene.title"
            :variant="sceneId !== scene.id ? 'ghost' : 'solid'"
            icon="i-mdi-location"
            size="sm"
            :color="org.data.main_scene === scene.id ? 'green' : 'gray'"
            @click="sceneId = scene.id"
          />
          <UButton
            icon="i-mdi-plus"
            size="sm"
            variant="ghost"
            color="gray"
            label="Добавить локацию"
            @click="console.log('!')"
          />
        </div>
      </Card>
      <Card class="p-4 col-span-2">
        <ScenesEditLocation
          v-if="sceneId"
          :org-username="props.orgUsername"
          :org-id="props.orgId"
          :scene-id="sceneId"
        />
        <p v-else>
          Выберите локацию
        </p>
      </Card>
    </div>
  </UContainer>
</template>
