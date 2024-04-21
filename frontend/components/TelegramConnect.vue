<script setup lang="ts">
import { useQueryClient } from '@tanstack/vue-query'
import { getUsersGetMeQueryKey, useProvidersTelegramConnect } from '~/api'

const queryClient = useQueryClient()
const me = useMe()

const config = useRuntimeConfig()
const botName = config.public.telegramBot

const { mutate } = useProvidersTelegramConnect({
  mutation: {
    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: getUsersGetMeQueryKey(),
      })
    },
  },
})

function callback(data: any) {
  mutate({ params: data })
}
</script>

<template>
  <div v-if="me.loggedIn && !me.me.value?.telegram">
    <TelegramLoginButton mode="callback" :telegram-login="botName" @callback="callback" />
  </div>
</template>
