<script setup lang="ts">
import { useQueryClient } from '@tanstack/vue-query'
import {
  getScenesGetScenesForOrganizationQueryKey,
  useFilesUploadFile,
  useScenesCreate,
} from '~/api'

const props = defineProps<{
  orgUsername: string
  orgId: string
}>()

const emit = defineEmits<{
  setSceneId: [sceneId: string]
}>()

const queryClient = useQueryClient()

const { mutate: createScene, isPending: createScenePending } = useScenesCreate({
  mutation: {
    onSuccess(data) {
      queryClient.setQueryData(getScenesGetScenesForOrganizationQueryKey(props.orgId), (oldData: any) => {
        if (!oldData)
          return oldData

        return {
          ...oldData,
          data: [...oldData.data, data.data],
        }
      })
      emit('setSceneId', data.data.id)
    },
  },
})

const { mutate: uploadFile, isPending: uploadFilePending } = useFilesUploadFile({
  mutation: {
    onSuccess(res) {
      createScene({
        data: {
          organization: props.orgId,
          title: 'Новая локация',
          meta: {},
          file: res.data.id,
        },
      })
    },
  },
})

function create(fileList: FileList | null) {
  const file = fileList?.[0]
  if (!file)
    return

  uploadFile({ data: { upload_file_obj: file } })
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <p>Установите приложение Google Camera и сделайте 3D-панораму места.</p>
    <p>Загрузите получившийся .jpg файл на этой странице.</p>

    <div class="py-8 flex items-center">
      <UInput type="file" size="sm" accept=".jpg" @change="create" />
      <UButton
        v-if="uploadFilePending || createScenePending"
        size="sm"
        variant="ghost"
        color="gray"
        icon="i-mdi-loading"
        class="ml-2"
        loading
      >
        Загрузка...
      </UButton>
    </div>
  </div>
</template>
