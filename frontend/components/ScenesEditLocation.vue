<script setup lang="ts">
import { useOrganizationsGetByUsername, useScenesGetScenesForOrganization } from '~/api'
import { getFileUrl } from '~/api/file'

const props = defineProps<{
  orgUsername: string
  orgId: string
  sceneId: string
}>()

const { data: org } = useOrganizationsGetByUsername(props.orgUsername, { query: { retry: 0 } })
const { data: scenes } = useScenesGetScenesForOrganization(props.orgId, { query: { retry: 0 } })

const scene = ref(scenes.value?.data.find(scene => scene.id === props.sceneId))
const data = ref({})
const pannellum = ref(null)

function reload() {
  scene.value = scenes.value?.data.find(scene => scene.id === props.sceneId)
  data.value = scene.value
    ? {
        current: {
          panorama: getFileUrl(scene.value.file),
          title: scene.value.title,
          hfov: 110,
          yaw: scene.value.meta?.yaw || 0,
          pitch: scene.value.meta?.pitch || 0,
          type: 'equirectangular',
        },
      }
    : {}
}

watch(() => props.sceneId, reload)
watch(() => scenes.value, reload)

function save() {
}
</script>

<template>
  <UContainer v-if="org && scene">
    <h3>Локация</h3>
    <UButton @click="save">
      Сохранить
    </UButton>
    <ClientOnly>
      <VuePannellum
        ref="pannellum"
        :default="{
          firstScene: 'current',
          sceneFadeDuration: 1000,
        }"
        :scenes="data"
        :pitch="25"
        auto-load
        show-fullscreen
        style="width: 100%; height: 300px;"
      />
    </ClientOnly>
  </UContainer>
</template>
