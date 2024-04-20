<script setup lang="ts">
import { useQueryClient } from '@tanstack/vue-query'
import {
  getScenesGetScenesForOrganizationQueryKey,
  useOrganizationsGetByUsername,
  useScenesGetScenesForOrganization,
  useScenesUpdate,
} from '~/api'
import { getFileUrl } from '~/api/file'

const props = defineProps<{
  orgUsername: string
  orgId: string
  sceneId: string
}>()

const queryClient = useQueryClient()
const { data: org } = useOrganizationsGetByUsername(props.orgUsername, { query: { retry: 0 } })
const { data: scenes } = useScenesGetScenesForOrganization(props.orgId, { query: { retry: 0 } })

const { mutate: updateScene } = useScenesUpdate({
  mutation: {
    onSuccess(data, variables, context) {
      queryClient.setQueryData(getScenesGetScenesForOrganizationQueryKey(props.orgId), (oldData: any) => {
        if (!oldData)
          return oldData

        return {
          ...oldData,
          data: oldData.data.map((scene: any) => scene.id === data.data.id ? data.data : scene),
        }
      })
    },
  },
})

function composeSceneData(scene: any) {
  return {
    panorama: getFileUrl(scene.file),
    title: scene.title,
    type: 'equirectangular',
    ...(scene.meta || {}),
  }
}

const scene = computed(() => scenes.value?.data.find(scene => scene.id === props.sceneId))
const scenesData = ref(scene.value ? { current: composeSceneData(scene.value) } : {})
const scenesDataId = ref<string>(scene.value?.id || '')
watch(scene, () => {
  if (!scene.value || scenesDataId.value === scene.value?.id)
    return

  scenesData.value = { current: composeSceneData(scene.value) }
  scenesDataId.value = scene.value.id
})

const pannellum = ref(null)
const sceneInfo = reactive({ title: scene.value?.title || '', yaw: scene.value?.meta?.yaw || 0, pitch: scene.value?.meta?.pitch || 0 })

function savePosition() {
  if (!scene.value || !pannellum.value)
    return

  updateScene({
    id: scene.value.id,
    data: {
      meta: {
        ...(scene.value.meta || {}),
        yaw: pannellum.value.viewer.getYaw(),
        pitch: pannellum.value.viewer.getPitch(),
      },
    },
  })
}

function restorePosition() {
  sceneInfo.yaw = scene.value?.meta?.yaw || 0
  sceneInfo.pitch = scene.value?.meta?.pitch || 0
}

function save() {
  if (!scene.value)
    return

  updateScene({ id: scene.value.id, data: { title: sceneInfo.title } })
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <div class="flex justify-end">
      <UButton @click="save">
        Сохранить
      </UButton>
    </div>
    <UInput v-model="sceneInfo.title" label="Название локации" />
    <ClientOnly>
      <VuePannellum
        ref="pannellum"
        v-model:yaw="sceneInfo.yaw"
        v-model:pitch="sceneInfo.pitch"
        :default="{
          firstScene: 'current',
          sceneFadeDuration: 1000,
        }"
        :scenes="scenesData"
        auto-load
        show-fullscreen
        style="width: 100%; height: 300px;"
      />
    </ClientOnly>
    <div class="flex flex-row gap-2 justify-end">
      <UButton variant="ghost" @click="savePosition">
        Сохранить позицию
      </UButton>
      <UButton variant="ghost" @click="restorePosition">
        Восстановить позицию
      </UButton>
    </div>
  </div>
</template>
