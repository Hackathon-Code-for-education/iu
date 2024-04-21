<script setup lang="ts">
import { useQueryClient } from '@tanstack/vue-query'
import { getUsersGetMeQueryKey, useProvidersTelegramLogin } from '~/api'

const queryClient = useQueryClient()

const config = useRuntimeConfig()
const botName = config.public.telegramBot

const { mutate } = useProvidersTelegramLogin({
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
  <div class="flex justify-center items-center w-full text-center">
    <TelegramLoginButton mode="callback" :telegram-login="botName" @callback="callback" />
  </div>
</template>
