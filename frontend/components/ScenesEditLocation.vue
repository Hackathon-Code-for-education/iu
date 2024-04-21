<script setup lang="ts">
import { useQueryClient } from '@tanstack/vue-query'
import {
  getOrganizationsGetByUsernameQueryKey,
  getOrganizationsReadQueryKey,
  getScenesGetScenesForOrganizationQueryKey,
  useOrganizationsGetByUsername,
  useOrganizationsUpdate,
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
    onSuccess(data) {
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

const { mutate: updateOrg } = useOrganizationsUpdate({
  mutation: {
    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: getOrganizationsReadQueryKey(props.orgId),
      })
      queryClient.invalidateQueries({
        queryKey: getOrganizationsGetByUsernameQueryKey(props.orgUsername),
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
const isMainOrgScene = computed(() => org.value?.data.main_scene === props.sceneId)
const scenesData = ref(scene.value ? { current: composeSceneData(scene.value) } : {})
const scenesDataId = ref<string>(scene.value?.id || '')

const pannellum = ref(null)
const sceneInfo = reactive({ title: scene.value?.title || '', yaw: scene.value?.meta?.yaw || 0, pitch: scene.value?.meta?.pitch || 0 })

watch(() => scene.value?.id, () => {
  if (!scene.value)
    return

  sceneInfo.title = scene.value?.title || ''
  sceneInfo.yaw = scene.value?.meta?.yaw || 0
  sceneInfo.pitch = scene.value?.meta?.pitch || 0

  scenesData.value = { current: composeSceneData(scene.value) }
  scenesDataId.value = scene.value.id
})

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
  pannellum.value?.viewer.stopMovement()
  sceneInfo.yaw = scene.value?.meta?.yaw || 0
  sceneInfo.pitch = scene.value?.meta?.pitch || 0
}

function save() {
  if (!scene.value)
    return

  pannellum.value?.viewer.stopMovement()
  updateScene({ id: scene.value.id, data: { title: sceneInfo.title } })
}

function setAsMain() {
  if (!scene.value)
    return

  updateOrg({ id: props.orgId, data: { main_scene: props.sceneId } })
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <UButton
      :variant="isMainOrgScene ? 'ghost' : 'ghost'"
      :disabled="isMainOrgScene"
      :icon="isMainOrgScene ? 'i-mdi-check' : 'i-mdi-star'"
      class="w-fit"
      @click="setAsMain"
    >
      {{ isMainOrgScene ? 'Основная локация' : 'Сделать основной локацией' }}
    </UButton>
    <div class="flex w-full gap-2">
      <UInput v-model="sceneInfo.title" class="w-full" label="Название локации" />
      <UButton
        :variant="sceneInfo.title !== scene?.title ? undefined : 'ghost'"
        :disabled="sceneInfo.title === scene?.title"
        @click="save"
      >
        Сохранить
      </UButton>
    </div>
    <div class="relative">
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

        <div
          v-if="sceneInfo.yaw !== scene?.meta?.yaw"
          class="absolute flex flex-col gap-2 justify-end right-0 bottom-0"
        >
          <UButton class="justify-center" @click="savePosition">
            Сохранить позицию
          </UButton>
          <UButton class="justify-center" @click="restorePosition">
            Восстановить позицию
          </UButton>
        </div>
      </ClientOnly>
    </div>
  </div>
</template>
