import { Html, useGLTF } from '@react-three/drei'
import { Suspense } from 'react'

export interface GLTFLoaderViewProps {
  url: string
}

export function GLTFLoaderView({ url }: GLTFLoaderViewProps) {
  const { scene } = useGLTF(url, true)
  return (
    <Suspense fallback={<Html center>Loading model…</Html>}>
      <primitive object={scene} />
    </Suspense>
  )
}

useGLTF.preload as unknown
