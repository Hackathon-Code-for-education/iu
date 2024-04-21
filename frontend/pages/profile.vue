<script lang="ts" setup>
import { useOrganizationsRead, useUsersGetMyReviews } from '~/api'

const { me, loggedIn } = useMe()
const { data: reviews } = useUsersGetMyReviews()
const { state: chattingState, startChatting, stopChatting } = useChattingAsStudent()

watch(loggedIn, (newLoggedIn) => {
  if (newLoggedIn === false)
    navigateTo('/login')
}, { immediate: true })

const approvementOrganizationId = computed(() => me.value?.student_approvement?.organization_id ?? '')
const suspendApprovementOrganizationFetching = computed(() => approvementOrganizationId.value === '')
const { data: org } = useOrganizationsRead(approvementOrganizationId, { query: { suspense: suspendApprovementOrganizationFetching } })

function handleToggleChatting(newVal: boolean) {
  if (newVal)
    startChatting()
  else
    stopChatting()
}

onBeforeUnmount(() => {
  stopChatting()
})
</script>

<template>
  <UContainer>
    <div v-if="!me">
      <USkeleton class="w-[300px] h-[200px] rounded-xl" />
    </div>

    <div v-else class="grid grid-cols-3 gap-4">
      <Card class="p-4 col-span-1 flex flex-col gap-4">
        <UFormGroup label="Имя">
          <UInput :model-value="me.name" disabled />
        </UFormGroup>

        <UDivider />

        <div v-if="!me.student_approvement">
          Подтвердите статус студента
        </div>
        <UFormGroup v-else-if="me.student_approvement.status === 'approved'">
          <template #label>
            <UPopover mode="hover">
              <span class="flex items-center gap-1 mb-1">
                Образовательное учреждение
                <UIcon class="text-green-500" name="i-octicon-verified-24" />
              </span>

              <template #panel>
                <p class="text-sm p-1">
                  Вы подтвердили, что являетесь студентом этого ВУЗа.
                </p>
              </template>
            </UPopover>
          </template>
          <UInput :model-value="org?.data.name ?? '...'" disabled />
        </UFormGroup>
        <UFormGroup v-else-if="me.student_approvement.status === 'pending'">
          <template #label>
            <UPopover mode="hover">
              <span class="flex items-center gap-1 mb-1">
                Образовательное учреждение
                <UIcon class="text-blue-500" name="i-octicon-clock-24" />
              </span>
              <template #panel>
                <p class="text-sm p-1">
                  Ожидайте подтверждения вашего статуса студента.
                </p>
              </template>
            </UPopover>
          </template>
          <p class="text-sm mb-2">
            Ваш запрос находится на рассмотрении.
          </p>
          <UInput :model-value="org?.data.name ?? '...'" disabled />
        </UFormGroup>
        <UFormGroup v-else-if="me.student_approvement.status === 'rejected'">
          <template #label>
            <UPopover mode="hover">
              <span class="flex items-center gap-1 mb-1">
                Образовательное учреждение
                <UIcon class="text-red-500" name="i-octicon-blocked-24" />
              </span>
              <template #panel>
                <p class="text-sm p-1">
                  Статус студента не подтвержден.
                </p>
              </template>
            </UPopover>
          </template>
          <p class="text-sm mb-2">
            Ваш запрос отклонен. Подайте новую заявку на странице вуза.
          </p>
          <UInput :model-value="org?.data.name ?? '...'" disabled />
        </UFormGroup>

        <UDivider v-if="me.student_approvement?.status === 'approved'" />

        <div v-if="me.student_approvement?.status === 'approved'">
          <UFormGroup>
            <template #label>
              <UPopover mode="hover">
                <span class="flex items-center gap-1 mb-1">
                  Общение с абитуриентами
                  <UIcon name="i-heroicons-information-circle" />
                </span>

                <template #panel>
                  <p class="text-sm p-1">
                    Включите, если вы готовы к общению с абитуриентами.
                  </p>
                </template>
              </UPopover>
            </template>
            <UToggle
              :model-value="chattingState !== 'idle'"
              :disabled="chattingState === 'starting' || chattingState === 'stopping'"
              @update:model-value="handleToggleChatting"
            />
          </UFormGroup>
        </div>

        <UDivider />

        <UFormGroup v-if="!me.telegram" label="Подключить телеграм">
          <TelegramConnect />
        </UFormGroup>
        <UFormGroup v-if="me.telegram" label="Телеграм">
          <div class="flex flex-col gap-2 text-sm">
            Вы можете использовать виджет Telegram для входа в аккаунт.
            <UInput :model-value="me.telegram.username || me.telegram.last_name || me.telegram.id" disabled />
          </div>
        </UFormGroup>
      </Card>
      <Card class="p-4 col-span-2">
        <h3 class="mb-2">
          Мои отзывы:
        </h3>
        <div v-if="reviews" class="flex flex-col gap-2">
          <Card v-for="review in reviews.data" :key="review.id" class="p-4 flex flex-col gap-2">
            <div class="flex justify-between">
              <Rating readonly size="sm" :model-value="review.rate" />
              <UButton
                :to="`/${review.organization_username}`"
                :label="review.organization_name"
                class="w-fit"
                variant="ghost"
              />
            </div>
            <div class="flex justify-between">
              <p>{{ review.text }}</p>
              <p>{{ new Date(review.at).toLocaleString("ru-RU") }}</p>
            </div>
          </Card>
        </div>
      </Card>
    </div>
  </UContainer>
</template>
