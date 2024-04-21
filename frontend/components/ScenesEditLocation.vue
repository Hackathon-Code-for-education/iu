<script setup lang="ts">
import { useQueryClient } from '@tanstack/vue-query'
import {
  getOrganizationsGetByUsernameQueryKey,
  getOrganizationsReadQueryKey,
  getScenesGetScenesForOrganizationQueryKey,
  useOrganizationsGetByUsername,
  useOrganizationsUpdate,
  useScenesDelete,
  useScenesGetScenesForOrganization,
  useScenesUpdate,
} from '~/api'
import { type SceneExtended, type SceneMeta, composeSceneData } from '~/api/scenes'

const props = defineProps<{
  orgUsername: string
  orgId: string
  sceneId: string
}>()

const emit = defineEmits<{
  'update:sceneId': [sceneId: string]
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

const { mutate: removeScene } = useScenesDelete({
  mutation: {
    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: getScenesGetScenesForOrganizationQueryKey(props.orgId),
      })
      emit('update:sceneId', '')
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

const scenesOptions = computed(() => scenes.value?.data.map(scene => ({
  label: scene.title,
  value: scene.id,
})) || [])

const scene = computed(() => scenes.value?.data.find(scene => scene.id === props.sceneId) as SceneExtended | undefined)
const isMainOrgScene = computed(() => org.value?.data.main_scene === props.sceneId)
const scenesData = ref(scene.value ? { current: composeSceneData(scene.value, false) } : {})

const pannellum = ref(null)
const sceneInfo = reactive({
  title: scene.value?.title || '',
  yaw: scene.value?.meta.yaw || 0,
  pitch: scene.value?.meta.pitch || 0,
  hotSpots: scene.value?.meta.hotSpots || [],
  editingHotSpotNumber: -1,
})

watch(() => scene.value?.id, () => {
  if (!scene.value)
    return

  sceneInfo.title = scene.value.title || ''
  sceneInfo.yaw = scene.value.meta.yaw || 0
  sceneInfo.pitch = scene.value.meta.pitch || 0
  sceneInfo.hotSpots = scene.value.meta.hotSpots || []
  sceneInfo.editingHotSpotNumber = -1

  scenesData.value = { current: composeSceneData(scene.value) }
})

function restorePosition() {
  pannellum.value?.viewer.stopMovement()
  sceneInfo.yaw = scene.value?.meta.yaw || 0
  sceneInfo.pitch = scene.value?.meta.pitch || 0
  sceneInfo.editingHotSpotNumber = -1
}

function save() {
  if (!scene.value)
    return

  pannellum.value?.viewer.stopMovement()
  updateScene({ id: scene.value.id, data: {
    title: sceneInfo.title,
    meta: {
      yaw: sceneInfo.yaw,
      pitch: sceneInfo.pitch,
      hotSpots: sceneInfo.hotSpots,
    } as SceneMeta,
  } })
}

function remove() {
  removeScene({ id: props.sceneId })
}

function setAsMain() {
  if (!scene.value)
    return

  updateOrg({ id: props.orgId, data: { main_scene: props.sceneId } })
}

function updateHotSpots() {
  if (!pannellum.value)
    return

  // Remove all hotspots
  for (const hotSpot of pannellum.value.viewer.getConfig().hotSpots)
    pannellum.value.viewer.removeHotSpot(hotSpot.id)

  // Add hotspots
  for (const index in sceneInfo.hotSpots) {
    if (sceneInfo.hotSpots[index].yaw === 0 && sceneInfo.hotSpots[index].pitch === 0)
      continue
    pannellum.value.viewer.addHotSpot({
      id: index,
      type: 'scene',
      yaw: sceneInfo.hotSpots[index].yaw,
      pitch: sceneInfo.hotSpots[index].pitch,
      text: sceneInfo.hotSpots[index].text,
    })
  }
}

function newHotSpot() {
  if (!pannellum.value)
    return

  sceneInfo.hotSpots = [
    ...sceneInfo.hotSpots,
    {
      yaw: 0,
      pitch: 0,
      text: '',
      sceneId: '',
      type: 'scene',
    },
  ]
  sceneInfo.editingHotSpotNumber = sceneInfo.hotSpots.length - 1
  updateHotSpots()
}

function removeHotSpot(index: number) {
  sceneInfo.hotSpots.splice(index, 1)
  sceneInfo.editingHotSpotNumber = -1
}

function onPannellumClick(event: any) {
  if (!pannellum.value || sceneInfo.editingHotSpotNumber === -1 || sceneInfo.editingHotSpotNumber >= sceneInfo.hotSpots.length)
    return

  const coords = pannellum.value?.viewer.mouseEventToCoords(event)
  sceneInfo.hotSpots = sceneInfo.hotSpots.map((hotSpot, index) => {
    if (index === sceneInfo.editingHotSpotNumber) {
      return {
        ...hotSpot,
        yaw: coords[1],
        pitch: coords[0],
      }
    }
    return hotSpot
  })
  updateHotSpots()
  sceneInfo.editingHotSpotNumber = -1
}

function handleHotspotTitleChange(index: number, v: string) {
  sceneInfo.hotSpots = sceneInfo.hotSpots.map((hotSpot, i) => {
    if (i === index) {
      return {
        ...hotSpot,
        text: v,
      }
    }
    return hotSpot
  })
  updateHotSpots()
}

function handleHotspotSceneChange(index: number, v: string) {
  sceneInfo.hotSpots = sceneInfo.hotSpots.map((hotSpot, i) => {
    if (i === index) {
      return {
        ...hotSpot,
        sceneId: v,
      }
    }
    return hotSpot
  })
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <div class="flex w-full gap-2 justify-between">
      <UButton
        :variant="isMainOrgScene ? 'ghost' : 'ghost'"
        :disabled="isMainOrgScene"
        :icon="isMainOrgScene ? 'i-mdi-check' : 'i-mdi-star'"
        class="w-fit"
        @click="setAsMain"
      >
        {{ isMainOrgScene ? 'Основная локация' : 'Сделать основной локацией' }}
      </UButton>
      <div class="flex gap-2">
        <UButton @click="save">
          Сохранить
        </UButton>
        <UButton color="red" @click="remove">
          Удалить
        </UButton>
      </div>
    </div>
    <UInput v-model="sceneInfo.title" class="w-full" label="Название локации" />
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
          @click="onPannellumClick"
        />

        <div
          v-if="sceneInfo.editingHotSpotNumber !== -1"
          class="absolute flex flex-col gap-2 justify-end right-0 top-0 text-green-600 font-medium"
        >
          Кликните на изображение, чтобы установить отметку
        </div>

        <div
          v-if="sceneInfo.yaw !== scene?.meta?.yaw && sceneInfo.editingHotSpotNumber === -1"
          class="absolute flex flex-col gap-2 justify-end right-0 bottom-0"
        >
          <UButton class="justify-center" @click="restorePosition">
            Восстановить позицию
          </UButton>
        </div>
      </ClientOnly>
    </div>
    <h3>Отметки на изображении</h3>
    <div class="flex flex-col gap-2">
      <div v-for="(hotspot, index) in sceneInfo.hotSpots" :key="index" class="flex gap-2">
        <UButton
          icon="i-mdi-pencil"
          :variant="sceneInfo.editingHotSpotNumber === index ? undefined : 'ghost'"
          @click="sceneInfo.editingHotSpotNumber = sceneInfo.editingHotSpotNumber === index ? -1 : index"
        />
        <UInput :model-value="hotspot.text" label="Подпись" placeholder="Подпись" @update:model-value="(v) => handleHotspotTitleChange(index, v)" />
        <USelect :model-value="hotspot.sceneId" label="Переход на локацию" placeholder="Переход на локацию" :options="scenesOptions" @update:model-value="(v) => handleHotspotSceneChange(index, v)" />
        <UButton icon="i-mdi-trash" variant="ghost" color="red" @click="removeHotSpot(index)" />
      </div>
      <div class="flex gap-2">
        <UButton icon="i-mdi-plus" variant="ghost" @click="newHotSpot">
          Добавить еще одну отметку
        </UButton>
      </div>
    </div>
  </div>
</template>
