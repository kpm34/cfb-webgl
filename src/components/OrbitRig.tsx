import { OrbitControls } from '@react-three/drei'

export interface OrbitRigProps {
  enableDamping?: boolean
  dampingFactor?: number
  minDistance?: number
  maxDistance?: number
}

export function OrbitRig({
  enableDamping = true,
  dampingFactor = 0.1,
  minDistance = 1,
  maxDistance = 20,
}: OrbitRigProps) {
  return (
    <OrbitControls
      enableDamping={enableDamping}
      dampingFactor={dampingFactor}
      minDistance={minDistance}
      maxDistance={maxDistance}
    />
  )
}
