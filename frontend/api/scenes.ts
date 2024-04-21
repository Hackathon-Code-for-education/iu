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
  scene: string
}

export function composeSceneData(scene: SceneExtended) {
  return {
    panorama: getFileUrl(scene.file),
    title: scene.title,
    type: 'equirectangular',
    ...(scene.meta || {}),
  }
}
