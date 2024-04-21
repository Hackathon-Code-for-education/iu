<script setup lang="ts">
import { z } from 'zod'
import { useQueryClient } from '@tanstack/vue-query'
import type { AxiosError } from 'axios'
import axios from 'axios'
import type { FormSubmitEvent } from '#ui/types'
import { getUsersGetMeQueryKey, useProvidersByCredentials } from '~/api'

const { loggedIn } = useMe()
const schema = z.object({
  login: z.string(),
  password: z.string().min(4, 'Минимальная длина 4 символа'),
})
type Schema = z.output<typeof schema>

watch(loggedIn, (newLoggedIn) => {
  if (newLoggedIn)
    navigateTo('/profile')
}, { immediate: true })
const queryClient = useQueryClient()
const loginByCreds = useProvidersByCredentials()

const state = reactive({
  login: '',
  password: '',
})
const errorMsg = ref<string>()

function handleSubmit(event: FormSubmitEvent<Schema>) {
  loginByCreds
    .mutateAsync({ data: event.data })
    .catch((err: AxiosError) => {
      if (axios.isAxiosError(err) && err.response?.status === 401)
        errorMsg.value = 'Неверное имя пользователя или пароль'
      else
        errorMsg.value = 'Произошла ошибка'
    })
    .then(() => {
      queryClient.invalidateQueries({
        queryKey: getUsersGetMeQueryKey(),
      })
    })
}
</script>

<template>
  <UContainer class="flex items-center justify-center">
    <Card class="py-4 px-8 m-auto w-[350px]">
      <h1 class="text-center text-2xl mb-4">
        Авторизация
      </h1>
      <UForm :schema="schema" :state="state" class="space-y-4" @submit="handleSubmit">
        <UFormGroup label="Имя пользователя" name="login" :error="errorMsg">
          <UInput v-model="state.login" :disabled="loginByCreds.isPending.value" />
        </UFormGroup>

        <UFormGroup label="Пароль" name="password">
          <UInput v-model="state.password" :disabled="loginByCreds.isPending.value" type="password" />
        </UFormGroup>

        <UButton :disabled="loginByCreds.isPending.value" type="submit">
          Войти
        </UButton>
      </UForm>
    </Card>
  </UContainer>
</template>
