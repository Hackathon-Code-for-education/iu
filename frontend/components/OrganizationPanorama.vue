<script setup lang="ts">
import { getFileUrl } from '~/api/file'
import { useScenesGetScenesForOrganization } from '~/api'

const props = defineProps<{
  orgUsername: string
  orgId: string
  mainSceneId?: string
}>()

const { data: scenes } = useScenesGetScenesForOrganization(props.orgId, { query: { retry: 0 } })

function composeSceneData(scene: any) {
  return {
    panorama: getFileUrl(scene.file),
    title: scene.title,
    type: 'equirectangular',
    ...(scene.meta || {}),
  }
}

const scenesData = computed(() => scenes?.value?.data && Object.fromEntries(scenes.value.data.map(scene => [scene.id, composeSceneData(scene)])))
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
