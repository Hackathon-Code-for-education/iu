<script>
export default {
  computed: {
    hotSpots() {
      return []
    },
    scenes() {
      return {
        main: {
          title: 'Университет',
          hfov: 110,
          type: 'equirectangular',
          panorama: '/original.jpg',
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
