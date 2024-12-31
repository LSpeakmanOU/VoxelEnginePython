#version 330 core

layout (location = 0) out vec4 fragColor;

in float light_val;
in vec3 block_color;

vec3 getLight(vec3 color) {
    return color * vec3(light_val, light_val, light_val);
}

void main() {
    float gamma = 2.2;
    vec3 color = block_color;
    // Remove gamma from texture
    //color = pow(color, vec3(gamma));
    color = getLight(color);
    // Fix overall gamma
    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}