<script>
import { getFileUrl } from '~/api/file.ts'

export default {
  computed: {
    scenes() {
      return {
        main: {
          title: 'Университет',
          hfov: 110,
          pitch: -3,
          yaw: 117,
          type: 'equirectangular',
          panorama: getFileUrl('6623c9af9ef35baea042874f'),
          hotSpots: [
            {
              pitch: 25,
              yaw: 7,
              type: 'scene',
              text: 'Внутрь',
              sceneId: 'hall',
            },
          ],
        },

        hall: {
          title: 'Холл',
          hfov: 110,
          yaw: 5,
          type: 'equirectangular',
          panorama: getFileUrl('6623f6e34f5a9a64a37cedf8'),
          hotSpots: [
            {
              pitch: -2,
              yaw: 240,
              type: 'scene',
              text: 'Снаружи',
              sceneId: 'main',
              targetYaw: 25,
              targetPitch: 2,
            },
          ],
        },
      }
    },
  },
}
</script>

<template>
  <ClientOnly>
    <VuePannellum
      :default="{
        firstScene: 'main',
        sceneFadeDuration: 1000,
      }"
      :scenes="scenes"
      :pitch="25"
      auto-load
      show-fullscreen
      style="width: 100%; height: 300px;"
    />
  </ClientOnly>
</template>
