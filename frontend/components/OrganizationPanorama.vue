<script setup lang="ts">
import { useScenesGetScenesForOrganization } from '~/api'
import { type SceneExtended, composeSceneData } from '~/api/scenes'

const props = defineProps<{
  orgUsername: string
  orgId: string
  mainSceneId?: string
}>()

const { data: scenes } = useScenesGetScenesForOrganization(props.orgId, { query: { retry: 0 } })

const scenesData = computed(() => scenes?.value?.data && Object.fromEntries(
  scenes.value.data.map(scene => [scene.id, composeSceneData(scene as SceneExtended)]),
))
</script>

<template>
  <ClientOnly>
    <VuePannellum
      v-if="scenesData"
      :default="{
        firstScene: props.mainSceneId,
        sceneFadeDuration: 1000,
      }"
      :scenes="scenesData"
      :yaw="props.mainSceneId && scenesData[props.mainSceneId]?.yaw || 0"
      :pitch="props.mainSceneId && scenesData[props.mainSceneId]?.pitch || 0"
      auto-load
      show-fullscreen
      style="width: 100%; height: 300px;"
    />
  </ClientOnly>
</template>
