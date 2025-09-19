import { Canvas } from '@react-three/fiber'
import { CameraRig } from '../components/CameraRig'
import { OrbitRig } from '../components/OrbitRig'

export const BasicScene = () => (
  <div style={{ width: '100%', height: '60vh' }}>
    <Canvas>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />
      <CameraRig />
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="#00aaff" />
      </mesh>
      <OrbitRig />
    </Canvas>
  </div>
)

BasicScene.storyName = 'Basic Scene'
