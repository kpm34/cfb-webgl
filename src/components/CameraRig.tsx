import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'
import type { PerspectiveCamera } from 'three'

export interface CameraRigProps {
  /** Damping for smooth follow */
  damping?: number
  /** Target position the camera eases toward */
  target?: [number, number, number]
}

export function CameraRig({ damping = 0.1, target = [0, 1.5, 4] }: CameraRigProps) {
  const ref = useRef<PerspectiveCamera>(null)

  useFrame((_state, delta) => {
    const cam = ref.current
    if (!cam) return
    cam.position.x += (target[0] - cam.position.x) * Math.min(1, damping * delta * 60)
    cam.position.y += (target[1] - cam.position.y) * Math.min(1, damping * delta * 60)
    cam.position.z += (target[2] - cam.position.z) * Math.min(1, damping * delta * 60)
    cam.lookAt(0, 0, 0)
  })

  return <perspectiveCamera ref={ref} fov={50} near={0.1} far={1000} />
}
