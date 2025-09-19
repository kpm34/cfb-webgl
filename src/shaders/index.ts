export const basicGlowFragment = /* glsl */ `
  uniform vec3 glowColor;
  void main() {
    gl_FragColor = vec4(glowColor, 1.0);
  }
`
