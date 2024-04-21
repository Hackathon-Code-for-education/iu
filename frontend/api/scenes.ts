import type { Scene } from './__generated__'
import { getFileUrl } from '~/api/file'

export interface SceneExtended extends Scene {
  meta: SceneMeta
}

export interface SceneMeta {
  yaw?: number
  pitch?: number
  hfov?: number
  hotSpots?: HotSpot[]
}

export interface HotSpot {
  text: string
  yaw: number
  pitch: number
  type: 'scene' | 'info'
  sceneId: string
}

export function composeSceneData(scene: SceneExtended, enableScenes: boolean = true) {
  return {
    panorama: getFileUrl(scene.file),
    title: scene.title,
    type: 'equirectangular',
    ...(scene.meta || {}),
    hotSpots: scene.meta?.hotSpots?.map(hotSpot => ({
      text: hotSpot.text || undefined,
      yaw: hotSpot.yaw || 0,
      pitch: hotSpot.pitch || 0,
      type: hotSpot.type || 'scene',
      sceneId: enableScenes ? hotSpot.sceneId || undefined : undefined,
    })) || [],
  }
}
