<script setup lang="ts">
import { z } from 'zod'
import { useQueryClient } from '@tanstack/vue-query'
import type { FormSubmitEvent } from '#ui/types'
import { getOrganizationsGetByUsernameQueryKey, getOrganizationsReadQueryKey, useOrganizationsRead, useOrganizationsUpdate } from '~/api'

const props = defineProps<{
  orgId: string
}>()

const toast = useToast()
const queryClient = useQueryClient()
const updateOrg = useOrganizationsUpdate({ mutation: {
  onSuccess: (res) => {
    toast.add({ color: 'green', title: 'Данные обновлены' })
    queryClient.invalidateQueries({
      queryKey: getOrganizationsReadQueryKey(res.data.id),
    })
    queryClient.invalidateQueries({
      queryKey: getOrganizationsGetByUsernameQueryKey(res.data.username),
    })
  },
} })
const {
  data: org,
  isLoading: orgLoading,
} = useOrganizationsRead(props.orgId, { query: { retry: 0 } })

const schema = z.object({
  username: z.string().min(1, 'Обязательное поле'),
  name: z.string().min(1, 'Обязательное поле'),
  fullName: z.string().min(1, 'Обязательное поле'),
})
type Schema = z.infer<typeof schema>
const form = ref()
const state = reactive({
  username: '',
  name: '',
  fullName: '',
})

function handleReset() {
  form.value.clear()
  const orgData = org.value?.data
  if (!orgData)
    return
  state.username = orgData.username
  state.name = orgData.name
  state.fullName = orgData.full_name
}

watch(org, (newOrg) => {
  const orgData = newOrg?.data
  if (!orgData)
    return

  state.username = orgData.username
  state.name = orgData.name
  state.fullName = orgData.full_name
})

const formDisabled = computed(() => orgLoading.value || updateOrg.isPending.value)
const formChanged = computed(() => {
  const orgData = org.value?.data
  if (!orgData)
    return false
  return (
    state.username !== orgData.username
    || state.name !== orgData.name
    || state.fullName !== orgData.full_name
  )
})

function handleSubmit(event: FormSubmitEvent<Schema>) {
  const orgData = org.value?.data
  if (!orgData)
    return

  updateOrg.mutate({
    id: orgData.id,
    data: {
      username: event.data.username,
      name: event.data.name,
      full_name: event.data.fullName,
    },
  })
}
</script>

<template>
  <UContainer v-if="org">
    <Card class="p-4">
      <UForm ref="form" :schema="schema" :state="state" class="space-y-4" @submit="handleSubmit">
        <UFormGroup required name="username" label="Ник-нейм" help="Короткое название организации, которое будет содержаться в ссылке.">
          <UInput v-model="state.username" :disabled="formDisabled" />
        </UFormGroup>

        <UFormGroup required name="name" label="Краткое название учреждения">
          <UInput v-model="state.name" :disabled="formDisabled" />
        </UFormGroup>

        <UFormGroup required name="fullName" label="Полное название учреждения">
          <UTextarea v-model="state.fullName" :disabled="formDisabled" />
        </UFormGroup>

        <UButton class="mr-2" type="submit" :disabled="formDisabled || !formChanged">
          Сохранить
        </UButton>
        <UButton variant="outline" :disabled="formDisabled || !formChanged" @click="handleReset">
          Отменить
        </UButton>
      </UForm>
    </Card>
  </UContainer>
</template>
