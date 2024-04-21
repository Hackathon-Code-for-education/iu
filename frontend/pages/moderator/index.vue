<script lang="ts" setup>
import { useQueryClient } from '@tanstack/vue-query'
import {
  getUsersGetUsersWithPendingApprovementQueryKey,
  useOrganizationsReadAll,
  useUsersApproveUser,
  useUsersGetUsersWithPendingApprovement,
} from '~/api'
import { getFileUrl } from '~/api/file'

const queryClient = useQueryClient()
const { data } = useUsersGetUsersWithPendingApprovement()
const { data: orgs } = useOrganizationsReadAll()

const { mutate } = useUsersApproveUser({
  mutation: {
    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: getUsersGetUsersWithPendingApprovementQueryKey(),
      })
    },
  },
})

function getOrgById(id?: string) {
  if (!id)
    return
  return orgs?.value?.data.find(org => org.id === id)
}

function approve(id: string) {
  mutate({ params: { is_approve: true }, userId: id })
}

function reject(id: string) {
  mutate({ params: { is_approve: false }, userId: id })
}
</script>

<template>
  <UContainer>
    <div v-if="!data">
      <USkeleton class="w-[300px] h-[200px] rounded-xl" />
    </div>

    <div v-else>
      <Card class="p-4">
        <h3 class="mb-2">
          Пользователи, ожидающие проверки:
        </h3>
        <div v-if="data" class="flex flex-col gap-2">
          <Card v-for="user in data.data" :key="user.id" class="p-4 flex flex-col gap-2">
            <div class="flex justify-between">
              <div class="flex flex-col gap-2">
                <p>Имя: {{ user.name }}</p>
                <p>Телеграм: {{ user.telegram ? `@${user.telegram?.username}` : 'не подключен' }}</p>
                <p v-if="user.student_approvement?.status === 'pending'" class="items-center flex gap-2">
                  Ожидает подтверждения
                  <UIcon class="text-blue-500" name="i-octicon-clock-24" />
                  <UButton
                    v-if="user.student_approvement?.attachment"
                    :to="getFileUrl(user.student_approvement?.attachment)"
                    variant="outline"
                  >
                    Просмотреть документ
                  </UButton>
                </p>
                <UButton
                  :to="`/${getOrgById(user.student_approvement?.organization_id)?.username}`"
                  variant="outline"
                  color="blue"
                >
                  {{ getOrgById(user.student_approvement?.organization_id)?.name }}
                </UButton>
              </div>
              <div class="flex flex-col gap-2">
                <UButton
                  label="Одобрить"
                  variant="outline"
                  class="h-fit"
                  @click="() => approve(user.id)"
                />
                <UButton
                  label="Отклонить"
                  variant="outline"
                  class="h-fit"
                  color="red"
                  @click="() => reject(user.id)"
                />
              </div>
            </div>
          </Card>
        </div>
      </card>
    </div>
  </UContainer>
</template>
