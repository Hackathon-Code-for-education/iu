import {VueQueryPlugin} from '@tanstack/vue-query'
import { defineNuxtPlugin } from '#imports'

export default defineNuxtPlugin((nuxtApp) => {
 nuxtApp.vueApp.use(VueQueryPlugin)
})
